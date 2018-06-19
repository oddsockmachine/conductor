# Sequencer needs to be synchronized!
- Different instruments are starting at different times!
- workaround: create all 16 instruments at the same time
- but ensure instruments with different tempos are synced to start at the same time

# unit tests
- for cursor, controller, display(?)

# delegate drawing to a Display component - which can be switched out for eg LEDs, GUI, etc.
- Use curses windows/panes to deal with window offsets
- build out gui, include
    info, current instrument, page status, key, octave, scale
    buttons: new instrument/page, switch instrument, inc/dec repeats
    borders, dividers (between bars, octaves etc)
    different colors for curses glyphs - maybe use all filled boxes, but greyscale
    etc
- Switch themes on the fly

# Tempo
- Select subdivision of tempo - 4ths, 16ths, etc. Do we want slow individual notes, or faster quarter notes?
- Do this per instrument - drums might be faster/more subdivided, but repeat often - melody might be slower

# Controls for adding/changing pages/instruments, setting musical constraints etc
- Mouse input for grid - not as awesome as a dedicated instrument, but easier to use than the arrows+enter
- When adding instrument, select from helpful presets: eg drums
- When adding instrument, select from same scale as sequencer or chromatic/drum - is there any value in selecting a different scale?
- Change octave of page/instrument at runtime
- Change key/scale of whole sequencer (or non-drum instruments) at runtime?
- Turn off note repeat for an instrumment - adjacent notes sustain instead of retriggering
- Clear notes from current page / current instrument

# synchronize with Ableton
- already in time, but are start of bars always the same or offset?
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0

# Save and load
- Save each piano roll on exit
- Load in piano roll using command line arg
- load in piano roll using runtime option

# convert everything to asynchronous/event driven

# is it possible/desirable to edit a page while another page is playing?

# listen for midi notes in on all channels
- add note to current beat of relevant instrument
- would allow live playing and editing of an instrument

# Z-mode
- normally time moves along the x-axis, pitch on y, instruments on z.
- Live performance mode with instruments along x, pitch on y, time steps through z.
- In other words, the ability to play all 16 instruments in real time

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
- Probably best to split 16 instruments/channels into 2 sets (since most controllers only handle 8 at a time)
- Channels/9-16 would mirror 1-8 in Ableton, but when triggered it would be possible to crossfade between them/transfer control

# Transfer to Ableton
- Button/whatever to trigger transfer currently playing instrument (or all) to ableton clips
- Send cmds to start recording at start of page/bar for each active instrument/channel, then stop recording once page(s) completed
- Could do the same thing in reverse to import and manipulate live midi
