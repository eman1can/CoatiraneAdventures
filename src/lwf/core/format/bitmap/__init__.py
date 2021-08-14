__all__ = ('Bitmap', 'BitmapEx')

from .ex import BitmapEx


class Bitmap:
    def __init__(self, m_id=0, tf_id=0):
        self.matrix_id = m_id
        self.texture_fragment_id = tf_id

    def is_construct(self):
        return False

    def __str__(self):
        return f"BitmapFormat <Matrix Id: {self.matrix_id}, TF Id: {self.texture_fragment_id}>"
