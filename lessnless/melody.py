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

        note_length = self._get_next_note_length()
        while note_length is not 0:
            notes.append(MelodyNote(current_raw_note, note_length))

            # choose step
            step = random.choice([1, 2])
            # go up or down on the scale?
            if random.choice([True, False]):
                step = -step

            # check if we're going to change octaves
            octave_change = 0
            if current_scale_idx + step >= scale_notes:
                octave_change = 1
            elif current_scale_idx + step < 0:
                octave_change = -1
            current_raw_note.octave += octave_change

            current_scale_idx = (current_scale_idx + step) % len(scale_notes)
            current_raw_note = Note(name=scale_notes[current_scale_idx], octave=current_raw_note.octave)

            note_length = self._get_next_note_length()

        return notes



class MelodyNote(object):
    def __init__(self, note, beat_count):
        self.note = note
        self.beat_count = beat_count

    def __repr__(self):
        return '<{}, {} beats>'.format(self.note, self.beat_count)


class Melody(object):
    def __init__(self, beats, chord):
        self.notes = self.get_notes(beats, chord)

    def get_notes(self, beat_count, chord):
        # TODO(PT): randomly choose between StepProgression and something else, IntervalProgression
        strategy = StepProgression(beat_count, chord)
        return strategy.generate_notes()
