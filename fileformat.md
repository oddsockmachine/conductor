# Save File Format

"Sequencer" : {
  "Height": 16,
  "Width": 16,
  "Instruments": {
    "1": {
      "Octave": "1",
      "Key": "c",
      "Scale": "foo",
      "Pages": [
        {
          "Repeats": 2,
          "Grid": [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6]  # Columns saved as 16 bit representations
        },
        {
          "Repeats": 1,
          "Grid": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        },
        {
          "Repeats": 0,
          "Grid": []
        }
      ]
    },
    "2": {
      ...
    },
    "3": {
      ...
    }
  }
}
