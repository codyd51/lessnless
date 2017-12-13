import random
import sys

from mingus.containers.note import Note
import mingus.core.scales as scales
from mingus.containers.bar import Bar


class Progression(object):
    def __init__(self, note_count, chord):
        self.note_count = note_count
        self.chord = chord
        self._generated_note_count = 0

    def generate_notes(self):
        raise NotImplementedError('Use concrete Progression subclass')

    def _get_starting_note(self):
        copy_note = random.choice(self.chord.notes)
        octave_jump = random.choice([1, 2])
        starting_note = Note(name=copy_note.name, octave=copy_note.octave + octave_jump)
        return starting_note


from song import Song


class CadenceTiming(object):
    def __init__(self, start_time, count):
        self.start_time = start_time
        self.eighth_count = count

    def __repr__(self):
        return '<note play {} eighths at {}>'.format(self.eighth_count, self.start_time)


class Cadence(object):
    def __init__(self, beat_count):
        self.beat_count = beat_count
        self.eighth_count = self.beat_count*2
        self.times = None

    def generate_timings(self):
        raise NotImplementedError('use concrete Cadence subclass')


class CadenceStrategyQuarterHalf(Cadence):
    def generate_timings(self):
        self.times = []
        time = 0
        for bar_index in range(self.beat_count / 4):
            if random.random() < 0.2:
                # add a whole note
                self.times.append(CadenceTiming(time, 8))
                time += 8
            else:
                # choose between:
                # quarter, quarter, quarter, quarter
                # quarter,half,quarter
                # quarter, quarter, half
                # half, quarter, quarter,
                # half, half
                type = random.choice([0, 1, 2, 3, 4])
                if type == 0:
                    # add 4 quarters
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                if type == 1:
                    # add quarter
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                    # add half
                    self.times.append(CadenceTiming(time, 4))
                    time += 4
                    # add quarter
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                elif type == 2:
                    # add quarter
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                    # add quarter
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                    # add half
                    self.times.append(CadenceTiming(time, 4))
                    time += 4
                elif type == 3:
                    # add half
                    self.times.append(CadenceTiming(time, 4))
                    time += 4
                    # add quarter
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                    # add quarter
                    self.times.append(CadenceTiming(time, 2))
                    time += 2
                elif type == 4:
                    # add half
                    self.times.append(CadenceTiming(time, 4))
                    time += 4
                    # add half
                    self.times.append(CadenceTiming(time, 4))
                    time += 4
        # sanity check
        # ensure we consumed all bars
        time_sum = 0
        for timing in self.times:
            time_sum += timing.eighth_count
        if time_sum != self.eighth_count:
            raise ValueError('Cadance didn\'t produce correct number of beats! {} instead of {}'.format(
                time_sum,
                self.eighth_count
            ))
        return self.times


class CadenceStrategyQuickNotes(Cadence):
    # TODO(PT): add HalfNote/QuarterNote/EighthNote instead of manipulating `time` directly
    def generate_timings(self):
        self.times = []
        time = 0
        for bar_index in range(self.beat_count / 4):
            count_in_bar = self.beat_count * 2
            count_so_far = 0
            # go for number of eighths in a bar
            while count_so_far < count_in_bar:
                # choose whether to add a quarter or half note
                place_quarter_note = random.random() < 0.9
                # only add a quarter note if there's enough time in the bar
                if place_quarter_note:
                    if count_in_bar - count_so_far < 2:
                        place_quarter_note = False

                count_to_use = 1
                if place_quarter_note:
                    count_to_use = 2
                self.times.append(CadenceTiming(time, count_to_use))
                time += count_to_use

                count_so_far += count_to_use
        return self.times


class StepProgression(Progression):
    def generate_notes(self):
        notes = []
        starting_note = self._get_starting_note()

        scale_notes = Song.get_c_scale()
        current_scale_idx = scale_notes.index(starting_note.name)
        current_raw_note = starting_note

        for i in range(self.note_count):
            notes.append(current_raw_note)

            step = 1
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
