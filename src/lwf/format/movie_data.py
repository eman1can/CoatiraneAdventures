__all__ = ('Movie')


class Movie:
    def __init__(self):
        self.depths = 0
        self.label_offset = 0
        self.labels = 0
        self.frame_offset = 0
        self.frames = 0
        self.clip_event_id = 0
        self.clip_events = 0

    def __str__(self):
        return f"Movie <Depths: {self.depths}, Label Offset: {self.label_offset}, Labels: {self.labels}, Frame Offset: {self.frame_offset}, Frames: {self.frames}, Clip Event Id: {self.clip_event_id}, Clip Events: {self.clip_events}>"
