class CompartmentSystem:
    """Manages compartments inside a box model."""

    def __init__(self, box_model):
        self.box_model = box_model
        self.compartments = []  # list of (x, y, z, w, h, d)

    def add_compartment(self, x, y, z, width, depth, height):
        self.compartments.append((x, y, z, width, depth, height))

    def clear(self):
        self.compartments = []

    def list_compartments(self):
        return list(self.compartments)
