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

def get_cell_to_note_converter():
    pass


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


if __name__ == '__main__':
    import unittest

    unittest.main()
