from lessnless.song import Song
from lessnless.melody import Melody
from mingus.midi import fluidsynth

import random
import time


class SongSegment(object):
    def __init__(self, generate=True, possible_chords=Song.get_c_chords(), beat_count=16):
        if not generate:
            return

        self.chord = self.get_chord(possible_chords)
        self.beat_count = beat_count
        self.notes = None
        self.melody = Melody(self.beat_count, self.chord)

    @staticmethod
    def get_chord(possible_chords):
        return random.choice(possible_chords)

    def play(self):
        beat_time = 0.25
        bar_time = beat_time * self.beat_count

        fluidsynth.set_instrument(1, 0)
        fluidsynth.play_NoteContainer(self.chord)

        note_idx = 0
        current_note = self.melody.notes[note_idx]
        fluidsynth.play_Note(current_note.note)
        note_end_beat_idx = current_note.beat_count

        for beat in range(self.beat_count):
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

