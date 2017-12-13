from lessnless.song import Song
from lessnless.melody import Melody
from mingus.midi import fluidsynth
from mingus.containers.note_container import NoteContainer

import random
import time
import math
import numpy as np



class SongSegment(object):
    def __init__(self, generate=True, possible_chords=Song.get_c_chords(), beat_count=16):
        if not generate:
            return

        self.chord = self.get_chord(possible_chords)
        self.beat_count = beat_count
        self.melody = Melody(self.beat_count, self.chord)

    @staticmethod
    def get_chord(possible_chords):
        return random.choice(possible_chords)

    def play(self):
        eighth_time = 0.125
        beat_time = eighth_time * 2
        bar_time = beat_time * self.beat_count

        fluidsynth.set_instrument(1, 0)
        fluidsynth.play_NoteContainer(self.chord)

        next_notes = list(self.melody.notes)
        playing_notes = []

        for eighth in range(self.beat_count*2):
            # bar boundary?
            if eighth % 8 == 0:
                self.play_chord()

            try:
                next_note = next_notes[0]
            except IndexError as e:
                # if this is the last note, the above will throw an IndexError
                pass

            if next_note.start_eighth == eighth:
                next_notes.remove(next_note)
                playing_notes.append(next_note)

                print('subbeat {}: PLAY FOR {}: {}'.format(eighth, next_note.eighth_count, next_note.note))
                fluidsynth.set_instrument(1, 0)
                fluidsynth.play_Note(next_note.note)

            for mel_note in list(playing_notes):
                if eighth == mel_note.start_eighth + mel_note.eighth_count:
                    print('subbeat {}: STOP        {}'.format(eighth, mel_note.note))

                    # don't stop the note if the same note is being played somewhere else!
                    note_played_elsewhere = False
                    for note in playing_notes:
                        # skip over this one, we're interested in other notes
                        if note == mel_note:
                            continue
                        if note.note == mel_note.note:
                            note_played_elsewhere = True

                    if not note_played_elsewhere:
                        fluidsynth.stop_Note(mel_note.note)

                    playing_notes.remove(mel_note)

            time.sleep(eighth_time)
        # we should have played the exact
        # if it isn't, something went wrong somewhere
        if len(playing_notes) != 0:
            #raise RuntimeError('playing_notes wasn\'t empty at the end of segment.play()!')
            print('EOS playing_notes: {}'.format(playing_notes))
            for mel_note in playing_notes:
                fluidsynth.stop_Note(mel_note.note)
                playing_notes.remove(mel_note)

    def play_chord(self):
        fluidsynth.stop_NoteContainer(self.chord)
        fluidsynth.set_instrument(1, 0)
        fluidsynth.play_NoteContainer(self.chord)

    def __repr__(self):
        return '<SongSegment chord: {} notes: {}>'.format(self.chord, self.melody.notes)

