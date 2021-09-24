from math import floor
from random import choices, randint, uniform

from game.effect import AppliedEffect, BLOCK_CHANCE, COUNTER, COUNTER_CHANCE, COUNTER_TYPES, CRITICAL_CHANCE, DARK_RESIST, DURATION, EARTH_RESIST, EFFECT_TYPES, EVADE_CHANCE, FIRE_RESIST, HEALTH_DOT, HEALTH_REGEN, HYBRID_RESIST, LIGHT_RESIST, \
    MAGICAL_RESIST, \
    MANA_DOT, \
    MANA_REGEN, NULL_ATK, NULL_HYB_ATK, NULL_MAG_ATK, NULL_PHY_ATK, PENETRATION_CHANCE, PHYSICAL_RESIST, SPECIFIC_TARGET, STAT, STATUS_EFFECT, STAT_TYPES, THUNDER_RESIST, WATER_RESIST, WIND_RESIST
from game.skill import AILMENT_CURE, ALLIES, ALLY, ATTACK, CAUSE_EFFECT, ELEMENTS, FOES, FOE, HEAL, MAGICAL, PHYSICAL, SELF, TEMP_BOOST_BY_TARGET
from refs import Refs


class TargetInfo:
    def __init__(self):
        self.effective_attack = 0
        self.defense = 0

        self.penetration = False
        self.critical = False
        self.block = False
        self.evade = False
        self.counter = False


