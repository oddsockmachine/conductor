## Top
- multi-instrument support: program new ones, and add cfg pages
- multi-color support
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0
- redo euclidean.regen algorithm
- fix lint issues around constants import

### Add small screen for better feedback
- from lcd import lcd
- lcd.line1("Select:")
- Each instrument presents 5 lines of status
- Or 4 lines, plus a line for recent messages/alerts

### Handle LED colors better
- different backgrounds for each instrument number and type
- create color engine, for different themes, brightnesses, background gradient, etc https://www.sweetwater.com/store/detail/Fire--akai-professional-fire-grid-controller-for-fl-studio
- Show gridlines, root notes, pentatonic notes, etc in different colors/shades
- call background(x, y) to get a color code for general background pixel, as chosen by some other setting/algo
- Show root notes, pentatonic notes, etc in different colors/shades
- Should be handled by instrument.get_led_status/get_led_grid, has access to scale and cell info
- semi-transparent config screens? See underlying instrument underneath

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

### BeatMaker
- Each drum instrument has a horizontal track
- Each horizontal cell is a different pattern (or no pattern) for each instrument
- Select a set of patterns for each instrument, change on the fly
- Show hits and highlight beatpos as normal
- 4x4 grid for saved pattern combos. Touch current to reset, touch other to load next page and save previous

### Binary Sequencer?
- Like Orca, but maybe use it for arpeggios and chords

### Chord Sequencer
- Specify chords on a timeline
- Specify how chord is played (tight, wide etc)
- Each step, chord voicing is generated on the fly for variation

### Droplets
- Touch high up, droplet falls with high velocity
- Touch low down, droplet falls with low velocity
- Touch above note to drag/extend it
- Touch below note to catch/remove it
- Add multiple drops per line?

### Drum Deviator - Random Deviation Beat Sequencer
- (suppressed: slightly darker - triggered: slightly brighter - transposed: different color)
- Allow multiple pages per instrument
- Randomness/chaos amount should be per bar, not per note. eg: at low levels, only change a few notes occasionally
- TODO randomness controls cover all pages - maybe they should be per-page?
- TODO apply_randomness doesn't show effects on LED grid
- TODO maybe fire chance shouldn't add notes randomly, only add where there are already other notes

### Drum Machine
Steal ideas from eg TR8s
Volume Faders for each instrument?

### Elaborator
- Draw a beat/pattern on a page
- Select which of the page repeats will be elaborated (eg every 4th)
- Add randomness to that repeat, but only use notes that are already on the page

### Euclidean Beat Generator

### Octopus
- TopRight 8x8 shows pages and controls. Save, select, clear pages

### Sequencer
- sequencer could be 15 notes high, one row dedicated to pages/repeats
- Copy page functionality

### Transformer
- Take a sequencer pattern, press one button to mutate by a set amount, another button to save the current state

### CC Controller
- Send CC messages
- Set up LFOs or timed transitions

### Marbles?
- Like mutable instruments, shift register style pattern randomness

### Keyboard
- Just for playing instruments directly

### Z-Mode
- Use for display only
- Maybe a screensaver?


### synchronize with Ableton
- call sequencer.restart() when controller receives "songpos" msg - all instruments reset to page 0, beatpos 0
- quick hack is to press a button to sync that
- synchronize sequences/pages with clips in Ableton. Use Live to launch, hardware to edit

### Transfer to Ableton
- Button/whatever to trigger transfer currently playing instrument (or all) to ableton clips
- Send cmds to start recording at start of page/bar for each active instrument/channel, then stop recording once page(s) completed
- Could do the same thing in reverse to import and manipulate live midi

### convert everything to asynchronous/event driven
- midi time and button pressed events kind of already are, can it be better?
- Not sure necessary, speed is more than adequate now

### MIDI control
- Each variable has a uid and can have midi CC's routed to it
- Might not be useful or practical, each instrument has its own config, why add more controls?
