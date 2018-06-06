convert between standard xy and curses xy - all positions, calculations etc should be done in standard, only convert to curses when it's time to draw
reverse touch_note: higher y = higher note, currently 0 = highest/top row

delegate drawing to a Display component - which can be switched out for eg LEDs, GUI, etc. Sequencer should pass in grid of LED statuses, display should decide how to draw it
build out gui, include info, buttons, borders etc

Save each piano roll on exit
Load in piano roll using command line arg
load in piano roll using runtime option

Z-mode - normally time moves along the x-axis, pitch on y, instruments on z. Live performance mode with instruments along x, pitch on y, time steps through z. In other words, the ability to play all 16 instruments in real time


convert everything to asynchronous/event driven
