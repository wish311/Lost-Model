class AutoSplitter:
    """Splits box models that exceed max dimensions."""

    def __init__(self, box_model, max_dim=256):
        self.box_model = box_model
        self.max_dim = max_dim
        self.parts = []

    def split(self):
        length, width, height = self.box_model.get_dimensions()
        self.parts = []
        if any(dim > self.max_dim for dim in (length, width, height)):
            # placeholder: simple half split along longest dimension
            if length >= width and length >= height:
                self.parts.append({'length': length/2, 'width': width, 'height': height})
                self.parts.append({'length': length/2, 'width': width, 'height': height})
            elif width >= length and width >= height:
                self.parts.append({'length': length, 'width': width/2, 'height': height})
                self.parts.append({'length': length, 'width': width/2, 'height': height})
            else:
                self.parts.append({'length': length, 'width': width, 'height': height/2})
                self.parts.append({'length': length, 'width': width, 'height': height/2})
        else:
            self.parts.append({'length': length, 'width': width, 'height': height})
        return self.parts
