class HitListener(AnimationStateAdapter):
    def __init__(self):
        self.callback = None

    def set_callback(self, callback_function):
        self.callback = callback_function

    def event(self, trackIndex, event):
        print("event:", event.getData().getName().strip())
        if event.getData().getName().strip() == 'hit':
            if self.callback is not None:
                self.callback()


class BattleAnimation(Label):
    def on_touch_hover(self, touch):
        return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0

    def appear(self):
        self.opacity = 1

    def fade_out(self, duration):
        anim = Animation(opacity=0, duration=duration * 0.5)
        Clock.schedule_once(lambda dt: self.start_fading(anim, duration), duration * 0.5)

    def start_fading(self, anim, duration):
        anim.start(self)
        Clock.schedule_once(lambda dt: self.remove(), duration * 0.5)

    def remove(self):
        if self.parent is None:
            print("ERROR")
            return
        self.parent.remove_widget(self)


class NumberAnimation(BattleAnimation):
    def __init__(self, number, **kwargs):
        super().__init__(**kwargs)
        self.text = str(number)
        self.color = 1, 1, 1, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class BlockAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Block'
        self.color = 0.22, 0.22, 0.61, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class EvadeAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Evade'
        self.color = 0.45, 0.68, 0.68, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class CriticalAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Critical'
        self.color = 0.6, 0.22, 0.22, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class PenetrationAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Penetration'
        self.color = 0.56, 0.56, 0.56, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'


class CounterAnimation(BattleAnimation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Counter'
        self.color = 0.76, 0.43, 0.18, 1
        self.outline_color = 0, 0, 0, 1
        self.outline_width = 2
        self.font_name = 'Gabriola'