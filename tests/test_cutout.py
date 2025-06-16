import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from stl_box_designer import BoxModel, CutoutPattern

class TestCutoutPattern(unittest.TestCase):
    def test_enable_disable(self):
        box = BoxModel()
        cp = CutoutPattern(box)
        self.assertFalse(cp.is_enabled())
        cp.enable()
        self.assertTrue(cp.is_enabled())
        cp.disable()
        self.assertFalse(cp.is_enabled())

if __name__ == '__main__':
    unittest.main()
