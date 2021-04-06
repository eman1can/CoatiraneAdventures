from math import floor
from random import choices

from game.effect import AppliedEffect, BLOCK_CHANCE, COUNTER, COUNTER_CHANCE, COUNTER_TYPES, CRITICAL_CHANCE, DARK_RESIST, DURATION, EARTH_RESIST, EVADE_CHANCE, FIRE_RESIST, HEALTH_DOT, HEALTH_REGEN, HYBRID_RESIST, LIGHT_RESIST, MAGICAL_RESIST, \
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
    def __init__(self, adventurers, supporters, special_amount, is_boss_fight=False):
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
        self._special_amount = special_amount
        self._dropped_items = {}

    def get_battle_log(self):
        return self._log

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

    def get_special_amount(self):
        return self._special_amount

    def get_special_count(self):
        return floor(self._special_amount / 5)

    def check_end(self):
        win = loss = True
        for entity in self._enemies:
            win &= entity.is_dead()
        for entity in self._adventurers:
            loss &= entity.is_dead()
        return win, loss

    def make_turn(self):
        # print(f'Process Turn {self._turn}')
        self._log += f'Turn {self._turn}\n'
        win = loss = False
        for entity in self._get_turn_order():
            # print(f'\tMove of {entity.get_name()}')
            self._process_move(entity)
            # Check for win or loss
            win, loss = self.check_end()
            if loss or win:
                break
        self._turn += 1
        # Increase SA Gauge
        # print('Special gauge', self._special_amount, '→', self._special_amount+1)
        if self._special_amount < 25:
            self._special_amount += 1

        # Do HP Regen and MP Regen and DOT

        for entity in self._enemies + self._adventurers:
            if entity.is_dead():
                continue
            health_regen = entity.get_total_boost(HEALTH_REGEN)
            if health_regen != 0:
                health_regen = min(entity.get_health() - entity.get_battle_health(), health_regen * entity.get_health())
                if health_regen > 0:
                    self._log += entity.get_name() + f' +{round(health_regen, 1)} health.\n'
                    entity.decrease_health(-health_regen)
            mana_regen = entity.get_total_boost(MANA_REGEN)
            if mana_regen != 0:
                mana_regen = min(entity.get_mana() - entity.get_battle_mana(), mana_regen * entity.get_mana())
                if mana_regen > 0:
                    self._log += entity.get_name() + f' +{round(mana_regen, 1)} mana.\n'
                    entity.decrease_mana(-mana_regen)
            health_dot = entity.get_total_boost(HEALTH_DOT)
            if health_dot != 0:
                self._log += entity.get_name() + f' -{round(health_dot * entity.get_health(), 1)} health.\n'
                entity.decrease_health(health_dot * entity.get_health())
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 0, Refs.gc.get_random_stat_increase())
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 4, Refs.gc.get_random_stat_increase())
            mana_dot = entity.get_total_boost(MANA_DOT)
            if mana_dot != 0:
                self._log += entity.get_name() + f' -{round(mana_dot * entity.get_mana(), 1)} mana.\n'
                entity.decrease_mana(mana_dot * entity.get_mana())
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 1, Refs.gc.get_random_stat_increase())

        # Decrease effect counters
        for entity in self._enemies + self._adventurers:
            entity.update_effects()

        if win:
            return True
        elif loss:
            return False
        else:
            return None

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
            self._log += f'{character.get_name()} joined the battle!\n'
            skill_level = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 4, 9: 4}[character.get_current_rank()]
            self.use_support_ability(character, character.get_skill(skill_level))

    def use_support_ability(self, caller, ability):
        self._log += f'{caller.get_name()} used the support skill {ability.get_name()}!\n'
        name = f'{caller.get_name()}_{ability.get_name()}'
        for entity in self._adventurers:
            for effect in ability.get_effects():
                self._apply_effects(name, effect, entity)

    def get_enemies(self):
        return self._enemies

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
        for enemy in self._enemies:
            if enemy.is_dead():
                continue
            turn_order[self._calculate_agility(enemy)] = enemy
        for character in self._adventurers:
            if character.is_dead():
                continue
            turn_order[self._calculate_agility(character)] = character

        entities = []
        for key in sorted(turn_order.keys(), reverse=True):
            entities.append(turn_order[key])

        return entities

    def _get_targets(self, target_type, is_character):
        targets = []
        if is_character and target_type in [FOE, FOES] or not is_character and target_type in [ALLY, ALLIES]:
            for entity in self._enemies:
                if not entity.is_dead():
                    targets.append(entity)
        else:
            for entity in self._adventurers:
                if not entity.is_dead():
                    targets.append(entity)

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

        info.critical = self._get_critical(info, entity, target)
        if info.critical:
            info.effective_attack *= Refs.gc.get_random_critical_modifier()
            self._log += f'      Critical\n'
            if entity.is_character():
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 5, Refs.gc.get_random_stat_increase() * 2)
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 6, Refs.gc.get_random_stat_increase() * 2)
        info.penetration = self._get_penetration(info, entity, target)
        if info.penetration:
            info.defense *= 0.15
            self._log += f'      Penetration\n'
            if entity.is_character():
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 2, Refs.gc.get_random_stat_increase() * 2)
        info.block = self._get_block(info, target)
        if info.block:
            info.effective_attack *= 0.5
            self._log += f'      Block\n'
            if target.is_character():
                Refs.gc.get_floor_data().increase_stat(target.get_id(), 4, Refs.gc.get_random_stat_increase() * 2)
        info.evade = self._get_evade(info, entity, target)
        if info.evade:
            info.effective_attack *= 0.15
            self._log += f'      Evade\n'
            if target.is_character():
                Refs.gc.get_floor_data().increase_stat(target.get_id(), 5, Refs.gc.get_random_stat_increase() * 2)
                Refs.gc.get_floor_data().increase_stat(target.get_id(), 6, Refs.gc.get_random_stat_increase() * 2)
        info.counter = self._get_counter(info, entity, target)
        if info.counter:
            if target.is_character():
                Refs.gc.get_floor_data().increase_stat(target.get_id(), 5, Refs.gc.get_random_stat_increase() * 2)
                Refs.gc.get_floor_data().increase_stat(target.get_id(), 6, Refs.gc.get_random_stat_increase() * 2)
        return max(info.effective_attack - info.defense, 0), info.counter, info.evade

    def _process_move(self, entity, counter=False):
        if entity.is_dead():
            return
        if counter:
            skill = entity.get_counter_skill()
            if skill is None:
                return
            # print(f'\t\tCounter with {skill.get_name()}')
            self._log += f'   {entity.get_name()} counters with {skill.get_name()}\n'
        else:
            skill = entity.get_selected_skill()
            # print(f'\t\tUses {skill.get_name()} ({TARGETS[skill.get_target()]})')
            self._log += f'   {entity.get_name()} used {skill.get_name()}\n'

        if skill.is_special():
            self._special_amount -= 5
            # print('\t\t\tSpecial Gauge -5')

        mana_cost = entity.get_mana_cost(skill)
        if mana_cost > 0:
            self._log += f'      -{mana_cost} Mana\n'
            entity.decrease_mana(mana_cost)
            if entity.is_character():
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 1, Refs.gc.get_random_stat_increase())

        if skill.get_boosts() is not None:
            for boost in skill.get_boosts():
                effect_name = f'{entity.get_name()}_{skill.get_name()}'
                boost_value = TEMP_BOOST_BY_TARGET[boost.get_type()][skill.get_target()]
                entity.apply_effect(effect_name, boost.get_stat_type(), AppliedEffect(boost_value, 1))

        # Get targets
        if skill.get_target() in [FOE, FOES]:
            targets = self._get_targets(skill.get_target(), entity.is_character())
            if skill.get_type() == ATTACK:
                self._process_attack(entity, skill, targets, counter)
            else:
                self._process_cause_effect(entity, skill, targets, counter)
        elif skill.get_target() in [ALLIES, ALLY]:
            targets = self._get_targets(skill.get_target(), entity.is_character())
            if skill.get_type() == CAUSE_EFFECT:
                self._process_cause_effect(entity, skill, targets, True)
            elif skill.get_type() == HEAL:
                self._process_heal(entity, skill, targets)
            elif skill.get_type() == AILMENT_CURE:
                self._process_ailment_cure(entity, skill, targets)
        else:
            if skill.get_type() == CAUSE_EFFECT:
                self._process_cause_effect(entity, skill, [entity], True)
            elif skill.get_type() == HEAL:
                self._process_heal(entity, skill, [entity])
            elif skill.get_type() == AILMENT_CURE:
                self._process_ailment_cure(entity, skill, [entity])

    def _process_attack(self, entity, skill, targets, counter):
        base_attack = entity.get_attack(skill.get_attack_type())
        skill_power = skill.get_power()
        effective_attack = base_attack * skill_power

        counters = []
        for target in targets:
            damage, do_counter, evade = self._get_damage(effective_attack, entity, target, skill)

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
                damage *= 1 - min(1, element_resist)
            else:
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
                    damage = 0

            if damage != 0:
                target.decrease_health(damage)
                if target.is_character():
                    Refs.gc.get_floor_data().increase_stat(target.get_id(), 0, Refs.gc.get_random_stat_increase())
                    Refs.gc.get_floor_data().increase_stat(target.get_id(), 4, Refs.gc.get_random_stat_increase())
                if entity.is_character():
                    if skill.get_attack_type() == PHYSICAL:
                        Refs.gc.get_floor_data().increase_stat(entity.get_id(), 2, Refs.gc.get_random_stat_increase())
                    elif skill.get_attack_type() == MAGICAL:
                        Refs.gc.get_floor_data().increase_stat(entity.get_id(), 3, Refs.gc.get_random_stat_increase())
                    else:
                        Refs.gc.get_floor_data().increase_stat(entity.get_id(), 2, Refs.gc.get_random_stat_increase())
                        Refs.gc.get_floor_data().increase_stat(entity.get_id(), 3, Refs.gc.get_random_stat_increase())
                self._log += f'      {round(damage, 1)} damage to {target.get_name()}\n'
            else:
                self._log += f'      No damage to {target.get_name()}\n'

            if target.is_dead():
                if target.is_character():
                    self._log += f'   {target.get_name()} has been incapacitated!\n'
                else:
                    self._log += f'   {target.get_name()} has been killed!\n'
            else:
                if do_counter and not counter:
                    counters.append(lambda t=target: self._process_move(t, True))
                if skill.get_effects() and not evade:
                    effect_name = f'{entity.get_name()}_{skill.get_name()}'
                    for effect in skill.get_effects():
                        if effect.get_target() == FOE:
                            self._apply_effects(effect_name, effect, target)
        self._process_effects(skill, entity)
        for counter in counters:
            counter()

    def _process_heal(self, entity, skill, targets):
        base_heal = entity.get_magical_attack()
        skill_power = skill.get_power()
        effective_heal = base_heal * skill_power

        for target in targets:
            random_modifier = Refs.gc.get_random_attack_modifier()

            target_effective_heal = min(effective_heal * random_modifier, target.get_health() - target.get_battle_health())
            self._log += f'      {round(target_effective_heal, 1)} heal to {target.get_name()}\n'
            target.decrease_health(-target_effective_heal)
            if entity.is_character():
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 3, Refs.gc.get_random_stat_increase())

            if skill.get_effects():
                effect_name = f'{entity.get_name()}_{skill.get_name()}'
                for effect in skill.get_effects():
                    if effect.get_target() == ALLY:
                        self._apply_effects(effect_name, effect, target)
        self._process_effects(skill, entity)

    def _process_ailment_cure(self, entity, skill, targets):
        for target in targets:
            if entity.is_character():
                Refs.gc.get_floor_data().increase_stat(entity.get_id(), 3, Refs.gc.get_random_stat_increase())
            target.clear_negative_effects()
            if skill.get_effects():
                effect_name = f'{entity.get_name()}_{skill.get_name()}'
                for effect in skill.get_effects():
                    if effect.get_target() == ALLY:
                        self._apply_effects(effect_name, effect, target)
        self._process_effects(skill, entity)

    def _process_cause_effect(self, entity, skill, targets, counter):
        counters = []
        for target in targets:
            info = TargetInfo()
            if entity.is_character() != target.is_character():
                info.evade = self._get_evade(info, entity, target)
                info.counter = self._get_counter(info, entity, target)

            if info.counter and not counter:
                if not target.is_dead():
                    counters.append(lambda t=target: self._process_move(t, True))
                    if skill.get_effects() and not info.evade:
                        effect_name = f'{entity.get_name()}_{skill.get_name()}'
                        for effect in skill.get_effects():
                            if effect.get_target() == FOE:
                                self._apply_effects(effect_name, effect, target)
        self._process_effects(skill, entity)
        for counter in counters:
            counter()

    def _process_effects(self, skill, entity):
        if skill.get_effects():
            name = f'{entity.get_id()}_{skill.get_name()}'
            for effect in skill.get_effects():
                if effect.get_target() == SELF:
                    self._apply_effects(name, effect, entity)
                elif effect.get_target() == ALLIES:
                    for target in self._get_targets(ALLIES, entity.is_character()):
                        self._apply_effects(name, effect, target)
                elif effect.get_target() == FOES:
                    for target in self._get_targets(FOES, entity.is_character()):
                        self._apply_effects(name, effect, target)
                else:
                    for target in self._get_targets(ALLY, False):
                        self._apply_effects(name, effect, target)

    def _apply_effects(self, name, effect, target):
        if effect.get_type() == STAT:
            self._log += f'    Apply {STAT_TYPES[effect.get_sub_type()]} ' + ('+' if effect.get_amount() > 0 else '') + f'{int(effect.get_amount() * 100)}% to {target.get_name()}\n'
            target.apply_effect(name, effect.get_sub_type(), AppliedEffect(effect.get_amount(), effect.get_duration() + 1))
        elif effect.get_type() == COUNTER:
            self._log += f'    Apply {COUNTER_TYPES[effect.get_sub_type()]}' + f'x{int(effect.get_amount())} to {target.get_name()}\n'
            target.apply_effect(name, effect.get_sub_type(), AppliedEffect(effect.get_amount()))
        elif effect.get_type() == DURATION:
            pass
        elif effect.get_type() == SPECIFIC_TARGET:
            pass
        elif effect.get_type() == STATUS_EFFECT:
            pass

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
