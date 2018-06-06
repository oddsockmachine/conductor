#
# Cell number 0-15
# starting point: cell 0 = key at octave
# m21 = A0 , 1st note on piano
#
# scale = list of intervals from root note, of any size
scales = {
    "chromatic": [1,1,1,1,1,1,1,1,1,1,1,1],
    "major": [2,2,1,2,2,2,1],
    "pentatonic": [3,2,3,2,2],
}

def get_starting_note(octave, key):
    cell0 = 21 + (12 * octave) + ['a','a#','b','c','c#','d','d#','e','f','f#','g','g#'].index(key)
    return cell0

def get_full_scale(height, scale_name):
    scale = scales[scale_name]  # Get the scale intervals
    times = int(height/len(scale)) + 1  # How many times to repeat the intervals to fill up the grid height
    return (scale * times)[:height]  # Repeat the intervals, then trim to fit

def scale_to_offset(scale):
    accum = 0
    offsets = [0]
    for s in scale[:-1]:
        accum += s
        offsets.append(accum)
    return offsets

def create_cell_to_midi_note_lookup(scale, octave, key, height):
    starting_note = get_starting_note(octave, key)
    offset = scale_to_offset(get_full_scale(height, scale))
    notes = [x + starting_note for x in offset]
    # print(notes)
    lookup = {i: n for i,n in enumerate(notes)}
    return lookup


import unittest
class TestStringMethods(unittest.TestCase):

    def test_starting_note(self):
        self.assertEqual(get_starting_note(0, 'a'), 21)
        self.assertEqual(get_starting_note(0, 'a#'), 22)
        self.assertEqual(get_starting_note(0, 'b'), 23)
        self.assertEqual(get_starting_note(1, 'a'), 33)
        self.assertEqual(get_starting_note(2, 'a'), 45)
        self.assertEqual(get_starting_note(5, 'a'), 81)
        self.assertEqual(get_starting_note(5, 'd#'), 87)

    def test_full_scale(self):
        self.assertEqual(get_full_scale(16, "pentatonic"), [3, 2, 3, 2, 2, 3, 2, 3, 2, 2, 3, 2, 3, 2, 2, 3])
        self.assertEqual(get_full_scale(16, "major"), [2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2])
        self.assertEqual(get_full_scale(16, "chromatic"), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(len(get_full_scale(16, "pentatonic")), 16)
        self.assertEqual(len(get_full_scale(16, "major")), 16)
        self.assertEqual(len(get_full_scale(16, "chromatic")), 16)

    def test_scale_to_offset(self):
        self.assertEqual(scale_to_offset(get_full_scale(16, "chromatic")), [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
        self.assertEqual(scale_to_offset(get_full_scale(8, "chromatic")), [0,1,2,3,4,5,6,7])
        self.assertEqual(scale_to_offset(get_full_scale(8, "pentatonic")), [0,3,5,8,10,12,15,17])

    def test_lookup(self):
        self.assertEqual(create_cell_to_midi_note_lookup("pentatonic", 2, "b", 4), {0: 47, 1: 50, 2: 52, 3: 55})
        self.assertEqual(create_cell_to_midi_note_lookup("chromatic", 0, "a", 4), {0: 21, 1: 22, 2: 23, 3: 24})
if __name__ == '__main__':

    unittest.main()
