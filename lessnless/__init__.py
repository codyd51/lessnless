from mingus.midi import fluidsynth
from mingus.containers.note_container import NoteContainer
from mingus.containers.note_container import Note
import mingus.core.scales as scales

import time
import random

from pprint import pprint

fluidsynth.init('../Nice-Keys-Ultimate-V2.3.sf2')

chords = [
    NoteContainer(['C-2',
                   'E-2',
                   'G-2']),

    NoteContainer(['F-2',
                   'A-2',
                   'C-3']),

    NoteContainer(['G-2',
                   'B-2',
                   'D-3']),

    NoteContainer(['A-2',
                   'C-3',
                   'E-3']),
]

def get_chord_set():
    usable_chords = chords
    chord_set = []
    for i in range(3):
        chord = random.choice(usable_chords)
        chord_set.append(chord)
        usable_chords.remove(chord)
    return chord_set

# chorys has dynamic range of notes,
# intro simple, less notes
# 8 bars for each section: intro, verse, chorus, bridge

class SongSegment(object):
    def __init__(self):
        self.chord = self.get_chord()
        possible_note_counts = [4, 8, 16]
        note_count = random.choice(possible_note_counts)
        self.notes = self.get_notes(note_count, self.chord)

    def get_chord(self):
        return random.choice(chords)

    def get_notes(self, count, chord):
        notes = []
        copy_note = random.choice(chord.notes)
        starting_note = Note(name=copy_note.name, octave=copy_note.octave + 2)

        scale_notes = scales.Major('C').ascending()
        current_scale_idx = scale_notes.index(starting_note.name)
        current_note = starting_note

        for i in range(count):
            notes.append(Note(current_note))

            # go up or down on the scale?
            off = 1
            if random.choice([True, False]):
                off = -1
            current_scale_idx = (current_scale_idx + off) % len(scale_notes)
            current_note = scale_notes[current_scale_idx]

        return notes

    def play(self):
        if len(self.notes) == 4:
            for i in range(4):
                self.play_bar(self.chord, self.notes)
        elif len(self.notes) == 8:
            for i in range(2):
                self.play_bar(self.chord, self.notes[0:4])
                self.play_bar(self.chord, self.notes[4:8])
        elif len(self.notes) == 16:
            for i in range(1):
                self.play_bar(self.chord, self.notes[0:4])
                self.play_bar(self.chord, self.notes[4:8])
                self.play_bar(self.chord, self.notes[8:12])
                self.play_bar(self.chord, self.notes[12:16])

    def play_bar(self, chord, notes):
        beat_time = 0.225
        bar_time = beat_time * len(notes)

        fluidsynth.set_instrument(1, 5)
        fluidsynth.play_NoteContainer(chord)

        fluidsynth.set_instrument(1, 0)
        for i in range(4):
            fluidsynth.play_Note(notes[i])
            time.sleep(beat_time)
            fluidsynth.stop_Note(notes[i])
        fluidsynth.stop_NoteContainer(chord)

    def __repr__(self):
        return '<SongSegment chord: {} notes: {}>'.format(self.chord, self.notes)


class Song(object):
    SEGMENT_ORDER = ['intro',
                     'verse',
                     'chorus',
                     'bridge']
    def __init__(self):
        self.intro = SongSegment()
        self.verse = SongSegment()
        self.chorus = SongSegment()
        self.bridge = SongSegment()

        self.segments = [self.intro,
                         self.verse,
                         self.chorus,
                         self.bridge,
                        ]

        for i, seg in enumerate(self.segments):
            print('{}: {}'.format(Song.SEGMENT_ORDER[i], seg))

    def play(self):
        # intro, verse, chorus, verse, chorus, bridge, chorus
        play_pattern = [0, 1, 2, 1, 2, 3, 2]
        for segment_index in play_pattern:
            print('Playing {} segment'.format(Song.SEGMENT_ORDER[segment_index]))
            self.segments[segment_index].play()

s = Song()
s.play()

