from math import floor
from random import choices

from game.effect import AppliedEffect, COUNTER, DURATION, HEALTH_DOT, HEALTH_REGEN, MANA_DOT, MANA_REGEN, SPECIFIC_TARGET, STAT, STATUS_EFFECT, STAT_TYPES
from game.skill import AILMENT_CURE, ALLIES, ALLY, ATTACK, ATTACK_POWERS, CAUSE_EFFECT, FOES, FOE, HEAL, SELF, TARGETS, TEMP_BOOST_BY_TARGET
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
            self._pre_battle_status[adventurer.get_id() + '_health'] = adventurer.get_battle_health()
            self._pre_battle_status[adventurer.get_id() + '_mana'] = adventurer.get_battle_mana()

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
            for effect_type, effects in entity.get_effects().items():
                if effect_type == HEALTH_REGEN:
                    for applied_effect in effects:
                        health = applied_effect.get_amount() * entity.get_health()
                        entity.decrease_health(-health)
                elif effect_type == MANA_REGEN:
                    for applied_effect in effects:
                        mana = applied_effect.get_amount() * entity.get_mana()
                        entity.decrease_health(-mana)
                elif effect_type == HEALTH_DOT:
                    for applied_effect in effects:
                        health = applied_effect.get_amount() * entity.get_health()
                        entity.decrease_health(health)
                elif effect_type == MANA_DOT:
                    for applied_effect in effects:
                        mana = applied_effect.get_amount() * entity.get_mana()
                        entity.decrease_health(mana)
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
            # print(character.get_description_recap())
        for character in self._supporters:
            self._log += f'{character.get_name()} joined the battle!\n'
            # self.use_support_ability(character, character.get_skill(0))

    def use_support_ability(self, caller, ability):
        self._log += f'{caller.get_name()} used the support skill {ability.get_name()}!\n'

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
        # print('\t\t\t\tRandom Modifier:', random_modifier)
        element_modifier = target.element_modifier(skill.get_element())
        # print('\t\t\t\tElement Modifier:', element_modifier)
        effective_attack *= element_modifier
        info.effective_attack = effective_attack
        info.defense = target.get_defense()
        info.penetration = self._get_penetration(info, entity, target)
        if info.penetration:
            info.defense = 0
            self._log += f'      Penetration\n'
        info.critical = self._get_critical(info)
        if info.critical:
            info.effective_attack *= Refs.gc.get_random_critical_modifier()
            self._log += f'      Critical\n'
        info.block = self._get_block(info, target)
        if info.block:
            info.effective_attack *= 0.5
            self._log += f'      Block\n'
        info.evade = self._get_evade(info, entity, target)
        if info.evade:
            info.effective_attack = 0
            self._log += f'      Evade\n'
        info.counter = self._get_counter(info, entity, target)
        return max(info.effective_attack - info.defense, 0) * random_modifier, info.counter, info.evade

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

        if skill.get_boosts() is not None:
            for boost in skill.get_boosts():
                boost_value = TEMP_BOOST_BY_TARGET[boost.get_type()][skill.get_target()]
                # print('\\t\t\tApply Boost of ', boost_value, 'to', STAT_TYPES[boost.get_stat_type()])
                entity.apply_effect(boost.get_stat_type(), AppliedEffect(boost_value, 1))

        # if skill.get_effects():
        #     for effect in skill.get_effects():
        #         print(effect)

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
        # Apply attack
        base_attack = entity.get_attack(skill.get_attack_type())
        # print('\t\t\tBase Attack:', base_attack)
        skill_power = skill.get_power()
        # print('\t\t\tSkill Modifier:', skill_power)

        effective_attack = base_attack * skill_power

        counters = []
        for target in targets:
            # print(f'\t\t\t{target.get_name()}:')
            damage, do_counter, evade = self._get_damage(effective_attack, entity, target, skill)
            # print('\t\t\t\tDamage: ', damage)
            self._log += f'      {round(damage, 1)} damage to {target.get_name()}\n'
            target.decrease_health(damage)

            if target.is_dead():
                if target.is_character():
                    self._log += f'   {target.get_name()} has been incapacitated!\n'
                else:
                    self._log += f'   {target.get_name()} has been killed!\n'
            else:
                if do_counter and not counter:
                    counters.append(lambda t=target: self._process_move(t, True))
                if skill.get_effects() and not evade:
                    for effect in skill.get_effects():
                        if effect.get_target() == FOE:
                            self._apply_effects(effect, target)
        self._process_effects(skill, entity)
        for counter in counters:
            counter()

    def _process_heal(self, entity, skill, targets):
        base_heal = entity.get_magical_attack()
        # print('\t\t\tBase Heal:', base_heal)
        skill_power = skill.get_power()
        # print('\t\t\tSkill Modifier:', skill_power)
        effective_heal = base_heal * skill_power

        for target in targets:
            # print(f'\t\t\t{target.get_name()}:')

            random_modifier = Refs.gc.get_random_attack_modifier()
            # print('\t\t\t\tRandom Modifier:', random_modifier)

            target_effective_heal = effective_heal * random_modifier
            # print('\t\t\t\tHeal: ', target_effective_heal)
            self._log += f'      {round(target_effective_heal, 1)} heal to {target.get_name()}\n'
            target.decrease_health(-target_effective_heal)
            if skill.get_effects():
                for effect in skill.get_effects():
                    if effect.get_target() == ALLY:
                        self._apply_effects(effect, target)
        self._process_effects(skill, entity)

    def _process_ailment_cure(self, entity, skill, targets):
        for target in targets:
            # print(f'\t\t\t{target.get_name()}:')
            # print('\t\t\t\tAilment Cure')
            if skill.get_effects():
                for effect in skill.get_effects():
                    if effect.get_target() == ALLY:
                        self._apply_effects(effect, target)
        self._process_effects(skill, entity)

    def _process_cause_effect(self, entity, skill, targets, counter):
        counters = []
        for target in targets:
            # print(f'\t\t\t{target.get_name()}:')
            info = TargetInfo()
            if entity.is_character() != target.is_character():
                info.evade = self._get_evade(info, entity, target)
                info.counter = self._get_counter(info, entity, target)

            if info.counter and not counter:
                if not target.is_dead():
                    counters.append(lambda t=target: self._process_move(t, True))
                    if skill.get_effects() and not info.evade:
                        for effect in skill.get_effects():
                            if effect.get_target() == FOE:
                                self._apply_effects(effect, target)
        self._process_effects(skill, entity)
        for counter in counters:
            counter()

    def _process_effects(self, skill, entity):
        if skill.get_effects():
            for effect in skill.get_effects():
                if effect.get_target() == SELF:
                    self._apply_effects(effect, entity)
                elif effect.get_target() == ALLIES:
                    for target in self._get_targets(ALLIES, entity.is_character()):
                        self._apply_effects(effect, target)
                elif effect.get_target() == FOES:
                    for target in self._get_targets(FOES, entity.is_character()):
                        self._apply_effects(effect, target)
                else:
                    for target in self._get_targets(ALLY, False):
                        self._apply_effects(effect, target)

    def _apply_effects(self, effect, target):
        if effect.get_type() == STAT:
            # print('\t\t\tApply Effect', STAT_TYPES[effect.get_sub_type()], 'to', target.get_name())
            target.apply_effect(effect.get_sub_type(), AppliedEffect(effect.get_amount(), effect.get_duration()))
        elif effect.get_type() == COUNTER:
            pass
        elif effect.get_type() == DURATION:
            pass
        elif effect.get_type() == SPECIFIC_TARGET:
            pass
        elif effect.get_type() == STATUS_EFFECT:
            pass

    def _make_choice(self, chance):
        if chance == 0:
            return 0
        return choices([True, False], [chance, 1 / chance])[0]

    def _get_penetration(self, info, entity, target):
        """
        The higher effective attack over defense
        This is offset by a targets agility. The higher a targets agility, the less chance of penetration
        """
        strength_ratio = info.effective_attack / max(info.defense, 1)
        agility_ratio = entity.get_agility() / target.get_agility()
        ratio = (strength_ratio * 2 + agility_ratio) / 3
        penetration = self._make_choice(ratio)
        # print('\t\t\t\tPenetration:', penetration)
        return penetration

    def _get_critical(self, info):
        """
        The higher entities strength over a targets defense, the higher chance for a critical
        """
        ratio = info.effective_attack / max(info.defense, 1)
        critical = self._make_choice(ratio)
        # print('\t\t\t\tCritical:', critical)
        return critical

    def _get_block(self, info, target):
        """
        The higher targets defense is over effective attack, the higher a chance for block
        """
        if info.penetration:
            return False
        ratio = info.defense / max(info.effective_attack, 1)
        block = self._make_choice(ratio)
        # print('\t\t\t\tBlock:', block)
        return block

    def _get_evade(self, info, entity, target):
        """
        The higher the dexterity and agility, the higher chance of an evasion
        """
        if info.penetration or info.block:
            return False
        dexterity_ratio = target.get_dexterity() / entity.get_dexterity()
        agility_ratio = target.get_agility() / entity.get_agility()
        ratio = (dexterity_ratio * 2 + agility_ratio) / 3
        evade = self._make_choice(ratio)
        # print('\t\t\t\tEvade:', evade)
        return evade

    def _get_counter(self, info, entity, target):
        dexterity_ratio = target.get_dexterity() / entity.get_dexterity()
        agility_ratio = target.get_agility() / entity.get_agility()
        ratio = (dexterity_ratio + agility_ratio) / 2
        if info.block or info.evade:
            ratio *= 1.5
        counter = self._make_choice(ratio)
        # print('\t\t\t\tCounter:', counter)
        return counter
