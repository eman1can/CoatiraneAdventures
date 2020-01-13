class MoveBarObject(FloatLayout):

    def __init__(self, **kwargs):
        super(MoveBarObject, self).__init__(**kwargs)
        self.visible = False
        self.opacity = 0
        self.size = 0, 0
        # for x in range(1):
        #     button = self.AtkBtn1
        #     button.size_hint = None, None
        #     button.text = '%s' % self.move1
        #     button.font_size = 40
        #     # button.color = self.color
        #     button.disabled = self.disabled
        #     button.background_color = .1, .1, .1, .2
        #     button.size = 175, 75
        #     button.disabled_color = 0, 0, 0, 0
        #     button.disabled_normal = ''
        #     button.disabled_background_color = 0, 0, 0, 0
        #     self.add_widget(button)

    def callback(self, text, movenum):
        if self.visible:
            # print(text)
            self.hide_widget()
            self.parent.text = text
            self.parent.parent.selectedMove = movenum
            # print(self.parent.parent.selectedMove)
            # print(self.parent.parent)
        else:
            print("not visible")

    def hide_widget(wid):
        # print(wid)
        if wid.visible:
            wid.size, wid.size_hint, wid.opacity = (0, 0), (0, 0), 0
            wid.visible = False
        else:
            wid.size, wid.size_hint, wid.opacity = (875, 75), (0, 0), 1
            wid.visible = True