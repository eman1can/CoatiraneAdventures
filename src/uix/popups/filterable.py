# KV Import
from uix.popups.view import View

from loading.kv_loader import load_kv
load_kv(__name__)


class FilterPopup(View):
    def __init__(self, filter_callback, filter_edit_callback, **kwargs):
        self._filter_callback = filter_callback
        self._filter_edit_callback = filter_edit_callback
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        for rank in range(1, 11):
            layered_image = self.ids[f'rank_{rank}_stars']
            star_data = []
            if rank > 2:
                star_size = min(0.2827 / (rank - 1), 0.226)
                for star_index in range(0, rank):
                    star = {
                        'id':        f'star_{star_index}',
                        'source':    'icons/star.png',
                        'size_hint': (0.226, 0.6),
                        'pos_hint':  {'center_x': 0.4583 + star_size * star_index, 'center_y': 0.5}
                    }
                    star_data.append(star)
            elif rank == 2:
                star = {
                    'id':        f'star_{0}',
                    'source':    'icons/star.png',
                    'size_hint': (0.226, 0.6),
                    'pos_hint':  {'center_x': 0.528975, 'center_y': 0.5}
                }
                star_data.append(star)
                star = {
                    'id':        f'star_{1}',
                    'source':    'icons/star.png',
                    'size_hint': (0.226, 0.6),
                    'pos_hint':  {'center_x': 0.670325, 'center_y': 0.5}
                }
                star_data.append(star)
            elif rank == 1:
                star = {
                    'id':        f'star_{0}',
                    'source':    'icons/star.png',
                    'size_hint': (0.226, 0.6),
                    'pos_hint':  {'center_x': 0.59965, 'center_y': 0.5}
                }
                star_data.append(star)

            layered_image.data = star_data

    def modify_filtering(self, filter_type):
        if isinstance(filter_type, str):
            self._filter_edit_callback(f'type_{filter_type.lower()}')
        else:
            self._filter_edit_callback(f'rank_{filter_type}')

    def do_filtering(self):
        self._filter_callback()

    def size_override(self):
        return .75, .9
