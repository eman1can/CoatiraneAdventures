from kivy.properties import BooleanProperty, ListProperty

from src.modules.KivyBase.Hoverable import ModalViewBase as ModalView


class Filterable(object):
    previews_filter = ListProperty(None)
    output = ListProperty(None)
    filter_types = ListProperty(['type_light', 'type_dark', 'type_earth', 'type_wind', 'type_thunder', 'type_fire', 'type_water',
                    'type_physical', 'type_magical', 'type_balanced', 'type_defensive', 'type_healing',
                    'rank_1', 'rank_2', 'rank_3', 'rank_4', 'rank_5', 'rank_6', 'rank_7', 'rank_8', 'rank_9', 'rank_10'])
    filters_applied = ListProperty(['type_light', 'type_dark', 'type_earth', 'type_wind', 'type_thunder', 'type_fire', 'type_water',
                    'type_physical', 'type_magical', 'type_balanced', 'type_defensive', 'type_healing',
                    'rank_1', 'rank_2', 'rank_3', 'rank_4', 'rank_5', 'rank_6', 'rank_7', 'rank_8', 'rank_9', 'rank_10'])
    no_filter = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_after_filter')
        super().__init__(**kwargs)
        self._filters_applied = self.filters_applied

    def filter(self):
        self.no_filter = True
        self.apply_filter()
        self.no_filter = False
        self.dispatch('on_after_filter')

    def apply_filter(self):
        stage1 = []
        for preview in self.previews_filter:
            if 'type_light' in self.filters_applied and preview['character'].get_element().lower() == 'light':
                stage1.append(preview)
            elif 'type_dark' in self.filters_applied and preview['character'].get_element().lower() == 'dark':
                stage1.append(preview)
            elif 'type_earth' in self.filters_applied and preview['character'].get_element().lower() == 'earth':
                stage1.append(preview)
            elif 'type_wind' in self.filters_applied and preview['character'].get_element().lower() == 'wind':
                stage1.append(preview)
            elif 'type_thunder' in self.filters_applied and preview['character'].get_element().lower() == 'thunder':
                stage1.append(preview)
            elif 'type_fire' in self.filters_applied and preview['character'].get_element().lower() == 'fire':
                stage1.append(preview)
            elif 'type_water' in self.filters_applied and preview['character'].get_element().lower() == 'water':
                stage1.append(preview)
        stage2 = []
        for preview in stage1:
            if 'type_magical' in self.filters_applied and preview['character'].get_type().lower() == 'magical':
                stage2.append(preview)
            elif 'type_physical' in self.filters_applied and preview['character'].get_type().lower() == 'physical':
                stage2.append(preview)
            elif 'type_balanced' in self.filters_applied and preview['character'].get_type().lower() == 'balanced':
                stage2.append(preview)
            elif 'type_defensive' in self.filters_applied and preview['character'].get_type().lower() == 'defensive':
                stage2.append(preview)
            elif 'type_healing' in self.filters_applied and preview['character'].get_type().lower() == 'healing':
                stage2.append(preview)
        output = []
        for preview in stage2:
            if 'rank_1' in self.filters_applied and preview['character'].get_current_rank() == 1:
                output.append(preview)
            elif 'rank_2' in self.filters_applied and preview['character'].get_current_rank() == 2:
                output.append(preview)
            elif 'rank_3' in self.filters_applied and preview['character'].get_current_rank() == 3:
                output.append(preview)
            elif 'rank_4' in self.filters_applied and preview['character'].get_current_rank() == 4:
                output.append(preview)
            elif 'rank_5' in self.filters_applied and preview['character'].get_current_rank() == 5:
                output.append(preview)
            elif 'rank_6' in self.filters_applied and preview['character'].get_current_rank() == 6:
                output.append(preview)
            elif 'rank_7' in self.filters_applied and preview['character'].get_current_rank() == 7:
                output.append(preview)
            elif 'rank_8' in self.filters_applied and preview['character'].get_current_rank() == 8:
                output.append(preview)
            elif 'rank_9' in self.filters_applied and preview['character'].get_current_rank() == 9:
                output.append(preview)
            elif 'rank_10' in self.filters_applied and preview['character'].get_current_rank() == 10:
                output.append(preview)
        self.output = output

    def on_previews(self, instance, preview):
        if self.no_filter:
            return
        self.filter()

    def on_filters_applied(self, instance, filters_applied):
        if filters_applied == self._filters_applied:
            return
        self._filters_applied = filters_applied
        self.filter()

    def on_after_filter(self):
        pass


class FilterWidget(ModalView):
    pass