class BattleData:
    def __init__(self, floor_data, adventurers, supporters, is_boss_fight=False):
        self._floor_data = floor_data
        self._enemies = None
        self._adventurers = adventurers
        self._supporters = supporters
        self._pre_battle_status = {}
        for adventurer in self._adventurers:
            self._pre_battle_status[adventurer.get_id() + '_health'] = round(adventurer.get_battle_health(), 0)
            self._pre_battle_status[adventurer.get_id() + '_mana'] = round(adventurer.get_battle_mana(), 0)

        self._turn = None
        self._state = None
        self._turn = 1
        self._log = '\n'
        self._boss_fight = is_boss_fight
        # self._special_amount = special_amount
        self._dropped_items = {}

    def get_battle_log(self):
        return self._log

    def clear_battle_log(self):
        self._log = ""

    def get_dropped_items(self):
        return self._dropped_items

    def set_dropped_items(self, items):
        self._dropped_items = items

    def get_pre_battle_status(self):
        return self._pre_battle_status

    def set_state(self, new_state):
        self._state = new_state

    def get_state(self):
        return self._state

    # def get_special_amount(self):
    #     return self._special_amount
    #
    # def get_special_count(self):
    #     return floor(self._special_amount / 5)

    def check_end(self):
        win = loss = True
        for entity in self._enemies:
            win &= entity.is_dead()
        for entity in self._adventurers:
            if entity is None:
                continue
            loss &= entity.is_dead()
        return win, loss

    def make_turn(self, targeted):
        animation_queue = []
        self._log += f'Turn {self._turn}\n'
        win = loss = False
        for entity in self._get_turn_order():
            if entity.is_character():
                entity.increase_special_amount(uniform(0.25, 1.25))
                target = targeted[entity]
            else:
                target = None
            for animation in self._process_move(entity, False, target):
                animation_queue.append(animation)
            # Check for win or loss
            win, loss = self.check_end()
            if loss or win:
                break
        self._turn += 1

        # Do HP Regen and MP Regen and DOT
        queues = [[], [], [], []]  # HP Regen, MP Regen, HP DOT, MP DOT
        for entity in self._get_alive_enemies() + self._get_alive_characters():
            health_regen = entity.get_total_boost(HEALTH_REGEN)
            if health_regen != 0:
                health_regen = min(entity.get_health() - entity.get_battle_health(), health_regen * entity.get_health())
                if health_regen > 0:
                    self._log += entity.get_name() + f' +{round(health_regen, 1)} health.\n'
                    queues[0].append({'entity': entity, 'type': 'health_rog', 'markers': {entity: [('health', health_regen)]}, 'targets': [entity]})
                    entity.decrease_health(-health_regen)
            mana_regen = entity.get_total_boost(MANA_REGEN)
            if mana_regen != 0:
                mana_regen = min(entity.get_mana() - entity.get_battle_mana(), mana_regen * entity.get_mana())
                if mana_regen > 0:
                    self._log += entity.get_name() + f' +{round(mana_regen, 1)} mana.\n'
                    queues[1].append({'entity': entity, 'type': 'mana_rog', 'markers': {entity: [('mana', mana_regen)]}, 'targets': [entity]})
                    entity.decrease_mana(-mana_regen)
            health_dot = entity.get_total_boost(HEALTH_DOT)
            if health_dot != 0:
                self._log += entity.get_name() + f' -{round(health_dot * entity.get_health(), 1)} health.\n'
                entity.decrease_health(health_dot * entity.get_health())
                queues[2].append({'entity': entity, 'type': 'health_dot', 'markers': {entity: [('dot', health_dot * entity.get_health())]}, 'targets': [entity]})
                Refs.gc.get_floor_data().increase_stat(entity.get_index(), 0, Refs.gc.get_random_stat_increase())
                Refs.gc.get_floor_data().increase_stat(entity.get_index(), 4, Refs.gc.get_random_stat_increase())
            mana_dot = entity.get_total_boost(MANA_DOT)
            if mana_dot != 0:
                self._log += entity.get_name() + f' -{round(mana_dot * entity.get_mana(), 1)} mana.\n'
                entity.decrease_mana(mana_dot * entity.get_mana())
                queues[3].append({'entity': entity, 'type': 'mana_dot', 'markers': {entity: [('dot', mana_dot * entity.get_mana())]}, 'targets': [entity]})
                Refs.gc.get_floor_data().increase_stat(entity.get_index(), 1, Refs.gc.get_random_stat_increase())
            # Update Conditions for afflictions
            Refs.log(f'Update status effects for {entity.get_name()}')
            animation_queue += entity.update_recurring_status_effect()
        for queue in queues:
            animation_queue += queue
        # Decrease effect counters
        for entity in self._get_alive_enemies() + self._get_alive_characters():
            animation_queue += entity.update_effects()

        if win:
            result = True
        elif loss:
            result = False
        else:
            result = None
        return result, animation_queue

    def progress_encounter(self):
        if self._state == 'start':
            self._state = 'battle'
            self._state = 'battle'
        elif self._state == 'battle':
            self._state = 'result'

    def set_enemies(self, enemies):
        self._enemies = enemies
        for enemy in enemies:
            self._log += f'{enemy.get_name()} entered the battle!\n'
        for character in self._adventurers:
            self._log += f'{character.get_name()} joined the battle!\n'
        for character in self._supporters:
            if character is not None:
                self._log += f'{character.get_name()} joined the battle!\n'
            # skill_level = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 4, 9: 4}[character.get_current_rank()]
            # self.use_support_ability(character, character.get_skill(skill_level))

    def use_support_ability(self, caller, ability):
        self._log += f'{caller.get_name()} used the support skill {ability.get_name()}!\n'
        animation_queue = []
        icons = {}
        for effect in ability.get_effects():
            if effect.get_target() == ALLIES:
                for entity in self._get_alive_characters():
                    animations, icon = self._apply_effects(caller, ability, effect, entity)
                    animation_queue += animations
                    if entity not in icons:
                        icons[entity] = []
                    icons[entity].append(icon)
            else:
                for entity in self._get_alive_enemies():
                    animations, icon = self._apply_effects(caller, ability, effect, entity)
                    animation_queue += animations
                    if entity not in icons:
                        icons[entity] = []
                    icons[entity].append(icon)
        return animation_queue, ability.get_effects(), icons

    def get_enemies(self):
        return self._enemies

    def get_alive_enemies(self):
        return self._get_alive_enemies()

    def get_characters(self):
        return self._adventurers

    def get_supporters(self):
        return self._supporters

    def _calculate_agility(self, entity):
        agility = entity.get_agility()
        modifier = entity.get_selected_skill().get_speed()
        percent_modifier = Refs.gc.get_random_attack_modifier()
        return agility * modifier * percent_modifier

    def _get_turn_order(self):
        turn_order = {}
        # Compile list based on agility DESC
        for enemy in self._get_alive_enemies():
            turn_order[self._calculate_agility(enemy)] = enemy
        for character in self._get_alive_characters():
            turn_order[self._calculate_agility(character)] = character

        entities = []
        for key in sorted(turn_order.keys(), reverse=True):
            entities.append(turn_order[key])

        return entities

    def _get_alive_characters(self):
        # Only return first four characters
        return [e for e in self._adventurers if e is not None and not e.is_dead()]

    def _get_replacement_character(self, replaced):
        index = self._adventurers.index(replaced)
        self._adventurers = self._floor_data.replace_character(self._adventurers, index)
        if self._adventurers[index] is not None:
            self._supporters[index] = self._adventurers[index].get_support()
        return self._adventurers[index], index

    def _get_alive_enemies(self):
        return [e for e in self._enemies if not e.is_dead()]

    def _get_targets(self, target_type, is_character):
        if is_character and target_type in [FOE, FOES] or not is_character and target_type in [ALLY, ALLIES]:
            targets = self._get_alive_enemies()
        else:
            targets = self._get_alive_characters()

        if target_type in [FOES, ALLIES]:
            return targets
        else:
            return choices(targets, k=1)

    def _get_damage(self, effective_attack, entity, target, skill):
        info = TargetInfo()
        random_modifier = Refs.gc.get_random_attack_modifier()
        element_modifier = target.element_modifier(skill.get_element())
        effective_attack *= element_modifier

        info.effective_attack = effective_attack * random_modifier
        info.defense = target.get_defense()

        markers = [None]
        info.critical = self._get_critical(info, entity, target)
        if info.critical:
            critical_modifier = Refs.gc.get_random_critical_modifier()
            info.effective_attack *= critical_modifier
            self._log += f'      Critical\n'
            markers.append('critical')
            if entity.is_character():
                self._floor_data.increase_stat(entity.get_index(), 5, Refs.gc.get_random_stat_increase() * 2)
                self._floor_data.increase_stat(entity.get_index(), 6, Refs.gc.get_random_stat_increase() * 2)
            if critical_modifier >= 3.5 and random_modifier >= 1.4:
                markers[0] = 'crit_damage'
        info.penetration = self._get_penetration(info, entity, target)
        if info.penetration:
            info.defense *= 0.15
            self._log += f'      Penetration\n'
            markers.append('penetration')
            if entity.is_character():
                self._floor_data.increase_stat(entity.get_index(), 2, Refs.gc.get_random_stat_increase() * 2)
        info.block = self._get_block(info, target)
        if info.block:
            info.effective_attack *= 0.5
            self._log += f'      Block\n'
            markers.append('block')
            if target.is_character():
                self._floor_data.increase_stat(target.get_index(), 4, Refs.gc.get_random_stat_increase() * 2)
        info.evade = self._get_evade(info, entity, target)
        if info.evade:
            info.effective_attack *= 0.15
            self._log += f'      Evade\n'
            markers.append('evade')
            if target.is_character():
                self._floor_data.increase_stat(target.get_index(), 5, Refs.gc.get_random_stat_increase() * 2)
                self._floor_data.increase_stat(target.get_index(), 6, Refs.gc.get_random_stat_increase() * 2)
        info.counter = self._get_counter(info, entity, target)
        if info.counter:
            markers.append('counter')
            if target.is_character():
                self._floor_data.increase_stat(target.get_index(), 5, Refs.gc.get_random_stat_increase() * 2)
                self._floor_data.increase_stat(target.get_index(), 6, Refs.gc.get_random_stat_increase() * 2)
        # return 1, info.counter, info.evade, markers
        return max(info.effective_attack - info.defense, 0), info.counter, info.evade, markers

    def _process_move(self, entity, counter=False, target=None):
        animation = {'entity': entity, 'is_counter': counter, 'markers': []}

        if entity.is_dead():
            return []
        if target is not None and target.is_dead():
            if counter:
                return []
            else:  # This will hit when a targeted enemy dies; Grab new target
                target = self._get_alive_enemies()[0]
        if counter:
            skill = entity.get_counter_skill()
            if skill is None:
                return []
            self._log += f'   {entity.get_name()} counters with {skill.get_name()}\n'
        else:
            skill = entity.get_selected_skill()
            self._log += f'   {entity.get_name()} used {skill.get_name()}\n'
        animation['skill'] = skill

        if skill.get_type() == ATTACK:
            animation['type'] = 'attack'
        elif skill.get_type() == CAUSE_EFFECT:
            animation['type'] = 'cause_effect'
        elif skill.get_type() == HEAL:
            animation['type'] = 'heal'
        else:
            animation['type'] = 'ailment_cure'

        animation['special'] = skill.is_special()
        if skill.is_special():
            entity.increase_special_amount(-5)
            # self._special_amount -= 5

        mana_cost = entity.get_mana_cost(skill)
        if mana_cost > 0:
            self._log += f'      -{mana_cost} Mana\n'
            entity.decrease_mana(mana_cost)
            animation['mana_cost'] = mana_cost
            if entity.is_character():
                self._floor_data.increase_stat(entity.get_index(), 1, Refs.gc.get_random_stat_increase())

        if skill.get_boosts() is not None:
            for boost in skill.get_boosts():
                boost_effect = AppliedEffect(TEMP_BOOST_BY_TARGET[boost.get_type()][skill.get_target()], 1)
                boost_effect.set_info(entity.get_name(), skill.get_name())
                entity.apply_effect(f'{entity.get_id()}_{skill.get_id()}', boost.get_stat_type(), boost_effect)

        # Get targets
        animations = []
        if skill.get_target() == FOE:
            if target is None:
                targets = self._get_targets(skill.get_target(), entity.is_character())
            else:
                targets = [target]
            if skill.get_type() == ATTACK:
                markers, animations, icons = self._process_attack(entity, skill, targets, counter)
            else:
                markers, animations, icons = self._process_cause_effect(entity, skill, targets, counter)
            animation['targets'] = targets
        elif skill.get_target() == FOES:
            targets = self._get_targets(skill.get_target(), entity.is_character())
            if skill.get_type() == ATTACK:
                markers, animations, icons = self._process_attack(entity, skill, targets, counter)
            else:
                markers, animations, icons = self._process_cause_effect(entity, skill, targets, counter)
            animation['targets'] = targets
        elif skill.get_target() in [ALLIES, ALLY]:
            targets = self._get_targets(skill.get_target(), entity.is_character())
            if skill.get_type() == CAUSE_EFFECT:
                markers, animations, icons = self._process_cause_effect(entity, skill, targets, True)
            elif skill.get_type() == HEAL:
                markers, icons = self._process_heal(entity, skill, targets)
            else:
                animations, markers, icons = self._process_ailment_cure(entity, skill, targets)
            animation['targets'] = targets
        else:
            if skill.get_type() == CAUSE_EFFECT:
                markers, animations, icons = self._process_cause_effect(entity, skill, [entity], True)
            elif skill.get_type() == HEAL:
                markers, icons = self._process_heal(entity, skill, [entity])
            else:
                animations, markers, icons = self._process_ailment_cure(entity, skill, [entity])
            animation['targets'] = [entity]
        animation['markers'] = markers
        animation['icons'] = icons
        return [animation] + animations

    def _process_attack(self, entity, skill, targets, counter):
        base_attack = entity.get_attack(skill.get_attack_type())
        skill_power = skill.get_power()
        effective_attack = base_attack * skill_power

        counters = []
        animations = []
        icons = []
        markers = {}
        for target in targets:
            damage, do_counter, evade, damage_markers = self._get_damage(effective_attack, entity, target, skill)

            attack_resist = 0
            if skill.get_attack_type() == PHYSICAL:
                attack_resist += target.get_total_boost(PHYSICAL_RESIST)
            elif skill.get_attack_type() == PHYSICAL:
                attack_resist += target.get_total_boost(MAGICAL_RESIST)
            else:
                attack_resist += target.get_total_boost(PHYSICAL_RESIST)
                attack_resist += target.get_total_boost(MAGICAL_RESIST)
                attack_resist += target.get_total_boost(HYBRID_RESIST)

            element_resists = [WATER_RESIST, FIRE_RESIST, THUNDER_RESIST, WIND_RESIST, EARTH_RESIST, LIGHT_RESIST, DARK_RESIST]
            element = list(ELEMENTS.keys()).index(skill.get_element())

            if damage > 0:
                if element > 0:
                    element_resist = element_resists[element - 1]
                    element_resist = target.get_total_boost(element_resist)
                else:
                    element_resist = 0

                if attack_resist > 0:
                    damage *= 1 - min(1, attack_resist)
                else:
                    damage *= 1 + -max(-1, attack_resist)

                if element_resist > 0:
                    damage_markers.append('resist')
                    damage *= 1 - min(1, element_resist)
                else:
                    damage_markers.append('weak')
                    damage *= 1 + -max(-1, element_resist)

            if round(damage, 0) > 0:
                null_damage = False
                attack_nulls = target.get_total_boost(NULL_ATK)
                if attack_nulls > 0:
                    target.reduce_effect_amount(NULL_ATK, 1)
                    null_damage = True
                if not null_damage:
                    attack_nulls = target.get_total_boost(NULL_HYB_ATK)
                    if attack_nulls > 0:
                        target.reduce_effect_amount(NULL_HYB_ATK, 1)
                        null_damage = True
                if not null_damage and skill.get_attack_type() == PHYSICAL:
                    attack_nulls = target.get_total_boost(NULL_PHY_ATK)
                    if attack_nulls > 0:
                        target.reduce_effect_amount(NULL_PHY_ATK, 1)
                        null_damage = True
                if not null_damage and skill.get_attack_type() == MAGICAL:
                    attack_nulls = target.get_total_boost(NULL_MAG_ATK)
                    if attack_nulls > 0:
                        target.reduce_effect_amount(NULL_MAG_ATK, 1)
                        null_damage = True
                if null_damage:
                    self._log += f'      Null {round(damage, 1)} Damage'
                    for marker in damage_markers[1:]:
                        if marker != 'counter':
                            damage_markers.remove(marker)
                    damage_markers.append('null')
                    damage = 0

            if damage_markers[0] is not None and damage_markers[0] == 'crit_damage':
                damage_markers[0] = ('crit_damage', damage)
            else:
                damage_markers[0] = ('damage', damage)

            if damage != 0:
                target.decrease_health(damage)
                if target.is_character():
                    self._floor_data.increase_stat(target.get_index(), 0, Refs.gc.get_random_stat_increase())
                    self._floor_data.increase_stat(target.get_index(), 4, Refs.gc.get_random_stat_increase())
                if entity.is_character():
                    if skill.get_attack_type() == PHYSICAL:
                        self._floor_data.increase_stat(entity.get_index(), 2, Refs.gc.get_random_stat_increase())
                    elif skill.get_attack_type() == MAGICAL:
                        self._floor_data.increase_stat(entity.get_index(), 3, Refs.gc.get_random_stat_increase())
                    else:
                        self._floor_data.increase_stat(entity.get_index(), 2, Refs.gc.get_random_stat_increase())
                        self._floor_data.increase_stat(entity.get_index(), 3, Refs.gc.get_random_stat_increase())
                self._log += f'      {round(damage, 1)} damage to {target.get_name()}\n'
            else:
                self._log += f'      No damage to {target.get_name()}\n'

            if target.is_dead():
                if target.is_character():
                    replace, hud_index = self._get_replacement_character(target)
                    if replace is not None:

                        if len(animations) > 0 and animations[-1]['type'] == 'enter_battle':
                            last_animation = animations[-1]
                            last_animation['entities'].append(target)
                            last_animation['targets'].append(replace)
                            last_animation['hud_index'] += '_' + str(hud_index)
                        else:
                            animations.append({'entity': None, 'entities': [target], 'type': 'enter_battle', 'targets': [replace], 'hud_index': str(hud_index)})
                    self._log += f'   {target.get_name()} has been incapacitated!\n'
                    hud_index = '_' + str(hud_index)
                else:
                    self._log += f'   {target.get_name()} has been killed!\n'
                    hud_index = ''

                damage_markers.append(f'death{hud_index}')
                if 'counter' in damage_markers:
                    damage_markers.remove('counter')
            else:
                if do_counter and not counter:
                    counters.append(lambda t=target: self._process_move(t, True, entity))
            markers[target] = damage_markers
            aqueue, eicons = self._process_effect(skill, entity, target, evade)
            animations += aqueue
            icons += eicons

        for counter in counters:
            animations += counter()
        return markers, animations, icons

    def _process_heal(self, entity, skill, targets):
        base_heal = entity.get_magical_attack()
        skill_power = skill.get_power()
        effective_heal = base_heal * skill_power

        markers = {}
        icons = []
        for target in targets:
            damage_markers = []
            random_modifier = Refs.gc.get_random_attack_modifier()

            target_effective_heal = min(effective_heal * random_modifier, target.get_health() - target.get_battle_health())
            self._log += f'      {round(target_effective_heal, 1)} heal to {target.get_name()}\n'
            target.decrease_health(-target_effective_heal)
            damage_markers.append(('health', target_effective_heal))
            if entity.is_character():
                self._floor_data.increase_stat(entity.get_index(), 3, Refs.gc.get_random_stat_increase())
            markers[target] = damage_markers
            animations, eicons = self._process_effect(skill, entity, target, False)
            icons += eicons
        return markers, icons

    def _process_ailment_cure(self, entity, skill, targets):
        aqueue = []
        markers = {}
        icons = []
        for target in targets:
            damage_markers = [None]
            if entity.is_character():
                self._floor_data.increase_stat(entity.get_index(), 3, Refs.gc.get_random_stat_increase())
            animations = target.clear_negative_effects()
            aqueue += animations
            markers[target] = damage_markers
            animations, eicons = self._process_effect(skill, entity, target, False)
            icons += eicons
        return aqueue, markers, icons

    def _process_cause_effect(self, entity, skill, targets, counter):
        counters = []
        icons = []
        markers = {}
        for target in targets:
            damage_markers = [None]
            info = TargetInfo()
            if entity.is_character() != target.is_character():
                info.evade = self._get_evade(info, entity, target)
                info.counter = self._get_counter(info, entity, target)
                if info.evade:
                    damage_markers.append('evade')
                if info.counter:
                    damage_markers.append('counter')

            if info.counter and not counter:
                if not target.is_dead():
                    counters.append(lambda t=target: self._process_move(t, True, entity))
            markers[target] = damage_markers

            animations, eicons = self._process_effect(skill, entity, target, info.evade)
            icons += eicons

        animation_queue = []
        for counter in counters:
            animation_queue += counter()
        return markers, animation_queue, icons

    def _process_effect(self, skill, entity, target, evade):
        animation_queue = []
        icons = []
        if skill.get_effects() and not evade:
            for effect in skill.get_effects():
                animations, icon = self._apply_effects(entity, skill, effect, target)
                animation_queue += animations
                icons.append(icon)
        return animation_queue, icons

    def _apply_effects(self, parent, ability, effect, target):
        effect_id = f'{parent.get_id()}_{ability.get_id()}'
        aeffect = None
        aqueue = []
        icon = None

        # Has an amount and a duration
        if effect.get_type() == STAT:
            aeffect = AppliedEffect(effect.get_amount(), effect.get_duration() + 1)
            icon = f"{effect.get_sub_type()}{'+' if effect.get_amount() > 0 else '-'}"
        # Has a counter of effective uses
        elif effect.get_type() == COUNTER:
            aeffect = AppliedEffect(effect.get_amount())
            icon = f"{effect.get_sub_type()}"
        # Has a duration
        elif effect.get_type() == DURATION:
            aeffect = AppliedEffect(0, effect.get_duration())
            icon = f"{effect.get_sub_type()}"
        elif effect.get_type() == SPECIFIC_TARGET:
            pass
        elif effect.get_type() == STATUS_EFFECT:
            if randint(0, 100) < effect.get_duration() * 100:
                aeffect = AppliedEffect(effect.get_amount())
                icon = f"{effect.get_sub_type()}"
                aqueue.append({'entity': target, 'type': 'set_status_effect', 'effect': effect.get_sub_type()})
        # Apply effect
        if aeffect is not None:
            aeffect.set_info(parent.get_name(), ability.get_name())
            target.apply_effect(effect_id, effect.get_sub_type(), aeffect)
        return aqueue, icon

    def _make_choice(self, chance):
        if chance == 0:
            return False
        return choices([True, False], [chance, 1 - chance])[0]

    def _get_penetration(self, info, entity, target):
        chance = min(0.85, (info.effective_attack / info.defense * 5 + entity.get_agility() / target.get_agility()) / 50)
        chance = min(1, max(chance + entity.get_total_boost(PENETRATION_CHANCE), 0))
        return self._make_choice(chance)

    def _get_critical(self, info, entity, target):
        chance = min(0.8, (entity.get_agility() / target.get_agility() + entity.get_dexterity() / target.get_dexterity()) / 5)
        chance = min(1, max(chance + entity.get_total_boost(CRITICAL_CHANCE), 0))
        return self._make_choice(chance)

    def _get_block(self, info, target):
        if info.penetration:
            return False
        chance = min(0.9, info.defense / info.effective_attack / 5)
        chance = min(1, max(chance + target.get_total_boost(BLOCK_CHANCE), 0))
        return self._make_choice(chance)

    def _get_evade(self, info, entity, target):
        if info.penetration or info.block:
            return False
        chance = min(0.6, (target.get_dexterity() / entity.get_dexterity() * 5 + target.get_agility() / entity.get_agility()) / 100)
        chance = min(1, max(chance + target.get_total_boost(EVADE_CHANCE), 0))
        return self._make_choice(chance)

    def _get_counter(self, info, entity, target):
        chance = min(0.8, (target.get_dexterity() / entity.get_dexterity() + target.get_agility() / entity.get_agility()) / 2)
        if info.block or info.evade:
            chance = max(chance * 1.5, 0.9)
        chance = min(1, max(chance + target.get_total_boost(COUNTER_CHANCE), 0))
        return self._make_choice(chance)
