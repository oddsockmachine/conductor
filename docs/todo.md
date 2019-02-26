## Top
- multi-instrument support
- create color engine, for different themes, brightnesses, background gradient, etc https://www.sweetwater.com/store/detail/Fire--akai-professional-fire-grid-controller-for-fl-studio
- Show gridlines, root notes, pentatonic notes, etc in different colors/shades
- call background(x, y) to get a color code for general background pixel, as chosen by some other setting/algo
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0


### synchronize with Ableton
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0
- quick hack is to press a button to sync that

### Save and load
- On startup, show colored pixels for numbered sets. Allows 255 memory slots, plus use 1 for empty
- Show that screen as a menu
- Click an empty pixel to save there

### convert everything to asynchronous/event driven
- midi time and button pressed events kind of already are, can it be better?
- Not sure necessary, speed is more than adequate now

### Z-mode
- Usability tweaks, like instrument speed etc
- Will probably ignore, now that 16 instruments may all be different type
- Maybe use as a display mode instead

### Generic Display
- Could it show two different 1/2 size instruments, one above the other?
- Or a 3/4 size instrument with a partial menu?
- Selectable, pluggable instruments - ie pick up to 16 of sequencer, drum randomizer, random generator etc

### Handle LED colors better
- create color engine, for different themes, brightnesses etc
- Show root notes, pentatonic notes, etc in different colors/shades
- Root note for pentatonics
- root and pentatonic for modes
- Should be handled by sequencer.get_led_status/get_led_grid, seq has access to scale and cell info

### Performance improvements
- fork trellis, seesaw etc
- batch cmds
- don't autoshow
- port to raspberry pi

### Add small screen for better feedback
from screen import sprint
sprint.line1("Select:")

### MIDI control
- Each variable has a uid and can have midi CC's routed to it

### Inspirations for new instruments
- Arc https://www.youtube.com/watch?v=HM0EBvJe1s0
- Euclidean https://www.youtube.com/watch?v=OHS3lN6snrE&t=29s
-           https://www.youtube.com/watch?v=vwigqSwYNaQ
- Lightbath https://www.youtube.com/channel/UCNcpKG4D0_nxBYwtgD4iA7w
- step through notes
- orca https://www.youtube.com/watch?v=4LIOVdtqgQg
-      https://www.youtube.com/watch?v=gG1ZEigm99A&t=0s&list=PLMZROl1GNSMHJHpEsBsqqDx-G9nn9uAVI&index=2
- flin https://vimeo.com/418349
- Meadowphysics https://monome.org/docs/modular/meadowphysics/
- general https://monome.org/docs/grid-studies/python/

## Instruments

- Handle saving/loading of different instruments
- Better inheritance
- Each instrument should handle their own status
- How to deal with multiple options for each instrument type?

### Grid Sequencer

### Z-Mode

### Euclidean Beat Generator
- For each drum-note/sample, set a bar length (<16), euclidean density, and offset

### Random Beat Generator
- For each drum-note/sample, the ability to generate a random sequence with specific sparsity/density
- Each note line can be regenerated at will
- Create multiple pages once happy with a particular page

### Random Deviation Beat Sequencer
- Draw a beat on a sequencer grid
- Each drum-note/sample has a separate random chance of suppressing/firing/transposing
- Show drum sequencer along bottom 16x8, with notes that are modified for this bar highlighted
- (suppressed: slightly darker - triggered: slightly brighter - transposed: different color)
- Use the top 16x8 for controls like randomness per note
- Allow multiple pages per instrument
- Transposition could/should be predictable, eg to +8 notes
- Random notes for each bar determined at start of bar
- Randomness/chaos amount should be per bar, not per note. eg: at low levels, only change a few notes occasionally

### Chord Sequencer
- Specify chords on a timeline
- Specify how chord is played (tight, wide etc)
- Each step, chord voicing is generated on the fly for variation

### Binary Sequencer?
- Like Orca, but maybe use it for arpeggios and chords

### Droplets
- Like Flin
- Droplets fall vertically
- Pitch is horizontal
- Touch high up, droplet falls with high velocity
- Touch low down, droplet falls with low velocity
- Pitch is triggered when droplet reaches bottom
- Touch above note to drag/extend it
- Touch below note to catch/remove it

## BeatMaker
- Each drum instrument has a vertical track
- Each vertical cell is a different pattern (or no pattern) for that instrument
- Select a set of patters for each instrument, change on the fly

### Transformer
- Take a sequencer pattern, press one button to mutate by a set amount, another button to save the current state



### Transfer to Ableton
- Button/whatever to trigger transfer currently playing instrument (or all) to ableton clips
- Send cmds to start recording at start of page/bar for each active instrument/channel, then stop recording once page(s) completed
- Could do the same thing in reverse to import and manipulate live midi

### unit tests remaining
- for controller, display(?), recent new features
