from timeit import Timer

from kivy.core.image import Image
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget


# from kivy.uix.image import Image

class Base(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        list = ['actresses_alexis_and_emilia', 'amatuer_model_calyse', 'architect_lexi', 'athlethic_sofi']
        options = ['_slide.png', '_preview.png', '_full.png']
        for res in list:
            for option in options:
                path = "../res/characters/test/" + res + "/" + res + option
                image = Image(path)
                with self.canvas:
                    Rectangle(size=(300, 300), pos=(0, 0), texture=image.texture)
                del image
        return


if __name__ == '__main__':
    t = Timer(lambda: Base())
    print(t.timeit(number=20000))