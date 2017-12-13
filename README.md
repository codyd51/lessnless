lessnless
-------

Music generator.

This tool automates song generation. Each song is composed of 4 segments, which are generated and then played in a specific order:

```
intro
verse 
chorus 
bridge
```

A segment is composed of a cadence (note timing) paired with a melody (set of notes to be played according to the note timings),
and a harmony (the background chords).

When generating a song segment, a random strategy for the cadence will be chosen.

Cadences can have quick, staccato notes, or longer intervals between notes, in different patterns depending on the strategy.

Then, when the melody is generated, it will chose one of several different strategies for note steps. For example,
it might choose to do single-steps up or down on the scale at each timing interval.

Every generated song is dumped to a json file which this library can parse, allowing generated songs to be saved and replayed.

This tool expects [this file](https://drive.google.com/file/d/0B3zFERJ2rMQpYnlHQ2tOUVBfeXc/view?usp=sharing) in
the top level directory. You can use any sound font you want, just be sure to change the file name in `__init__.py`.

MIT license.

