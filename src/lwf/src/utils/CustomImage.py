
class CustomImage:
    src = None
    def __init__(self):
        self.source = ""
        self.onerror = None
        self.onload = None

    @src.setter
    def src(self, newSrc):
        self.source = newSrc
        self.load_image()

    def load_image(self):
        try:
            self.data = Image(source=self.source)
        except Exception:
            if self.onerror is not None:
                self.onerror()
        if self.onload is not None:
            self.onload()

