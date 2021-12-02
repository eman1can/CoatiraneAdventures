from copy import copy
from math import floor

from kivy.properties import BooleanProperty, Clock, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty

from game.crafting_queue import DISPLAY_COUNT, WORKING_SLOT_COUNT
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from game.crafting_recipe import ALLOY, EQUIPMENT, ITEM, PROCESS
from loading.kv_loader import load_kv
from refs import Refs
from uix.modules.spine_display import SpineDisplay
from uix.screens.header_screen import HeaderScreen

load_kv(__name__)


class CraftingMain(HeaderScreen, SpineDisplay):
    header = StringProperty('')
    page_data = ListProperty([])
    recipes_visible = BooleanProperty(False)
    crafting_visible = BooleanProperty(False)
    equipment_visible = BooleanProperty(False)

    def __init__(self, **kwargs):
        self._recipes = None
        self._displayed_recipe = None
        self._calculated_recipe = None
        self._displayed_panel = None
        self._queue_items = []
        super().__init__(**kwargs)

        self._displays = [CraftingItemDisplay() for _ in range(DISPLAY_COUNT)]

        self.headers = {
            'process_materials': 'What type of finished material would you like to make?',
            'craft_materials':   'What kind of materials would you link to make?',
            'craft_items':       'What type of item would you like to make?',
            'craft_equipment':   'What type of equipment would you like to make?',
            'craft_potions':     'What type of potion would you like to make?'
        }

        self.recipe_lists = {
            'process_materials': Refs.gc.get_process_recipes,
            'craft_materials':   Refs.gc.get_alloy_recipes,
            'craft_items':       Refs.gc.get_item_recipes,
            'craft_equipment':   Refs.gc.get_equipment_recipes,
            'craft_potions':     Refs.gc.get_potion_recipes
        }

        self.display_none()
        self.display()

    def on_enter(self):
        frame_rate = 30
        Clock.schedule_interval(self.ids.spine_display.update, 1 / frame_rate)
        self.show_crafting_queue()

    def on_leave(self):
        Clock.unschedule(self.ids.spine_display.update)
        self.hide_crafting_queue()

    def reload(self, **kwargs):
        # Go back to hidden version with only headers
        self.display_none()
        self.display()

    def display_none(self):
        self.header = 'What kind of crafting would you like to do?'
        self._recipes = None
        self.recipes_visible = False
        if self.crafting_visible or self.equipment_visible:
            self._displayed_recipe = None
            self._displayed_panel = None
            self.crafting_visible = False
            self.equipment_visible = False

    def on_height(self, *args):
        if 'view' not in self.ids:
            return
        for child in self.ids.view.children:
            if isinstance(child, CraftingDisplay):
                child.height = self.height * 0.104
            else:
                child.main_height = self.height * 0.0868
                child.sub_height = child.main_height * 0.5 * len(child.ingredients)
                child.ingredient_height = child.main_height * 0.5

    def display(self):
        self.ids.view.clear_widgets()
        process_materials = CraftingDisplay()
        process_materials.id = 'process_materials'
        process_materials.text = 'Process Materials'
        process_materials.image_source = 'items/cotton_cloth.png'
        process_materials.locked = not Refs.gc.has_perk('basic_tailor') and not Refs.gc.has_perk('apprentice_blacksmith')
        process_materials.callback = self.display_recipe_list

        craft_materials = CraftingDisplay()
        craft_materials.id = 'craft_materials'
        craft_materials.text = 'Craft Materials'
        craft_materials.image_source = 'items/tin/ingot.png'
        craft_materials.locked = not Refs.gc.has_perk('basic_tailor') and not Refs.gc.has_perk('apprentice_blacksmith')
        craft_materials.callback = self.display_recipe_list

        craft_items = CraftingDisplay()
        craft_items.id = 'craft_items'
        craft_items.text = 'Craft Items'
        craft_items.image_source = 'items/tin/ingot.png'
        craft_items.locked = not Refs.gc.has_perk('daedalus_protege')
        craft_items.callback = self.display_recipe_list

        craft_equipment = CraftingDisplay()
        craft_equipment.id = 'craft_equipment'
        craft_equipment.text = 'Craft Equipment'
        craft_equipment.image_source = 'items/equipment.png'
        craft_equipment.locked = not Refs.gc.has_perk('reputable_tailor') and not Refs.gc.has_perk('skilled_blacksmith')
        craft_equipment.callback = self.display_recipe_list

        craft_potions = CraftingDisplay()
        craft_potions.id = 'craft_potions'
        craft_potions.text = 'Craft Potions'
        craft_potions.image_source = 'items/potion.png'
        craft_potions.locked = True,  # not Refs.gc.has_perk('fledgling_alchemist'),
        craft_potions.callback = self.display_recipe_list

        base_display = [
            process_materials,
            craft_materials,
            craft_items,
            craft_equipment,
            craft_potions
        ]

        for display in base_display:
            display.size_hint = 1, None
            display.height = self.height * 0.104
            self.ids.view.add_widget(display)

    def display_recipe_list(self, display):
        index = self.ids.view.children.index(display)
        if display.recipes_shown:
            self.hide_recipes(index, display.recipe_count)
        else:
            self._recipes = self.recipe_lists[display.id]()
            display.recipe_count = len(self._recipes)
            self.display_recipes(index)
        display.recipes_shown = not display.recipes_shown

    def display_recipes(self, index):
        for recipe in self._recipes:
            if recipe.get_type() in (ITEM, PROCESS, ALLOY):
                item = Refs.gc.get_item_data(recipe.get_output_id())
                inventory_string = f'{Refs.gc.get_inventory().get_item_count(item.get_id())} in inventory'
                child = CraftingRecipeDisplay(
                    item_id=item.get_id(),
                    mode='item',
                    text=item.get_name(),
                    sub_text=item.get_description(),
                    count=f'x{recipe.get_item_count()}',
                    image_source=item.get_image(),
                    inventory=inventory_string,
                    button_disabled=not Refs.gc.has_perk(recipe.get_perk_requirement()),
                    callback=lambda display=recipe: self.display_recipe(display)
                )

                ingredients = []
                inventory = Refs.gc.get_inventory()
                for ingredient_id, count in recipe.get_ingredients().items():
                    ingredient = Refs.gc.get_item_data(ingredient_id)
                    if ingredient is None:
                        print(f'Can\'t find {ingredient_id}')
                    have_count = inventory.get_item_count(ingredient.get_id())
                    sub_data = {
                        'id':                ingredient_id,
                        'text':              ingredient.get_name(),
                        'image_source':      ingredient.get_image(),
                        'background_source': 'crafting_ingredient_middle.png',
                        'count':             f'x{count} - Have: {have_count}'
                    }
                    ingredients.append(sub_data)
                if len(ingredients) > 0:
                    ingredients[-1]['background_source'] = 'crafting_ingredient_bottom.png'
                child.ingredients = ingredients

                child.main_height = self.height * 0.0868
                child.sub_height = child.main_height * 0.5 * len(child.ingredients)
                child.ingredient_height = child.main_height * 0.5

            elif recipe.get_type() == EQUIPMENT:
                item = Refs.gc.get_equipment_data(recipe.get_output_id())
                child = CraftingRecipeDisplay(
                    item_id=item.get_id(),
                    mode='equipment',
                    text=item.get_name(),
                    sub_text=item.get_description(),
                    count=f'x{recipe.get_item_count()}',
                    image_source=item.get_image(),
                    button_disabled=not (Refs.gc.has_perk('reputable_tailor') or Refs.gc.has_perk('skilled_blacksmith')),
                    callback=lambda display=recipe: self.display_recipe(display)
                )
                ingredients = []
                inventory = Refs.gc.get_inventory()
                for ingredient_id, count in recipe.get_ingredients().items():
                    sub_data = self.format_equipment_material(None, inventory, ingredient_id, count)
                    ingredients.append(sub_data)

                if len(ingredients) > 0:
                    ingredients[-1]['background_source'] = 'crafting_ingredient_bottom.png'
                child.ingredients = ingredients

                child.main_height = self.height * 0.0868
                child.sub_height = child.main_height * 0.5 * len(child.ingredients)
                child.ingredient_height = child.main_height * 0.5
            else:
                raise Exception('Invalid recipe type!')
            self.ids.view.add_widget(child, index)

    def hide_recipes(self, index, count):
        self.crafting_visible = False
        self._displayed_recipe = None
        children = self.ids.view.children[index - count:index]
        for child in children:
            self.ids.view.remove_widget(child)

    def format_equipment_material(self, panel, inventory, ingredient_id, needed_count):
        if '/' in ingredient_id:
            ingredient_type, modifier = ingredient_id.split('/')
        else:
            ingredient_type, modifier = ingredient_id, ''
        sub_data = {
            'id':                '',
            'text':              'X Material',
            'background_source': 'icons/invisible.png',
            'cost':              needed_count,
            'count':             f'x{needed_count}'
        }
        if ingredient_type == 'wood':
            for wood in Refs.gc.get_wood_materials():
                wood_count = inventory.get_item_count(wood.get_processed_id())
                if wood_count < 0:
                    continue
                # max_craft = min(max_craft, wood_count / needed_count)
            sub_data['text'] = 'Wood Material'
            sub_data['id'] = 'wood'
            if panel is not None:
                panel.ids.modification_buttons.add_widget(Button(text='Choose Wood Material'))
        elif ingredient_type == 'soft':
            for soft in Refs.gc.get_soft_materials():
                soft_count = inventory.get_item_count(soft.get_processed_id())
                if soft_count < 0:
                    continue
                # max_craft = min(max_craft, soft_count / needed_count)
            sub_data['text'] = 'Soft Material'
            sub_data['id'] = 'soft'
            if panel is not None:
                panel.ids.modification_buttons.add_widget(Button(text='Choose Soft Material'))
        elif ingredient_type == 'hard':
            for hard in Refs.gc.get_hard_materials():
                hard_count = inventory.get_item_count(hard.get_processed_id())
                if hard_count < 0:
                    continue
                # max_craft = min(max_craft, hard_count / needed_count)
            sub_data['text'] = 'Hard Material'
            sub_data['id'] = 'hard'
            if panel is not None:
                panel.ids.modification_buttons.add_widget(Button(text='Choose Hard Material'))
        elif ingredient_type == 'gem':
            for gem in Refs.gc.get_gem_materials():
                gem_count = inventory.get_item_count(gem.get_processed_id())
                if gem_count < 0:
                    continue
                # max_craft = min(max_craft, gem_count / needed_count)
            sub_data['text'] = 'Gem Material'
            sub_data['id'] = 'gem'
            if panel is not None:
                panel.ids.modification_buttons.add_widget(Button(text='Choose Gem Material'))
        else:
            ingredient = Refs.gc.get_item_data(ingredient_type)
            have_count = inventory.get_item_count(ingredient.get_id())
            # max_craft = min(max_craft, floor(have_count / needed_count))
            sub_data = {
                'text':              ingredient.get_name(),
                'image_source':      ingredient.get_image(),
                'background_source': 'icons/invisible.png',
                'cost':              needed_count,
                'have':              have_count,
                'count':             f'x{needed_count} - Have: {have_count}'
            }
        if modifier == 'defining':
            sub_data['text'] += ' (Defining)'
        elif modifier == 'secondary':
            sub_data['text'] += ' (Secondary)'
        return sub_data

    def display_recipe(self, recipe):
        if self._displayed_recipe == recipe:
            self.crafting_visible = False
            self.equipment_visible = False
            self._displayed_recipe = None
            return

        self._displayed_recipe = recipe
        if self._calculated_recipe != recipe:
            inventory = Refs.gc.get_inventory()
            self._calculated_recipe = recipe

            if recipe.get_type() == EQUIPMENT:
                self._displayed_panel = panel = self.ids.equipment_panel
                self.equipment_visible = True
                panel.set_recipe(self, recipe)

                item = Refs.gc.get_equipment_data(recipe.get_output_id())
                panel.item_id = item.get_id()
                panel.item_name = item.get_name()
                panel.item_description = item.get_description()
                panel.image_source = item.get_image()
                
                panel.ids.modification_buttons.clear_widgets()
                
                ingredient_types = recipe.get_ingredients()
                ingredients = []
                for ingredient_type, needed_count in ingredient_types.items():
                    sub_data = self.format_equipment_material(panel, inventory, ingredient_type, needed_count)
                    ingredients.append(sub_data)
                panel.set_ingredients(ingredients)
                
                
            else:
                self._displayed_panel = panel = self.ids.crafting_panel
                self.crafting_visible = True
                panel.set_recipe(self, recipe)

                item = Refs.gc.get_item_data(recipe.get_output_id())
                have_count = inventory.get_item_count(item.get_id())

                panel.item_id = item.get_id()
                panel.item_name = item.get_name()
                panel.item_description = item.get_description()
                panel.image_source = item.get_image()
                panel.in_inventory = have_count

                ingredients = []
                max_craft = 50
                for ingredient_id, count in recipe.get_ingredients().items():
                    ingredient = Refs.gc.get_item_data(ingredient_id)
                    have_count = inventory.get_item_count(ingredient.get_id())
                    max_craft = int(min(max_craft, floor(have_count / count)))
                    sub_data = {
                        'text':              ingredient.get_name(),
                        'image_source':      ingredient.get_image(),
                        'background_source': 'icons/invisible.png',
                        'cost':              count,
                        'have':              have_count,
                        'count':             f'x{count} - Have: {have_count}'
                    }
                    ingredients.append(sub_data)
                panel.set_ingredients(ingredients)

                count_adjuster = panel.ids.count_adjuster
                count_adjuster.max = max_craft
                minimum = min(max_craft, 1)
                count_adjuster.min = minimum
                count_adjuster.set_value(minimum)

    def show_crafting_queue(self):
        Refs.gc.attach_crafting_queue_display(self.ids.crafting_queue, copy(self._displays))

    def hide_crafting_queue(self):
        Refs.gc.detach_crafting_queue_display()

    def update_item_info(self, instance, item_id, new_count):
        # Update the current crafting panel
        panel = self.ids.crafting_panel
        if panel.item_id == item_id:
            panel.in_inventory = new_count
        # Update the list of recipes
        for display in self.ids.view.children:
            if isinstance(display, CraftingRecipeDisplay) and display.item_id == item_id:
                display.inventory = f'{new_count} in inventory'

    def update_recipes(self):
        inventory = Refs.gc.get_inventory()
        for display in self.ids.view.children:
            if isinstance(display, CraftingRecipeDisplay):
                for ingredient in display.ingredients:
                    have_count = inventory.get_item_count(ingredient['id'])
                    ingredient['count'] = ingredient['count'].split('-')[0] + f'- Have: {have_count}'
                display.ids.ingredient_view.refresh_from_data()


