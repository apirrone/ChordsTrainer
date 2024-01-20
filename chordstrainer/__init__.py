import multiprocessing
from multiprocessing import Queue

import pygame

pygame.display.init()
pygame.font.init()


data_queue = Queue()


def midi_process():
    import mido

    from chordstrainer.chords import find_chords

    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    min_note = 21

    pressed = {}
    inport = mido.open_input("uMIDI/O22:uMIDI/O22 MIDI 1 20:0")
    for msg in inport:
        if "note" not in msg.type:
            continue
        note = int(msg.note)
        # note = (int(msg.note) - min_note) % len(notes)
        if msg.type == "note_on":
            if note not in pressed:
                pressed[note] = 1
        elif msg.type == "note_off":
            if note in pressed:
                del pressed[note]

        chord = tuple([(note - min_note) % 12 for note in sorted(pressed.keys())])
        chord_notes = [notes[note] for note in chord]
        names, abbrs, degrees = find_chords(" ".join([notes[note] for note in chord]))

        data_queue.put(
            {
                "chord_notes": chord_notes,
                "names": names,
                "abbrs": abbrs,
                "degrees": degrees,
            }
        )
        # print(" ".join([notes[note] for note in chord]))
        # print(names, abbrs)


def main():
    screen = pygame.display.set_mode((500, 300), flags=pygame.SRCALPHA + pygame.NOFRAME)

    multiprocessing.Process(target=midi_process).start()
    data = {"chord_notes": [], "names": [], "abbrs": [], "degrees": []}
    while True:
        screen.fill((255, 255, 255))
        try:
            data = data_queue.get(False)
        except multiprocessing.queues.Empty:
            pass

        font = pygame.font.SysFont("Arial", 30)
        text = font.render(" ".join(data["chord_notes"]), True, (0, 0, 0))
        screen.blit(text, (0, 0))

        if len(data["names"]) > 0:
            # display main chord name in big in the middle
            font = pygame.font.SysFont("Arial", 60)
            text = font.render(data["names"][0], True, (0, 0, 0))
            screen.blit(
                text, (250 - text.get_width() // 2, 150 - text.get_height() // 2)
            )

        if len(data["abbrs"]) > 0:
            # display abbrs smaller below
            font = pygame.font.SysFont("Arial", 30)
            text = font.render(", ".join(data["abbrs"]), True, (0, 0, 0))
            screen.blit(
                text, (250 - text.get_width() // 2, 180 + text.get_height() // 2)
            )

        if len(data["degrees"]) > 0:
            # Display degrees under the chord_notes in small
            # degrees is a dict of {note: degree}

            font = pygame.font.SysFont("Arial", 20)
            for i, chord_note in enumerate(data["chord_notes"]):
                text = font.render(data["degrees"][chord_note], True, (0, 0, 0))
                screen.blit(text, (3 + i * 30, 30))

        pygame.display.flip()
