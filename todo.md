## Top
- create color engine, for different themes, brightnesses etc
- Show root notes, pentatonic notes, etc in different colors/shades
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0
- Live performance mode with instruments along x, pitch on y, time steps through z.

### Hardware
- create color engine, for different themes, brightnesses etc

### synchronize with Ableton
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0

### Save and load
- How to do that when running on external hardware? Startup menu? Probably only viable via ssh connection

### convert everything to asynchronous/event driven
- midi time and button pressed events kind of already are, can it be better?

### Z-mode
- Usability tweaks, like instrument speed etc

### Handle LED colors better
- Show root notes, pentatonic notes, etc in different colors/shades
- Root note for pentatonics
- root and pentatonic for modes
- Should be handled by sequencer.get_led_status/get_led_grid, seq has access to scale and cell info

### Transfer to Ableton
- Button/whatever to trigger transfer currently playing instrument (or all) to ableton clips
- Send cmds to start recording at start of page/bar for each active instrument/channel, then stop recording once page(s) completed
- Could do the same thing in reverse to import and manipulate live midi

### unit tests remaining
- for controller, display(?), recent new features

### Performance improvements
- fork trellis, seesaw etc
- batch cmds
- don't autoshow
