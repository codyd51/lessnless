import random
from mingus.containers.note import Note
import mingus.core.scales as scales


class Progression(object):
    def __init__(self, beat_count, chord):
        self.beat_count = beat_count
        self.chord = chord
        self._generated_note_count = 0

    def generate_notes(self):
        raise NotImplementedError('Use concrete Progression subclass')

    def _get_starting_note(self):
        copy_note = random.choice(self.chord.notes)
        octave_jump = 1
        if random.choice([True, False]):
            octave_jump = 2
        starting_note = Note(name=copy_note.name, octave=copy_note.octave + octave_jump)
        return starting_note

    def _get_next_note_length(self):
        # first, check if we're done generating notes
        if self._generated_note_count == self.beat_count:
            return 0

        note_lengths = range(1, 4)
        current_note_length = random.choice(note_lengths)
        # was this more than beats we have left?
        overlap = self._generated_note_count + current_note_length - self.beat_count
        if overlap > 0:
            # bind note length to beats we have left
            current_note_length -= overlap
        self._generated_note_count += current_note_length
        return current_note_length


from song import Song


class StepProgression(Progression):
    def generate_notes(self):
        notes = []
        starting_note = self._get_starting_note()

        scale_notes = Song.get_c_scale()
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
