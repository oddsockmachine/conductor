# Conductor

## _A Grid instrument, sequencer and performance workstation for live music creation_

## Introduction

The _Conductor_ was designed to be the center of any electronic music setup. Whether you want to control modular synths, live loop, create giant improvised sets, control Ableton, or generate music algorithmically, the Conductor can do it all.

Think of it like the conductor in an orchestra; it's not making any noise, but it's flailing its arms wildly, keeping every instrument around it under control, in time, and in tune... and looking cool doing while it.

## Examples

- https://soundcloud.com/oddsockmachine/droplets

- https://www.youtube.com/watch?v=3huPQ8svOUQ

- https://www.youtube.com/watch?v=pdu7UI-fMRo

## Installation

`python3 -m venv ./venv && source venv/bin/activate`

`pip install -r requirements.txt`

`python controller.py [--hw 1]`

## Usage

The Conductor  has four modes:

- Load/Save set
  - Displays all saved sets as highlighted items on the grid.
  - When loading, select an existing saved set to load it.
  - When saving, select a blank space to save the set there (or overwrite an existing set).
  - Accessed on startup, or pressing `L`/`S` from the "global config" mode

- Global config
  - Controls configuration that affects the entire set.
  - Accessed by pushing the left button
  - Musical scale is represented at the top left with two characters. Pressing within those characters will scroll forward or back through available scales and set that across all instruments in the set.
  - Musical key/root note is represented below this, and works in the same way..
  - The `L` button will trigger the load set screen.
  - The `S` button will trigger the save set screen.
  - The `R` button will reset the set to its initial conditions.
  - The `D` button will delete the current instrument.
  - The rightmost column of pixels represents all instruments that have been added to the set. Pressing one will take you to that instrument's play screen.
  - The second rightmost column of pixels represents each of the different types of instruments that can be used. Pressing one will add the corresponding instrument to the set.

- Instrument config
  - Controls configurations that affect the currently selected instrument.
  - Accessed by pushing the right button.
  - Each instrument may have different controls based on its unique characteristics.
  - Full details of each instrument's controls are available in the `Instruments` section of this document.

- Play
  - Shows the performance screen of the currently selected instrument
  - Details about how each instrument works are available in the `Instruments` section of this document.

## Instruments

Each "instrument" is a different method of making music, controlling things, or generating inspiration.

Some have obvious analogs in the real world, like sequencers or drum machines, or MIDI control surfaces.

Others take inspiration from the worlds of modular synth, ambient and generative music for maximum flexibility.

Instruments are listed alphabetically, the same order they are available in when adding them to a set.

#### Beat Maker

TODO

#### Binary Sequencer

TODO

#### CC

TODO

#### Chord Sequencer

TODO

#### Droplets

TODO

#### Drum Deviator

TODO

#### Drum Machine

TODO

#### Elaborator

TODO

#### Euclidean Generator

TODO

#### Keyboard

TODO

#### LFO

TODO

#### Marbles

TODO

#### Octopus

TODO

#### Sequencer

TODO

#### Transformer

TODO



### Changelog/releases
