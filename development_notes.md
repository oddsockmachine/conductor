## Architecture

Display

Cursor

Controller

Sequencer

Instrument

Note_Grid


## Constants

Constants are shared throughout the program, and do not change at runtime.
They typically represent limitations of hardware, for example the width of the visible grid.
In future, the constants will likely change depending on what hardware the sequencer is running against.

## Note positions

We always refer to notes by x/y coordinates, where:
  x is the beat position along the horizontal axis from the left
  y is the note pitch along the veritcal axis from the bottom.
In other words,
  x=0 is the first bar, x=15 is the last bar
  y=0 is the lowest pitch, y=15 is the highest pitch.

Notes are stored in a note_grid, which is a list (of len W) of columns.
Each column is al list of ints representing the state of the notes in that column.
The states are defined in the constants file.
The y/pitch of the note in the column is its index in the list.

This sometimes seems at odds with a traditional coordinate system, or the way an array is naively printed out.
This is done to ensure the note_grid always represents _notes_ versus time, not necessarily their position on a display.
When a note_grid is ready for display, only then do we do the necessary conversion to absolute position.
Each component should ideally have a print method for debugging its state, which will handle that conversion.
However, the internal representation of that component's state should be in whatever format is most fitting.
