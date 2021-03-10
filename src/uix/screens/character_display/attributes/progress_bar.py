# Kivy Imports
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class ProgressBar(Widget):
    value = NumericProperty(0)
    max = NumericProperty(100)

    def __init__(self, type, size, *args):
        super(ProgressBar, self).__init__()
        self.size = size
        self.isRainbow = False

        foreground = ''
        background = 'res/ProgressBarBackground.png'
        if type == 0:
            foreground = 'res/ProgressBarBlack.png'
        elif type == 1:
            foreground = 'res/ProgressBarRed.png'
        elif type == 2:
            foreground = 'res/ProgressBarBlue.png'
        elif type == 3:
            foreground = 'res/ProgressBarGreen.png'
        elif type == 4:
            foreground = 'res/ProgressBarPurple.png'
        elif type == 5:
            foreground = 'res/ProgressBarOrange.png'

        self.background = Image(source=background, size=self.size, pos=self.pos, keep_ratio=False, allow_stretch=True)
        self.maxValue = Label(text='%d' % self.max, pos=(self.pos[0] + self.width + 50, self.pos[1] + 10),
                              color=(0, 0, 0, 1), font_size=30)
        self.maxValue.size = self.maxValue.texture_size
        diff = 0
        if self.value > self.max:
            self.foreground.oldsource = self.foreground.source
            foreground = 'res/ProgressBarRainbow.png'
            diff = self.max
            self.isRainbow = True
        self.foreground = Image(source=foreground,
                                size=((self.width * ((self.value - diff) / self.max), self.height), self.height),
                                pos=self.pos, keep_ratio=False, allow_stretch=True)
        self.add_widget(self.background)
        self.add_widget(self.foreground)
        self.add_widget(self.maxValue)

    def on_value(self, *args):
        diff = 0
        if self.value > self.max:
            if not self.isRainbow:
                self.foreground.oldsource = self.foreground.source
                self.foreground.source = 'res/ProgressBarRainbow.png'
                diff = self.max
                if self.value > self.max * 2:
                    self.value = self.max * 2
                self.isRainbow = True
        else:
            if self.isRainbow:
                self.foreground.source = self.foreground.oldsource
                self.foreground.oldsource = ''
                self.isRainbow = False
        self.foreground.size = (self.width * ((self.value - diff) / self.max), self.height)

    def on_max(self, *args):
        self.maxValue.text = ('{:6}'.format('{:0.1f}'.format(self.max)))
        # self.maxValue.size = self.maxValue.texture_size
        # self.maxValue.pos = (self.pos[0] + self.width + 50, self.pos[1] + 10)

        diff = 0
        if self.value > self.max:
            if not self.isRainbow:
                self.foreground.oldsource = self.foreground.source
                self.foreground.source = 'res/ProgressBarRainbow.png'
                diff = self.max
                self.isRainbow = True
        else:
            if self.isRainbow:
                self.foreground.source = self.foreground.oldsource
                self.foreground.oldsource = ''
                self.isRainbow = False
        self.foreground.width = self.width * ((self.value - diff) / self.max)

    def on_pos(self, *args):
        self.foreground.pos = self.pos
        self.background.pos = self.pos
        self.maxValue.pos = (self.pos[0] + self.width + 50, self.pos[1] + 10)