class CharPreview(Image):
    health = NumericProperty(0)
    mp = NumericProperty(0)
    selectedMove = NumericProperty(0)

    move1 = ObjectProperty(None)
    move2 = ObjectProperty(None)
    move3 = ObjectProperty(None)
    move4 = ObjectProperty(None)
    special = ObjectProperty(None)
    move1name = StringProperty("")
    move2name = StringProperty("")
    move3name = StringProperty("")
    move4name = StringProperty("")
    specialname = StringProperty("")

    def __init__(self, char, pos):
        super(CharPreview, self).__init__()
        self.char = char
        # print(str(self.char.getmove(0)))
        self.move1 = self.char.getmove(0)
        self.move2 = self.char.getmove(1)
        self.move3 = self.char.getmove(2)
        self.move4 = self.char.getmove(3)
        self.special = self.char.getmove(4)
        self.source = self.char.getpreviewimage()
        self.size = 200, 200
        self.pos = pos
        self.size_hint = None, None
        self.allow_stretch = True
        self.keep_ratio = True
        with self.canvas:
            Color(1, 1, 1, .6)
            Rectangle(pos=self.pos, size=(200, 55))
        self.healthLabel = Label(text="[b]HP[/b]", font_size=24, markup=True, pos=(self.pos[0] + 10, self.pos[1] + 30),
                                 size=(20, 20),
                                 color=(0, 0, 0, 1), size_hint=(None, None))
        self.healthBar = ProgressBarCustom(1, (145, 20))
        self.healthBar.pos = self.pos[0] + 45, self.pos[1] + 30
        self.healthBar.max = self.char.totalHealth
        self.healthBar.value = self.health
        self.mpLabel = Label(text="[b]MP[/b]", font_size=24, markup=True, pos=(self.pos[0] + 10, self.pos[1] + 5),
                             size=(20, 20),
                             color=(0, 0, 0, 1), size_hint=(None, None))
        self.mpBar = ProgressBarCustom(2, (145, 20))
        self.mpBar.pos = self.pos[0] + 45, self.pos[1] + 5
        self.mpBar.max = self.char.totalMP
        self.mpBar.value = self.mp
        self.add_widget(self.healthBar)
        self.add_widget(self.healthLabel)
        self.add_widget(self.mpBar)
        self.add_widget(self.mpLabel)
        self.health = char.totalHealth
        self.mp = char.totalMP
        # self.add_widget(moveBar())

    def on_health(self, *args):
        self.healthBar.value = self.health

    def on_mp(self, *args):
        self.mpBar.value = self.mp

    def on_move1(self, *args):
        self.move1name = self.move1.getname()

    def on_move2(self, *args):
        self.move2name = self.move2.getname()

    def on_move3(self, *args):
        self.move3name = self.move3.getname()

    def on_move4(self, *args):
        self.move4name = self.move4.getname()

    def on_special(self, *args):
        self.specialname = self.special.getname()