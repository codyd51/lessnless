from mingus.midi import fluidsynth
from mingus.containers.note_container import NoteContainer
from mingus.containers.note_container import Note
import mingus.core.scales as scales

import json
import time


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


class Song(object):
    SEGMENT_ORDER = ['intro',
                     'verse',
                     'chorus',
                     'bridge']

    def __init__(self):
        self.chord = None
        self.melody = None
        self.segments = {}

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

from song_segment import SongSegment


class GeneratedSong(Song):
    def __init__(self):
        super(self.__class__, self).__init__()

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
        s = Song()
        with open(filename, 'r') as song_file:
            data = json.loads(song_file.read())
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
