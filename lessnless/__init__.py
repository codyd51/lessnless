from mingus.midi import fluidsynth
from mingus.containers.note_container import NoteContainer
from mingus.containers.note_container import Note
import mingus.core.scales as scales

import time
import random
import json
import threading

from pprint import pprint

fluidsynth.init('../Nice-Keys-Ultimate-V2.3.sf2')


class Song(object):
    SEGMENT_ORDER = ['intro',
                     'verse',
                     'chorus',
                     'bridge']

    def __init__(self, generate=True):
        self.segments = {}
        if not generate:
            return

        chords = Song.get_c_chords()
        for i in range(4):
            seg = SongSegment(possible_chords=chords)
            chords.remove(seg.chord)

            self.segments[Song.SEGMENT_ORDER[i]] = seg
            print('{}: {}'.format(Song.SEGMENT_ORDER[i], seg))

        song_dump = json.dumps(self, default=dumper, indent=2)
        timestamp = int(time.time())
        filename = 'lessnless-{}.json'.format(timestamp)
        with open(filename, 'w') as song_file:
            song_file.write(song_dump)
            print('Dumped song to {}'.format(filename))

    @classmethod
    def get_c_chords(cls):
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
        return chords

    def play(self):
        intro = self.segments['intro']
        fluidsynth.play_NoteContainer(intro.chord)
        time.sleep(0.25 * 8)
        fluidsynth.stop_NoteContainer(intro.chord)
        # intro, verse, chorus, verse, chorus, bridge, chorus
        play_pattern = [0, 1, 2, 1, 2, 3, 2]
        for segment_index in play_pattern:
            print('Playing {} segment'.format(Song.SEGMENT_ORDER[segment_index]))
            self.segments[Song.SEGMENT_ORDER[segment_index]].play()

        outro = self.segments['chorus']
        for i in range(3):
            fluidsynth.play_NoteContainer(outro.chord)
            time.sleep(0.25 * 8)
            fluidsynth.stop_NoteContainer(outro.chord)

    @classmethod
    def inflate_song(cls, filename):
        s = Song(generate=False)
        with open(filename, 'r') as song_file:
            data = json.loads(song_file.read())
            pprint(data)
            for segment_name, segment_data in data['segments'].iteritems():
                print('segment_name {}'.format(segment_name))
                segment_idx = cls.SEGMENT_ORDER.index(segment_name)

                print('inflating {} from {}'.format(segment_name, segment_data))
                s.segments[Song.SEGMENT_ORDER[segment_idx]] = cls.inflate_segment(segment_data)
        return s

    @classmethod
    def inflate_segment(cls, segment_data):
        s = SongSegment(generate=False)
        s.chord = None
        s.notes = []
        for note_data in segment_data['notes']:
            note = Note(name=str(note_data['name']), octave=int(note_data['octave']))
            s.notes.append(note)
        chord_notes = []
        for note_data in segment_data['chord']['notes']:
            note = Note(name=str(note_data['name']), octave=int(note_data['octave']))
            chord_notes.append(note)
        s.chord = NoteContainer(chord_notes)
        return s


class MelodyNote(object):
    def __init__(self, note, beat_count):
        self.note = note
        self.beat_count = beat_count

    def __repr__(self):
        return '<{}, {} beats>'.format(self.note, self.beat_count)


class Melody(object):
    def __init__(self, chord):
        self.notes = self.get_notes(16, chord)

    def get_notes(self, beat_count, chord):
        notes = []
        copy_note = random.choice(chord.notes)
        starting_note = Note(name=copy_note.name, octave=copy_note.octave + 2)

        scale_notes = scales.Major('C').ascending()
        current_scale_idx = scale_notes.index(starting_note.name)
        current_raw_note = starting_note

        i = 0
        while i < beat_count:
            note_lengths = range(1, 4)
            current_note_length = random.choice(note_lengths)
            notes.append(MelodyNote(current_raw_note, current_note_length))

            # increment i by the number of beats used by this note
            i += current_note_length

            # go up or down on the scale?
            off = 1
            if random.choice([True, False]):
                off = -1
            current_scale_idx = (current_scale_idx + off) % len(scale_notes)
            current_raw_note = Note(name=scale_notes[current_scale_idx], octave=current_raw_note.octave)

        return notes


class SongSegment(object):
    def __init__(self, generate=True, possible_chords=Song.get_c_chords()):
        if not generate:
            return

        self.chord = self.get_chord(possible_chords)
        self.notes = None
        self.melody = Melody(self.chord)

    def get_chord(self, possible_chords):
        return random.choice(possible_chords)

    def play(self):
        beat_time = 0.25
        bar_time = beat_time * 16

        fluidsynth.set_instrument(1, 0)
        fluidsynth.play_NoteContainer(self.chord)

        note_idx = 0
        current_note = self.melody.notes[note_idx]
        fluidsynth.play_Note(current_note.note)
        note_end_beat_idx = current_note.beat_count

        for beat in range(16):
            if beat % 4 == 0:
                fluidsynth.stop_NoteContainer(self.chord)
                fluidsynth.set_instrument(1, 0)
                fluidsynth.play_NoteContainer(self.chord)

            if beat == note_end_beat_idx:
                fluidsynth.stop_Note(current_note.note)
                note_idx += 1
                current_note = self.melody.notes[note_idx]
                note_end_beat_idx += current_note.beat_count
                fluidsynth.set_instrument(1, 0)
                fluidsynth.play_Note(current_note.note)

            time.sleep(beat_time)

    def __repr__(self):
        return '<SongSegment chord: {} notes: {}>'.format(self.chord, self.melody.notes)


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


list = [
    1508651627,
    1508651653,
    1508651704,
    1508651730,
]

for timestamp in list:
    name = 'lessnless-{}.json'.format(timestamp)
    #s = Song.inflate_song(name)
    s = Song()
    s.play()
    break

