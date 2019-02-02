## Architecture

#### Display

#### Cursor

#### Supercell

#### Conductor
  - A collection of Instruments operating in-sync
  - Provides no major added functionality, except to synchronize and control all of its Instruments
  - Provides a top level interface analagous to a real-world sequencer
  - Takes input to advance to next beat, and triggers all instruments to do the same
  - Returns visual representation of currently selected Instrument's currently playing Note_Grid when needed
  - Will eventually return split visuals for two instruments at once
  - Will eventually handle 'Z-mode', when all 16 instruments can be controlled in real-time

#### Instrument
  - Responsible for a stream of Midi out messages on a single channel
  - Analogous to a real instrument, its output will be fed into a Midi instrument
  - The Instrument may have one or more pages of Note_Grid/piano roll
  - Each page is played, and either repeated or the Instrument switches to the next page
  - The Instrument has a particular starting octave, root note/key, and musical scale
  - All notes on its pages are relative to those rules
  - When step_beat is called, the Instrument stops any notes it was previously playing, and advances the beat_position
  - The beat position is the current beat, as shown on the x position of a Note_Grid
  - The notes on the current page are then taken, and converted into midi notes according to octave, key, and scale
  - The Instrument outputs those notes on its assigned Midi channel
  - Most of its properties are set at creation. Helper methods are provided to get important information
  - Many helper methods exist to pass information down to the current/relevant page/Note_Grid

#### Note_Grid
  - Represents a page of notes that have been saved into the sequencer - like a section of piano roll
  - Notes do not actually have any pitch info, only relative position on a scale that is known to the Instrument
  - Provides helper functions to set and get note information
  - See "Note Positions" for info on how notes are stored and used
  - Each page can be repeated zero or more times. The Note_Grid knows how many repeats it has, but the Instrument handles whether to repeat or not

#### Constants

  - Constants are shared throughout the program, and do not change at runtime.
  - They typically represent limitations of hardware, for example the width of the visible grid.
  - In future, the constants will likely change depending on what hardware the sequencer is running against.

#### Note positions

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
