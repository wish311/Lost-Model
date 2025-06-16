import os, sys; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from stl_box_designer import BoxModel, CompartmentSystem

class TestCompartmentSystem(unittest.TestCase):
    def test_add_compartment(self):
        box = BoxModel()
        cs = CompartmentSystem(box)
        cs.add_compartment(0, 0, 0, 10, 10, 10)
        self.assertEqual(len(cs.list_compartments()), 1)

if __name__ == '__main__':
    unittest.main()
