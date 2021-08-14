__all__ = ('MovieClipEvent',)


LOAD = 1
UNLOAD = 2
ENTER_FRAME = 4

TO_STRING = {
    LOAD: 'Load',
    UNLOAD: 'Unload',
    ENTER_FRAME: 'Enter Frame'
}


class MovieClipEvent:
    def __init__(self):
        self.clip_event = 0
        self.animation_id = 0

    def __str__(self):
        if self.clip_event == LOAD:
            clip_event = 'Load'
        elif self.clip_event == UNLOAD:
            clip_event = 'Unload'
        else:
            clip_event = 'Enter Frame'
        return f"MovieClipEvent <Clip Event: {clip_event}, Animation Id: {self.animation_id}>"