class CraftingDisplay(RelativeLayout):
    id = StringProperty('')
    text = StringProperty('')
    image_source = StringProperty('')
    locked = BooleanProperty(True)
    recipes_shown = BooleanProperty(False)
    callback = ObjectProperty(None)

    def do_callback(self, *args):
        if self.callback is None:
            return
        self.callback(self)


class IngredientDisplay(RelativeLayout):
    id = StringProperty('')
    background_source = StringProperty('')
    text = StringProperty('')
    image_source = StringProperty('')
    count = StringProperty('')


class CraftingRecipeDisplay(RelativeLayout):
    item_id = StringProperty('')
    mode = OptionProperty('page', options=['page', 'item', 'equipment'])
    text = StringProperty('')
    sub_text = StringProperty('')
    count = StringProperty('')
    inventory = StringProperty('')
    image_source = StringProperty('')
    button_disabled = BooleanProperty(False)
    callback = ObjectProperty(None)
    ingredients = ListProperty([])

    main_height = NumericProperty(0)
    sub_height = NumericProperty(0)
    ingredient_height = NumericProperty(0)

    def do_callback(self, *args):
        if self.callback is None:
            return
        self.callback()


class CountAdjuster(RelativeLayout):
    min = NumericProperty(0)
    max = NumericProperty(0)

    def __init__(self, **kwargs):
        self.register_event_type('on_value')
        super().__init__(**kwargs)

    def on_value(self, value):
        pass

    def get_value(self):
        return self.ids.slider.value

    def set_value(self, value):
        self.ids.slider.value = value


