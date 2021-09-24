__all__ = ('Bitmap',)


class Bitmap:
    class Attribute:
        REPEAT_S = (1 << 0)
        REPEAT_T = (1 << 1)

    def __init__(self, m_id=0, tf_id=0):
        self.matrix_id = m_id
        self.texture_fragment_id = tf_id
        self.attribute = 0
        self.u = 0.0
        self.v = 0.0
        self.w = 0.0
        self.h = 0.0

    def __str__(self):
        return f"Bitmap <Matrix Id: {self.matrix_id}, TfId: {self.texture_fragment_id}>"
