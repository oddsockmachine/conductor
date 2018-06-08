
# unit tests
- for cursor, controller, display(?)

# delegate drawing to a Display component - which can be switched out for eg LEDs, GUI, etc.
- build out gui, include
    grid relative position
    info, current instrument, page status, key, octave, scale
    buttons,
    borders, dividers (between bars, octaves etc)
    etc
- Switch themes on the fly

# Controls for adding/changing pages/instruments, setting musical constraints etc
- When adding instrument, select from helpful presets: eg drums

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
- Root note for pentatonics
- root and pentatonic for modes
- Should be handled by sequencer.get_led_status/get_led_grid, seq has access to scale and cell info

# Dual mode
- How to have one sequencer running/looping live, but have another being built up in the background/cue output?
- So a "done"/playing song can be left for a short time, while the start of another is built up behind the scenes
