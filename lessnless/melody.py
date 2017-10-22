import random
from mingus.containers.note import Note
import mingus.core.scales as scales


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
