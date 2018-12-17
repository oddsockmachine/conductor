## Top
- create color engine, for different themes, brightnesses etc
- Show root notes, pentatonic notes, etc in different colors/shades
- Turn off note repeat for an instrument - adjacent notes sustain instead of retriggering
- set random range for page repeats
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0
- Live performance mode with instruments along x, pitch on y, time steps through z.

### Hardware
- create color engine, for different themes, brightnesses etc

### unit tests remaining
- for controller, display(?), recent new features

### Controls for adding/changing pages/instruments, setting musical constraints etc
- Turn off note repeat for an instrument - adjacent notes sustain instead of retriggering

### synchronize with Ableton
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0

### Save and load
- Load in piano roll using command line arg (almost, saved note conversion needs work)
- Add beat division/speed to load/save
- How to do that when running on external hardware? Startup menu? Probably only viable via ssh connection

### convert everything to asynchronous/event driven
- midi time and button pressed events kind of already are, can it be better?

### Z-mode
- normally time moves along the x-axis, pitch on y, instruments on z.
- Live performance mode with instruments along x, pitch on y, time steps through z.
- In other words, the ability to play all 16 instruments in real time

### set random range for page repeats
- to keep things interesting, good for ambient music

### Handle LED colors better
- Show root notes, pentatonic notes, etc in different colors/shades
- Root note for pentatonics
- root and pentatonic for modes
- Should be handled by sequencer.get_led_status/get_led_grid, seq has access to scale and cell info

### Transfer to Ableton
- Button/whatever to trigger transfer currently playing instrument (or all) to ableton clips
- Send cmds to start recording at start of page/bar for each active instrument/channel, then stop recording once page(s) completed
- Could do the same thing in reverse to import and manipulate live midi
