class BoxModel:
    """Data model for a rectangular box."""

    def __init__(self, length=100, width=100, height=50):
        self.length = length
        self.width = width
        self.height = height

    def set_dimensions(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def get_dimensions(self):
        return self.length, self.width, self.height
