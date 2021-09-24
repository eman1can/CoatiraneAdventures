__all__ = ('TextProperty',)


class TextProperty:
    class Align:
        LEFT = 0
        RIGHT = 1
        CENTER = 2
        ALIGN_MASK = 0x3
        VERTICAL_BOTTOM = 4
        VERTICAL_MIDDLE = 8
        VERTICAL_MASK = 0xc

    def __init__(self):
        self.max_length = 0
        self.font_id = 0
        self.font_height = 0
        self.align = 0
        self.left_margin = 0
        self.right_margin = 0
        self.letter_spacing = 0.0
        self.leading = 0
        self.stroke_color_id = 0
        self.stroke_width = 0
        self.shadow_color_id = 0
        self.shadow_offset_x = 0
        self.shadow_offset_y = 0
        self.shadow_blur = 0

    def __str__(self):
        if self.align == TextProperty.Align.LEFT:
            align = 'left'
        elif self.align == TextProperty.Align.RIGHT:
            align = 'right'
        elif self.align == TextProperty.Align.CENTER:
            align = 'center'
        elif self.align == TextProperty.Align.VERTICAL_BOTTOM:
            align = 'vertical bottom'
        else:
            align = 'vertical middle'
        return f"Text Property <Max Length: {self.max_length}, Font Id: {self.font_id}, Font Height: {self.font_height}, Align: {align}, Left Margin: {self.left_margin}, Right Margin: {self.right_margin}, Letter Spacing: {self.letter_spacing}, Leading: {self.leading}, Stroke Color Id: {self.stroke_color_id}, Stroke Width: {self.stroke_width}," \
               f"Shadow Color Id: {self.shadow_color_id}, Shadow Offset X: {self.shadow_offset_x}, Shadow Offset Y: {self.shadow_offset_y}, Shadow Blur: {self.shadow_blur}>"
