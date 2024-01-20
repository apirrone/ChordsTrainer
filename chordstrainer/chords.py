import re

# https://github.com/AnthonyChiavelli/PyChordFinder/blob/master/ChordFinder.py

chr_scale = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

chord_names = {
    "Major": {"pattern": [0, 4, 7], "abbrvs": ["maj", "M", "Maj", "Δ"]},
    "Minor": {"pattern": [0, 3, 7], "abbrvs": ["min", "m", "Min", "-"]},
    "Major7": {"pattern": [0, 4, 7, 11], "abbrvs": ["maj7", "M7", "Maj7", "Δ7"]},
    "Augmented": {"pattern": [0, 4, 8], "abbrvs": ["aug", "+"]},
    "Diminished": {"pattern": [0, 3, 6], "abbrvs": ["dim", "°"]},
    "Diminished7": {"pattern": [0, 3, 6, 9], "abbrvs": ["dim7", "°7"]},
    "Half-diminished7": {"pattern": [0, 3, 6, 10], "abbrvs": ["m7b5", "-7b5"]},
    "Minor-major7": {"pattern": [0, 3, 7, 11], "abbrvs": ["mM7", "-M7"]},
    "Augmented7": {"pattern": [0, 4, 8, 10], "abbrvs": ["+7"]},
    "Augmented major7": {"pattern": [0, 4, 8, 11], "abbrvs": ["+M7"]},
    "Minor7": {"pattern": [0, 3, 7, 10], "abbrvs": ["m7", "-7"]},
    "Major6": {"pattern": [0, 4, 7, 9], "abbrvs": ["M6", "6"]},
    "Minor6": {"pattern": [0, 3, 7, 9], "abbrvs": ["m6", "-6"]},
    "Dominant7": {"pattern": [0, 4, 7, 10], "abbrvs": ["7"]},
    "Sus2": {"pattern": [0, 2, 7], "abbrvs": ["sus2"]},
    "Sus4": {"pattern": [0, 5, 7], "abbrvs": ["sus4"]},
    "Add9": {"pattern": [0, 2, 4, 7], "abbrvs": ["add9"]},
}

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
    print(chord_name)
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
    if len(abbrs) > 0:
        abbrs = abbrs[0]
    if len(degrees) > 0:
        degrees = degrees[0]

    return chords_found, abbrs, degrees
