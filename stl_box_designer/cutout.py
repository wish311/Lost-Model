class CutoutPattern:
    """Represents a honeycomb cutout pattern."""

    def __init__(self, box_model, density=0.5):
        self.box_model = box_model
        self.density = density  # 0..1
        self.enabled = False

    def enable(self, density=None):
        self.enabled = True
        if density is not None:
            self.density = density

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled
