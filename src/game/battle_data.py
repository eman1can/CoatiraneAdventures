from math import floor
from random import choices

from game.skill import ALL_ALLIES, ALL_FOES, FOE, SELF
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
    def __init__(self, adventurers, supporters, special_amount):
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
        self._special_amount = special_amount
        self._dropped_items = {}

    def get_battle_log(self):
        return self._log

    def get_dropped_items(self):
        return self._dropped_items

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
        print(f'Process Turn {self._turn}')
        self._log += f'Turn {self._turn}\n'
        win = loss = False
        for entity in self._get_turn_order():
            print(f'\tMove of {entity.get_name()}')
            self._process_move(entity)
            # Check for win or loss
            win, loss = self.check_end()
            if loss or win:
                break
        self._turn += 1
        # Increase SA Gauge
        print('Special gauge', self._special_amount, '→', self._special_amount+1)
        if self._special_amount < 25:
            self._special_amount += 1
        # Decrease effect counters and apply EOT effects
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
            self._log += f'Level {enemy.get_level()} {enemy.get_name()} entered the battle!\n'
        for character in self._adventurers:
            self._log += f'{character.get_name()} joined the battle!\n'
            print(character.get_description_recap())
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

    # def use_skill(self, caller, skill):
    #     self._log += f'{caller.get_name()} used skill {skill.get_name()}!\n'
    #     if skill.get_target() == ALL_FOES:
    #         for enemy in self._enemies:
    #             for effect in skill.get_effects():
    #                 enemy.apply_effect(effect)
    #     elif skill.get_target() == ALL_FOES:
    #         pass
    #     elif skill.get_target() == ALL_ALLIES:
    #         for character in self._adventurers:
    #             for effect in skill.get_effects():
    #                 character.apply_effect(effect)
    #     elif skill.get_target() == SELF:
    #         pass

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

        # print(entities[0].get_name(), end=' ')
        # for entity in entities[1:]:
        #     print('→', entity.get_name(), end=' ')
        # print()
        return entities

    def _get_targets(self, target_type, is_character):
        targets = []
        if is_character:
            for entity in self._enemies:
                if not entity.is_dead():
                    targets.append(entity)
        else:
            for entity in self._adventurers:
                if not entity.is_dead():
                    targets.append(entity)

        if target_type is ALL_FOES:
            return targets
        else:
            return choices(targets, k=1)

    def _get_damage(self, effective_attack, entity, target, skill):
        info = TargetInfo()
        random_modifier = Refs.gc.get_random_attack_modifier()
        print('\t\t\t\tRandom Modifier:', random_modifier)
        element_modifier = skill.element_modifier(target)
        print('\t\t\t\tElement Modifier:', element_modifier)
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
        return max(info.effective_attack - info.defense, 0) * random_modifier, info.counter

    def _process_move(self, entity, counter=False):
        if entity.is_dead():
            return
        if counter:
            skill = entity.get_counter_skill()
            if skill is None:
                return
            print(f'\t\tCounter with {skill.get_name()}')
            self._log += f'   {entity.get_name()} counters with {skill.get_name()}\n'
        else:
            skill = entity.get_selected_skill()
            print(f'\t\tUses {skill.get_name()}')
            self._log += f'   {entity.get_name()} used {skill.get_name()}\n'

        # Get targets
        if skill.get_target() in [FOE, ALL_FOES]:
            # Pre-attack effects to skill

            # Get targets
            targets = self._get_targets(skill.get_target(), entity.is_character())
            # Apply attack
            base_attack = entity.get_attack(skill.get_attack_type())
            print('\t\t\tBase Attack:', base_attack)
            skill_modifier = skill.get_modifier()
            print('\t\t\tSkill Modifier:', skill_modifier)

            effective_attack = base_attack * skill_modifier

            if skill.is_special():
                self._special_amount -= 5

            if skill.get_mana_cost() > 0:
                self._log += f'      -{skill.get_mana_cost()} Mana\n'
                entity.decrease_mana(skill.get_mana_cost())

            for target in targets:
                print(f'\t\t\t{target.get_name()}:')
                damage, do_counter = self._get_damage(effective_attack, entity, target, skill)
                print('\t\t\t\tDamage: ', damage)
                self._log += f'      {round(damage, 1)} damage to {target.get_name()}\n'
                target.decrease_health(damage)
                if target.is_dead():
                    if target.is_character():
                        self._log += f'   {target.get_name()} has been incapacitated!\n'
                    else:
                        self._log += f'   {target.get_name()} has been killed!\n'
                        self._generate_drop(target)
                if do_counter and not counter:
                    if not target.is_dead():
                        self._process_move(target, True)

    def _make_choice(self, chance):
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
        print('\t\t\t\tPenetration:', penetration)
        return penetration

    def _get_critical(self, info):
        """
        The higher entities strength over a targets defense, the higher chance for a critical
        """
        ratio = info.effective_attack / max(info.defense, 1)
        critical = self._make_choice(ratio)
        print('\t\t\t\tCritical:', critical)
        return critical

    def _get_block(self, info, target):
        """
        The higher targets defense is over effective attack, the higher a chance for block
        """
        if info.penetration:
            return False
        ratio = info.defense / max(info.effective_attack, 1)
        block = self._make_choice(ratio)
        print('\t\t\t\tBlock:', block)
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
        print('\t\t\t\tEvade:', evade)
        return evade

    def _get_counter(self, info, entity, target):
        dexterity_ratio = target.get_dexterity() / entity.get_dexterity()
        agility_ratio = target.get_agility() / entity.get_agility()
        ratio = (dexterity_ratio + agility_ratio) / 2
        if info.block or info.evade:
            ratio *= 1.5
        counter = self._make_choice(ratio)
        print('\t\t\t\tCounter:', counter)
        return counter

    def _generate_drop(self, entity):
        """
        Generate a dropped item from the enemy
        """
        drop_ids = Refs.gc['enemies'][entity.get_id()].generate_drop()
        announced = []
        for drop_id in drop_ids:
            item = Refs.gc.add_to_inventory(drop_id)
            if item not in self._dropped_items:
                self._dropped_items[item] = 0
            self._dropped_items[item] += 1
            if drop_id not in announced:
                self._log += f'      {entity.get_name()} dropped {item.get_name()} x {drop_ids.count(drop_id)}\n'
                announced.append(drop_id)
