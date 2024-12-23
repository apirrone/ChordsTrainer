import re
import random

# Heavily inspired by https://github.com/AnthonyChiavelli/PyChordFinder/blob/master/ChordFinder.py

# TODO handle flat notes
chr_scale = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

chord_names = {
    "Major": {"pattern": [0, 4, 7], "abbrvs": ["maj", "M", "Maj", "Δ"]},
    "Minor": {"pattern": [0, 3, 7], "abbrvs": ["min", "m", "Min", "-"]},
    "Major7": {"pattern": [0, 4, 7, 11], "abbrvs": ["maj7", "M7", "Maj7", "Δ7"]},
    "Dominant7": {"pattern": [0, 4, 7, 10], "abbrvs": ["7"]},
    "Minor7": {"pattern": [0, 3, 7, 10], "abbrvs": ["m7", "-7"]},
    "Half-diminished7": {"pattern": [0, 3, 6, 10], "abbrvs": ["m7b5", "-7b5"]},
    "Diminished7": {"pattern": [0, 3, 6, 9], "abbrvs": ["dim7", "°7"]},

    "Major6": {"pattern": [0, 4, 7, 9], "abbrvs": ["M6", "6"]},
    "Minor6": {"pattern": [0, 3, 7, 9], "abbrvs": ["m6", "-6"]},
    "Augmented": {"pattern": [0, 4, 8], "abbrvs": ["aug", "+"]},
    "Diminished": {"pattern": [0, 3, 6], "abbrvs": ["dim", "°"]},

    "Minor-major7": {"pattern": [0, 3, 7, 11], "abbrvs": ["mM7", "-M7"]},
    "Augmented7": {"pattern": [0, 4, 8, 10], "abbrvs": ["+7"]},
    "Augmented major7": {"pattern": [0, 4, 8, 11], "abbrvs": ["+M7"]},
    "Sus2": {"pattern": [0, 2, 7], "abbrvs": ["sus2"]},
    "Sus4": {"pattern": [0, 5, 7], "abbrvs": ["sus4"]},
    "Add9": {"pattern": [0, 2, 4, 7], "abbrvs": ["add9"]},
}

difficulties = {
    0: ["Major", "Minor", "Major7", "Dominant7", "Minor7", "Half-diminished7", "Diminished7"],
    1: ["Major", "Minor", "Major7", "Dominant7", "Minor7", "Half-diminished7", "Diminished7", "Major6", "Minor6", "Augmented", "Diminished"],
    2: ["Major", "Minor", "Major7", "Dominant7", "Minor7", "Half-diminished7", "Diminished7", "Major6", "Minor6", "Augmented", "Diminished", "Minor-major7", "Augmented7", "Augmented major7", "Sus2", "Sus4", "Add9"],
}

def get_chord_names(difficulty=0): # 3 levels ? 0, 1, 2
    names = {}
    for chord in difficulties[difficulty]:
        names[chord] = chord_names[chord]

    return names

def get_all_names(difficulty=0): # 3 levels ? 0, 1, 2
    chord_names = get_chord_names(difficulty)
    all_names = list(chord_names.keys())
    for chord, val in chord_names.items():
        all_names.extend(val["abbrvs"])

    return all_names



def find_chord_from_abbr(abbr):
    for name, val in chord_names.items():
        if abbr in val["abbrvs"] or abbr == name:
            return name, val
    return None

# TODO test this ? generated by copilot
def is_same_chord(chord1, chord2):
    ch1_root = chord1.split(" ")[0]
    ch2_root = chord2.split(" ")[0]
    ch1_abbr = chord1.split(" ")[1]
    ch2_abbr = chord2.split(" ")[1]


    chord1 = find_chord_from_abbr(ch1_abbr)
    chord2 = find_chord_from_abbr(ch2_abbr)
    notes1 = parse_chord(ch1_root + " " + chord1[0])
    notes2 = parse_chord(ch2_root + " " + chord2[0])
    return set(notes1) == set(notes2)


pattern_to_degree = {
    "0": "0",
    "1": "2b",
    "2": "2",
    "3": "3b",
    "4": "3",
    "5": "4",
    "6": "5b",
    "7": "5",
    "8": "6b",
    "9": "6",
    "10": "7b",
    "11": "7",
}


def gen_random_chord(difficulty=0):
    """
    Returns: chord name (random abbr), root, pattern
    """

    root = random.choice(chr_scale)
    chord_abbr = random.choice(get_all_names(difficulty))
    return root + " " + chord_abbr, root, find_chord_from_abbr(chord_abbr)[1]["pattern"]


