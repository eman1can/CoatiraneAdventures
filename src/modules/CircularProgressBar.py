from src.modules.KivyBase.Hoverable import WidgetBase as Widget
from kivy.properties import NumericProperty, OptionProperty, BoundedNumericProperty, ReferenceListProperty


class CircularProgressBar(Widget):
    thickness = BoundedNumericProperty(10, min=0)
    precision = BoundedNumericProperty(10, min=0)
    cap_style = OptionProperty('round', options=['round', 'none', 'square'])
    cap_precision = NumericProperty(100)

    pr = BoundedNumericProperty(1, min=0, max=1)
    pg = BoundedNumericProperty(0, min=0, max=1)
    pb = BoundedNumericProperty(0, min=0, max=1)
    pa = BoundedNumericProperty(1, min=0, max=1)
    progress_color = ReferenceListProperty(pr, pg, pb, pa)

    br = BoundedNumericProperty(0.46, min=0, max=1)
    bg = BoundedNumericProperty(0.46, min=0, max=1)
    bb = BoundedNumericProperty(0.46, min=0, max=1)
    ba = BoundedNumericProperty(1, min=0, max=1)
    background_color = ReferenceListProperty(br, bg, bb, ba)

    min = NumericProperty(0)
    max = NumericProperty(100)
    value = BoundedNumericProperty(0)

    draw_min = BoundedNumericProperty(0, min=0, max=359)
    draw_max = BoundedNumericProperty(360, min=1, max=360)
    rot_angle = BoundedNumericProperty(0, min=0, max=360)

    normalized_min = NumericProperty(0)
    normalized_max = NumericProperty(1)
    normalised_value = BoundedNumericProperty(0)
