# Kivy Imports
from kivy.properties import BooleanProperty, ListProperty

from kivy.uix.modalview import ModalView

RANK_FILTERS = ['rank_1', 'rank_2', 'rank_3', 'rank_4', 'rank_5', 'rank_6', 'rank_7', 'rank_8', 'rank_9', 'rank_10']
TYPE_FILTERS = ['type_physical', 'type_magical', 'type_hybrid', 'type_defensive', 'type_healing']
ELEMENT_FILTERS = ['type_light', 'type_dark', 'type_earth', 'type_wind', 'type_thunder', 'type_fire', 'type_water']


class Filterable(object):
    previews_filter = ListProperty(None)
    output = ListProperty(None)

    stage_1_filters = ListProperty(RANK_FILTERS)
    stage_2_filters = ListProperty(TYPE_FILTERS)
    stage_3_filters = ListProperty(ELEMENT_FILTERS)

    filter_types = ListProperty(TYPE_FILTERS + RANK_FILTERS + ELEMENT_FILTERS)

    filters_applied = ListProperty(TYPE_FILTERS + RANK_FILTERS + ELEMENT_FILTERS)
    _filters_applied = ListProperty([])

    stage_1_output = ListProperty([])
    stage_2_output = ListProperty([])
    stage_3_output = ListProperty([])

    no_filter = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_after_filter')
        super().__init__(**kwargs)

    def filter(self, filter_all=False):
        self.no_filter = True
        self.apply_filter(filter_all)
        self.no_filter = False
        self.dispatch('on_after_filter')

    def apply_filter(self, filter_all):

        self.output = self.previews_filter
        return

        if filter_all:
            self.output = []
            self.stage_1_output = []
            self.stage_2_output = []
            self.stage_3_output = []
            self._filters_applied = []
        filter_add = list(set(self.filters_applied) - set(self._filters_applied))
        filter_remove = list(set(self._filters_applied) - set(self.filters_applied))

        filter_1_add = list(set(filter_add) & set(self.stage_1_filters))
        filter_1_remove = list(set(filter_remove) & set(self.stage_1_filters))
        filter_2_add = list(set(filter_add) & set(self.stage_2_filters))
        filter_2_remove = list(set(filter_remove) & set(self.stage_2_filters))
        filter_3_add = list(set(filter_add) & set(self.stage_3_filters))
        filter_3_remove = list(set(filter_remove) & set(self.stage_3_filters))

        debug = False

        # Filter stage 1 - ranks
        if debug:
            print(f'Before step 1 filter - {len(self.previews_filter)} - {self.previews_filter}')
            print('Add', filter_1_add)
            print('Remove', filter_1_remove)

        # Previews not in stage 1 filter and in stage 1 output
        stage_1_remove = []
        if len(filter_1_remove) > 0:
            for preview in self.stage_1_output:
                if f"rank_{preview['character'].get_current_rank()}" in filter_1_remove:
                    stage_1_remove.append(preview)

        if debug:
            print(f'Stage 1 remove - {len(stage_1_remove)} - {stage_1_remove}')

        # Previews in stage 1 filter and not in stage 1 output
        stage_1_add = []
        if len(filter_1_add) > 0:
            # filter_2_add = list(set(self.filters_applied) & set(self.stage_2_filters))
            # self.stage_2_output = []
            for preview in self.previews_filter:
                if preview in self.stage_1_output:
                    continue
                if f"rank_{preview['character'].get_current_rank()}" in filter_1_add:
                    stage_1_add.append(preview)

        if debug:
            print(f'Stage 1 add - {len(stage_1_add)} - {stage_1_add}')

        # Remove previews
        for preview in stage_1_remove:
            self.stage_1_output.remove(preview)

        # Add previews
        for preview in stage_1_add:
            self.stage_1_output.append(preview)

        if debug:
            print(f'After stage 1 filter - {len(self.stage_1_output)} - {self.stage_1_output}')
            print('Add', filter_2_add)
            print('Remove', filter_2_remove)
        # Filter stage 2 - attack types

        # Previews not in stage 2 filter and in stage 2 output
        stage_2_remove = []
        if len(filter_2_remove) > 0:
            for preview in self.stage_2_output:
                if f"type_{preview['character'].get_attack_type_string().lower()}" in filter_2_remove:
                    stage_2_remove.append(preview)

        if debug:
            print(f'Stage 2 remove - {len(stage_2_remove)} - {stage_2_remove}')

        # Previews in stage 2 filter and not in stage 2 output
        stage_2_add = []
        if len(filter_2_add) > 0:
            # filter_3_add = list(set(self.filters_applied) & set(self.stage_3_filters))
            # self.stage_3_output = []
            for preview in self.stage_1_output:
                if preview in self.stage_2_output:
                    continue
                if f"type_{preview['character'].get_attack_type_string().lower()}" in filter_2_add:
                    stage_2_add.append(preview)

        if debug:
            print(f'Stage 2 add - {len(stage_2_add)} - {stage_2_add}')

        # Update stage 2 output
        for preview in stage_2_add:
            self.stage_2_output.append(preview)
        # for preview in filter_2_remove:
        #     self.stage_2_output.remove(preview)
        for preview in stage_2_remove:
            self.stage_2_output.remove(preview)

        if debug:
            print(f'After stage 2 filter - {len(self.stage_2_output)} - {self.stage_2_output}')
            print('Add', filter_3_add)
            print('Remove', filter_3_remove)

        # Filter Stage 3 - element types

        # Previews not in stage 3 filter and in stage 3 output
        stage_3_remove = []
        if len(filter_3_remove) > 0:
            for preview in self.stage_3_output:
                if f"type_{preview['character'].get_element_string().lower()}" in filter_3_remove:
                    stage_3_remove.append(preview)

        if debug:
            print(f'Stage 3 remove - {len(stage_3_remove)} - {stage_3_remove}')

        # Previews in stage 3 filter and not in stage 3 output
        stage_3_add = []
        if len(filter_3_add) > 0:
            for preview in self.stage_2_output:
                if preview in self.stage_3_output:
                    continue
                if f"type_{preview['character'].get_element_string().lower()}" in filter_3_add:
                    stage_3_add.append(preview)
        if debug:
            print(f'Stage 3 add - {len(stage_3_add)} - {stage_3_add}')

        for preview in stage_3_remove:
            self.stage_3_output.remove(preview)

        for preview in stage_3_add:
            self.stage_3_output.append(preview)
        # for preview in stage_1_remove:
        #     self.stage_3_output.remove(preview)
        # for preview in stage_2_remove:
        #     self.stage_3_output.remove(preview)

        if debug:
            print(f'After stage 3 filter - {len(self.stage_3_output)} - {self.stage_3_output}')

        self.output = self.stage_3_output
        self._filters_applied = self.filters_applied.copy()

    def on_previews_filter(self, instance, preview):
        if self.no_filter:
            return
        self.filter(True)

    def on_filters_applied(self, instance, filters_applied):
        if filters_applied == self._filters_applied:
            return
        if self.no_filter:
            return
        self.filter()

    def on_after_filter(self):
        pass


class FilterWidget(ModalView):
    pass
