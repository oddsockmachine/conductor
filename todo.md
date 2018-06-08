
# unit tests
- for sequencer, cursor, controller, display(?)

# delegate drawing to a Display component - which can be switched out for eg LEDs, GUI, etc.
  Sequencer should pass in grid of LED statuses, display should decide how to draw it
  build out gui, include
    info, current instrument, page status, key, octave, scale
    buttons,
    borders, dividers (between bars, octaves etc)
    etc


# convert between standard xy and curses xy - all positions, calculations etc should be done in standard, only convert to curses when it's time to draw

# is it possible/desirable to edit a page while another page is playing?

# Save and load
- Save each piano roll on exit
- Load in piano roll using command line arg
- load in piano roll using runtime option

# Z-mode
- normally time moves along the x-axis, pitch on y, instruments on z.
- Live performance mode with instruments along x, pitch on y, time steps through z.
- In other words, the ability to play all 16 instruments in real time

# synchronize with Ableton
- already in time, but are start of bars the same or offset?
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0

# convert everything to asynchronous/event driven

# listen for midi notes in on all channels
- add note to current beat of relevant instrument
- would allow live playing and editing of an instrument

# set random range for page repeats
- to keep things interesting

# Handle LED colors better
- Show root notes, pentatonic notes, etc in different colors/shades
-  Root note for pentatonics
-  root and pentatonic for modes

# Dual mode
- How to have one sequencer running/looping live, but have another being built up in the background/cue output?