class IngredientList(RelativeLayout):
    def __init__(self, **kwargs):
        self._ingredients = []
        super().__init__(**kwargs)

    def set_ingredients(self, ingredients):
        self._ingredients = ingredients
        self.ids.ingredient_view.data = self._ingredients
        self.ids.ingredient_view.refresh_from_data()

    def update_have(self, index, count):
        self._ingredients[index]['have'] = count
        self.ids.ingredient_view.data = self._ingredients
        self.ids.ingredient_view.refresh_from_data()

    def update_cost(self, count):
        for ingredient in self._ingredients:
            total_cost = count * ingredient['cost']
            ingredient['count'] = f'x{total_cost} - Have: {ingredient["have"]}'
        self.ids.ingredient_view.data = self._ingredients
        self.ids.ingredient_view.refresh_from_data()


class ItemCraftingPanel(RelativeLayout):
    item_id = StringProperty('')
    item_name = StringProperty('')
    item_description = StringProperty('')
    image_source = StringProperty('')
    in_inventory = NumericProperty(0)

    queue_time = NumericProperty(0)
    available_queue_time = NumericProperty(1000)
    cost = NumericProperty(0)
    have = NumericProperty(0)

    def __init__(self, **kwargs):
        self._recipe = None
        self._screen = None
        super().__init__(**kwargs)

    def set_recipe(self, screen, recipe):
        self._screen = screen
        self._recipe = recipe

    def set_ingredients(self, ingredients):
        self.ids.ingredient_list.set_ingredients(ingredients)

    def update_cost(self, count):
        self.ids.ingredient_list.update_cost(count)
        self.queue_time = count * self._recipe.get_crafting_time()

    def do_craft(self):
        # Add result to inventory and subtract cost
        # Update Panel Values
        count = self.ids.count_adjuster.get_value()
        output_id = self._recipe.get_output_id()
        inventory = Refs.gc.get_inventory()
        self.in_inventory = inventory.get_item_count(output_id)

        # Update ingredients and calculate new max_craft
        max_craft = 50
        for index, (ingredient_id, cost) in enumerate(self._recipe.get_ingredients().items()):
            inventory.remove_item(ingredient_id, count * cost)
            have_count = inventory.get_item_count(ingredient_id)
            max_craft = int(min(max_craft, floor(have_count / cost)))
            self.ids.ingredient_list.update_have(index, have_count)

        # Update count limits and vlaue
        self.ids.count_adjuster.max = max_craft
        minimum = min(max_craft, 1)
        self.ids.count_adjuster.min = minimum
        self.ids.count_adjuster.set_value(minimum)

        # Add the item to the queue
        crafting_time = self._recipe.get_crafting_time()
        crafting_type = self._recipe.get_crafting_type()
        Refs.gc.add_recipe_to_crafting_queue(output_id, crafting_type, crafting_time, count)

        # Update the recipes list with new values
        self._screen.update_recipes()


