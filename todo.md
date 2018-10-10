## Most Important
* Figure out why everything waits while mouse button held!
* Buttons for scale, key, octave, drum controls, save on exit

### Convert display to separate service
- Communicate via messages

### unit tests remaining
- for controller, display(?), recent new features

### delegate drawing to a Display component - which can be switched out for eg LEDs, GUI, etc.
- build out gui, include
    borders, dividers (between bars, octaves etc)
    different colors for curses glyphs
- Start on converting to Kivy, for raspi/touchscreen solution

### Controls for adding/changing pages/instruments, setting musical constraints etc
- Turn off note repeat for an instrument - adjacent notes sustain instead of retriggering

### synchronize with Ableton
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0

### Save and load
- Load in piano roll using command line arg (almost, saved note conversion needs work)
- Add beat division/speed to load/save

### convert everything to asynchronous/event driven

### Z-mode
- normally time moves along the x-axis, pitch on y, instruments on z.
- Live performance mode with instruments along x, pitch on y, time steps through z.
- In other words, the ability to play all 16 instruments in real time

### set random range for page repeats
- to keep things interesting

### Handle LED colors better
- Show root notes, pentatonic notes, etc in different colors/shades
- Root note for pentatonics
- root and pentatonic for modes
- Should be handled by sequencer.get_led_status/get_led_grid, seq has access to scale and cell info

### Dual mode
- How to have one sequencer running/looping live, but have another being built up in the background/cue output?
- So a "done"/playing song can be left for a short time, while the start of another is built up behind the scenes
- Probably best to split 16 instruments/channels into 2 sets (since most controllers only handle 8 at a time)
- Channels/9-16 would mirror 1-8 in Ableton, but when triggered it would be possible to crossfade between them/transfer control
- Might just be easiest to do this entirely in Ableton, send 9-16 to cue track and switch over with one slider

### Transfer to Ableton
- Button/whatever to trigger transfer currently playing instrument (or all) to ableton clips
- Send cmds to start recording at start of page/bar for each active instrument/channel, then stop recording once page(s) completed
- Could do the same thing in reverse to import and manipulate live midi
