import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from stl_box_designer import BoxModel, AutoSplitter

class TestAutoSplitter(unittest.TestCase):
    def test_split_needed(self):
        box = BoxModel(300, 100, 100)
        sp = AutoSplitter(box, max_dim=256)
        parts = sp.split()
        self.assertEqual(len(parts), 2)

    def test_no_split(self):
        box = BoxModel(200, 200, 200)
        sp = AutoSplitter(box, max_dim=256)
        parts = sp.split()
        self.assertEqual(len(parts), 1)

if __name__ == '__main__':
    unittest.main()
