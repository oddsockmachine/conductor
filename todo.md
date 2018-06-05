Create Cursor component
convert between standard xy and curses xy - all positions, calculations etc should be done in standard, only convert to curses when it's time to draw

midi in for clock detection
midi out for each instrument at beat_step (and remember to note_off where necessary)
convert from y position to midi note depending on scale, key and octave

build out gui, include info, buttons, borders etc


Z-mode - normally time moves along the x-axis, pitch on y, instruments on z. Live performance mode with instruments along x, pitch on y, time steps through z. In other words, the ability to play all 16 instruments in real time
