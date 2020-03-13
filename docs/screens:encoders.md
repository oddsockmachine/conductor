# A (far left)
### A Screen
Current instrument name and basic stats
### A LED color
### A Click
Show global controls
### A Scroll
Scroll through instruments, click to select

# B (center left)
### B Screen
### B LED color
### B Click
### B Scroll

# C (center right)
### C Screen
### C LED color
### C Click
### C Scroll

# D (far left)
### D Screen
### D LED color
### D Click
Show instrument level controls
### D Scroll


each instrument has its own state and logic for screen contents, encoder reactions etc
need a de/multiplexor to relay enc/screen info through the correct busses

what if global config screen is like another instrument?
so gbl_cfg, 16x instruments and 16x ins_cfg are all the same type/interface

