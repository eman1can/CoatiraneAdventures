__all__ = ('MovieClipEvent',)


class MovieClipEvent:
    LOAD = (1 << 0)
    UNLOAD = (1 << 1)
    ENTER_FRAME = (1 << 2)

    def __init__(self):
        self.clip_event = 0
        self.animation_id = 0

    def __str__(self):
        if self.clip_event == MovieClipEvent.LOAD:
            clip_event = 'Load'
        elif self.clip_event == MovieClipEvent.UNLOAD:
            clip_event = 'Unload'
        else:
            clip_event = 'Enter Frame'
        return f"MovieClipEvent <Clip Event: {clip_event}, Animation Id: {self.animation_id}>"