if __name__ == "__main__":
    for i in range(200):
        print(gen_random_chord())


def parse_notes(notes):
    """Parses a string and converts valid notes to sharp notation

    Valid notes include a letter A-G, uppercase or lowercase, followed by
    between 0 and 2 sharp symbols (hash symbol "#") or between 0 and 2 flat
    symbols (lower case "b"). Notes are converted to their enharmonic
    equivalent if they contain a flat symbol, so only natural notes and sharp
    notes are returned.

    >>> parse_notes("C D J b D# G## Ab AB")
    ['C', 'D', 'A#', 'D#', 'A', 'G#', 'A', 'B']

    Args:
        A string containing valid notes
    Returns:
        A list of valid sharp-notation notes

    """
    raw_list = re.compile("[A-Ga-g][#b]{0,2}").findall(notes)
    parsed_list = []
    for note in raw_list:
        note_name = note[0]  # First character is name of note
        chr_note_pos = chr_scale.index(note_name.upper())  # Get chr_scale index
        # Increment or decrement if sharps or flats are found
        for char in note:
            if char == "#":
                chr_note_pos += 1
            elif char == "b":
                chr_note_pos -= 1
        # Get the enharmonic equivalent from chr_scale and append it to
        # the list to be returned.
        final_chr_note = chr_scale[(chr_note_pos + 12) % 12]
        parsed_list.append(final_chr_note)
    return parsed_list


def parse_chord(chord_name):
    # returns a list of notes in the chord
    # e.g. "C Major" -> ["C", "E", "G"]

    root = chord_name.split(" ")[0]
    name = chord_name.split(" ")[1:]
    name = " ".join(name)
    pattern = chord_names[name]["pattern"]

    notes = [chr_scale[(chr_scale.index(root) + interval) % 12] for interval in pattern]
    return notes


def get_abbrevs(chord_name):
    root = chord_name.split(" ")[0]
    name = chord_name.split(" ")[1]
    abbrevs = chord_names[name]["abbrvs"]
    return [root + abbr for abbr in abbrevs]


def get_degrees(chord_name):
    root = chord_name.split(" ")[0]
    notes = parse_chord(chord_name)

    # Find which degree each note is in the current chord, save it in a dict like {F:0, ...}
    degrees = {}
    for note in notes:
        interval = ((chr_scale.index(note) - chr_scale.index(root)) + 12) % 12
        degrees[note] = pattern_to_degree[str(interval)]

    return degrees


def find_chords(notes):
    """Finds chords that describe the notes given

    >>> find_chords("A, C#, E")
    ['A Major']
    >>> find_chords("C, E, G, E, C")
    ['C Major']
    >>> find_chords("C D G")
    ['C Sus2', 'G Sus4']

    Args:
        A list of notes in sharp notation

    Returns:
        A list of chord names that describe the given notes

    """
    notes = parse_notes(notes)
    chords_found = []

    # Each iteration, we assume a different note is the tonic
    for tonic in notes:
        pattern = []

        # Each note is compared to the tonic and a pattern is built
        for note in notes:
            interval = ((chr_scale.index(note) - chr_scale.index(tonic)) + 12) % 12
            pattern.append(interval)

        pattern = list(set(pattern))  # Eliminate duplicate intervals
        pattern.sort()

        # Match the pattern to one in the chord library
        for name, value in chord_names.items():
            match_pattern = value["pattern"]
            if pattern == match_pattern:
                chords_found.append(str(tonic) + " " + str(name))

    chords_found = list(set(chords_found))
    abbrs = [get_abbrevs(chord) for chord in chords_found]
    degrees = [get_degrees(chord) for chord in chords_found]

    # if len(abbrs) > 0:
    #     abbrs = abbrs[0]
    # if len(degrees) > 0:
    #     degrees = degrees[0]

    # place in the first position the chord which the lowest note is the tonic. For ex :

    # ['D# Major6', 'C Minor7']
    # [{'D#': '0', 'G': '3', 'A#': '5', 'C': '6'}, {'C': '0', 'D#': '3b', 'G': '5', 'A#': '7b'}]
    # ['C', 'G', 'A#', 'D#'] -> notes played from low to high. C is the lowest note, so C Minor7 should be first

    first_chord_index = 0
    for i, chord in enumerate(chords_found):
        if notes[0] == chord[0]:
            first_chord_index = i
            break

    chords_found = chords_found[first_chord_index:] + chords_found[:first_chord_index]
    abbrs = abbrs[first_chord_index:] + abbrs[:first_chord_index]
    degrees = degrees[first_chord_index:] + degrees[:first_chord_index]

    return chords_found, abbrs, degrees
