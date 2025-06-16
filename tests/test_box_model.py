import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from stl_box_designer import BoxModel

class TestBoxModel(unittest.TestCase):
    def test_dimensions(self):
        box = BoxModel()
        box.set_dimensions(10, 20, 30)
        self.assertEqual(box.get_dimensions(), (10, 20, 30))

if __name__ == '__main__':
    unittest.main()