class EquipmentCraftingPanel(RelativeLayout):
    item_id = StringProperty('')
    item_name = StringProperty('')
    item_description = StringProperty('')
    image_source = StringProperty('')
    in_inventory = NumericProperty(0)

    queue_time = NumericProperty(0)
    available_queue_time = NumericProperty(1000)
    cost = NumericProperty(0)
    have = NumericProperty(0)

    def __init__(self, **kwargs):
        self._recipe = None
        self._screen = None
        super().__init__(**kwargs)

    def set_recipe(self, screen, recipe):
        self._screen = screen
        self._recipe = recipe

    def set_ingredients(self, ingredients):
        self.ids.ingredient_list.set_ingredients(ingredients)

    def update_cost(self, count):
        self.ids.ingredient_list.update_cost(count)
        self.queue_time = count * self._recipe.get_crafting_time()


class CraftingQueue(RelativeLayout):
    queue_time = NumericProperty(0)
    queue_count = NumericProperty(0)

    def __init__(self, **kwargs):
        self.register_event_type('on_item_crafted')
        super().__init__(**kwargs)

    def on_item_crafted(self, item_id, count):
        pass


class CraftingItemDisplay(RelativeLayout):
    image_source = StringProperty('items/empty.png')

    current_time = NumericProperty(0)
    time = NumericProperty(1)

    def __init__(self, **kwargs):
        self.images = [0 for _ in range(WORKING_SLOT_COUNT)]
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        for x in range(len(self.images)):
            self.images[x] = CharacterImage(opacity=0)
            self.ids.image_layout.add_widget(self.images[x])

    def on_height(self, *args):
        self.width = self.height


class CharacterImage(Image):
    def on_source(self, *args):
        if self.source == '':
            self.opacity = 0
        else:
            self.opacity = 1
