"""
Elimination Quest: Kill X monster
Gathering Quest: Collect X of item
Progress Quest: Reach X Floor
Exploration Quest: Uncover X Nodes or Safe Zones
Survival Quest: Survive X Encounters without dying
Crafting Quest: Craft X item
Growth Quest: Gain X ability points or Unlock x status board slots or Spend x skill points
Recruitment Quest: Recruit x adventurers
Loyalty Quest: Play for x days
Rank Break Quest: Rank Break x adventuers
Rank Up Quest: Rank Up x adventurers
Familiarity Quest: Gain X% Familiarity
Score Quest: Achieve a Party Score of x

Change Quest Type based on Renown

Daily Quests:
2-4 Elimination Quests
2-4 Gathering Quests
1-2 Survival Quests
1-2 Growth Quests
Login From 12 PM - 11:59 AM
Login From 12 AM - 11:59 PM
Complete All Above Quests

Weekly Quests:
8-12 Elimination Quests
8-12 Gathering Quests
4-8 Survival Quests
4-8 Growth Quests
2-4 Crafting Quests
Login Every Day of the Week
Complete All Above Quests

Monthly Quests:
24-36 Elimination Quests
24-36 Gathering Quests
18-24 Survival Quests
18-24 Growth Quests
10-16 Crafting Quests
2-4 Familiarity Quests
2-4 Score Quests
2-4 Exploration Quests
2-4 Progress Quests
Login Every Day of the Month
Login at least two days of the week
Complete All Above Quests

"Campaign" Quests
Blah
"""

# Quest Types
from math import ceil, sqrt

from calendar import monthrange
from datetime import datetime, timedelta
from random import choices, gauss, randint, uniform
from time import time_ns

from refs import Refs

UNSPECIFIED = 0
ELIMINATION = 1   # C Kill X monster
GATHERING   = 2   # C Collect X of item
PROGRESS    = 3   # Reach X Floor
EXPLORATION = 4   # Uncover X Nodes or Safe Zones
SURVIVAL    = 5   # C Survive X Encounters without dying
CRAFTING    = 6   # C Craft X item
GROWTH      = 7   # C Gain X ability points or Unlock x status board slots or Spend x skill points
RECRUITMENT = 8   # Recruit x adventurers
LOGIN_PERIOD= 9   # C Play for x days
LOYALTY     = 10  # C Play for x days
RANK_UP     = 11  # Rank Up x adventurers
RANK_BREAK  = 12  # Rank Break x adventuers
FAMILIARITY = 13  # Gain X% Familiarity
SCORE       = 14  # Achieve a Party Score of x
COMPLETION  = 15  # Complete other quests
STACK_COMPLETION = 16  # Complete other quest stacks


class QuestManager:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._daily_quests = []
        self._weekly_quests = []
        self._monthly_quests = []
        self._campaign_quests = []

        self._timestamp = datetime.now()

    def get_data_to_save(self):
        save_data = {}

        daily_quests = []
        for quest_stack in self._daily_quests:
            daily_quests.append(quest_stack.get_data_to_save(self))
        save_data['daily_quests'] = daily_quests

        weekly_quests = []
        for quest_stack in self._weekly_quests:
            weekly_quests.append(quest_stack.get_data_to_save(self))
        save_data['weekly_quests'] = weekly_quests

        monthly_quests = []
        for quest_stack in self._monthly_quests:
            monthly_quests.append(quest_stack.get_data_to_save(self))
        save_data['monthly_quests'] = monthly_quests

        campaign_quests = []
        for quest_stack in self._campaign_quests:
            campaign_quests.append(quest_stack.get_data_to_save(self))
        save_data['campaign_quests'] = campaign_quests

        save_data['timestamp'] = datetime.timestamp(self._timestamp)

        return save_data

    def load_from_data(self, save_data):

        timestamp = datetime.fromtimestamp(save_data['timestamp'])
        current_timestamp = datetime.now()

        Refs.log(f'Save timestamp is {timestamp.hour}:{timestamp.minute} {timestamp.month}, {timestamp.day} {timestamp.year}')
        Refs.log(f'Current timestamp is {current_timestamp.hour}:{current_timestamp.minute} {current_timestamp.month}, {current_timestamp.day} {current_timestamp.year}')

        if timestamp.year == current_timestamp.year:
            if timestamp.date() == current_timestamp.date():
                daily_quests = []
                for quest_stack_data in save_data['daily_quests']:
                    quest_stack = QuestStack()
                    quest_stack.load_from_data(self, quest_stack_data)
                    daily_quests.append(quest_stack)
                self._daily_quests = daily_quests
            else:
                self._daily_quests = self.generate_daily_quests()

            if (timestamp.day - timestamp.weekday()) == (current_timestamp.day - current_timestamp.weekday()):
                weekly_quests = []
                for quest_stack_data in save_data['weekly_quests']:
                    quest_stack = QuestStack()
                    quest_stack.load_from_data(self, quest_stack_data)
                    weekly_quests.append(quest_stack)
                self._weekly_quests = weekly_quests
            else:
                self._weekly_quests = self.generate_weekly_quests()

            if timestamp.month == current_timestamp.month:
                monthly_quests = []
                for quest_stack_data in save_data['monthly_quests']:
                    quest_stack = QuestStack()
                    quest_stack.load_from_data(self, quest_stack_data)
                    monthly_quests.append(quest_stack)
                self._monthly_quests = monthly_quests
            else:
                self._monthly_quests = self.generate_monthly_quests()
        else:
            self._daily_quests = self.generate_daily_quests()
            self._weekly_quests = self.generate_weekly_quests()
            self._monthly_quests = self.generate_monthly_quests()

        campaign_quests = []
        for quest_stack_data in save_data['campaign_quests']:
            quest_stack = QuestStack()
            quest_stack.load_from_data(self, quest_stack_data)
            campaign_quests.append(quest_stack)
        self._campaign_quests = campaign_quests

        stacks = self._daily_quests + self._weekly_quests + self._monthly_quests + self._campaign_quests
        for stack in stacks:
            for quest in stack:
                quest.form_memory_links(self)

    def generate_quest(self, quest_type):
        if quest_type == ELIMINATION:
            max_explored_floor = Refs.gc.get_lowest_floor()
            enemy_ids = Refs.gc.get_enemies_to_floor(max_explored_floor)
            return self._generate_elimination_quest(enemy_ids)
        elif quest_type == GATHERING:
            max_explored_floor = Refs.gc.get_lowest_floor()
            enemy_ids = Refs.gc.get_enemies_to_floor(max_explored_floor)
            item_ids = Refs.gc.get_materials_to_floor(max_explored_floor)
            for enemy_id in enemy_ids:
                enemy = Refs.gc['enemies'][enemy_id]
                item_ids += enemy.get_drop_items().keys()
            return self._generate_gathering_quest(item_ids)
        elif quest_type == PROGRESS:
            return self._generate_progress_quest()
        elif quest_type == EXPLORATION:
            node_ids = []
            max_explored_floor = Refs.gc.get_lowest_floor()
            node_ids += Refs.gc.get_enemies_to_floor(max_explored_floor)
            for floor_index in range(max_explored_floor):
                floor_materials = Refs.gc['floors'][floor_index + 1].get_resources()
                node_ids += list(floor_materials['metals'].keys())
                node_ids += list(floor_materials['gems'].keys())
            return self._generate_exploration_quest(node_ids)
        elif quest_type == SURVIVAL:
            return self._generate_survival_quest()
        elif quest_type == CRAFTING:
            item_ids = [recipe.get_output_id() for recipe in Refs.gc.get_craftable_recipes()]
            if len(item_ids) == 0:
                return None
            return self._generate_crafting_quest(item_ids)
        elif quest_type == GROWTH:
            return self._generate_growth_quest()
        elif quest_type == RECRUITMENT:
            targets = [char.get_id() for char in Refs.gc.get_all_obtained_characters()]
            return self._generate_recruitment_quest(targets)
        elif quest_type == LOGIN_PERIOD:
            date = datetime.now().date()
            start_time = datetime(date.year, date.month, date.day, 0, 0, 0)
            end_time = datetime(date.year, date.month, date.day, 23, 59, 59)
            return self._generate_login_quest(start_time, end_time)
        elif quest_type == LOYALTY:
            date = datetime.now().date()
            week_offset = timedelta(days=-date.weekday())
            start_date = date + week_offset
            periods = []
            for index in range(7):
                start_time = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0) + timedelta(days=index)
                end_time = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59) + timedelta(days=index)
                periods.append((start_time, end_time))
            return self._generate_loyalty_quest(periods)
        elif quest_type == RANK_UP:
            targets = [char.get_id() for char in Refs.gc.get_all_obtained_characters()]
            return self._generate_rank_up_quest(targets)
        elif quest_type == RANK_BREAK:
            targets = [char.get_id() for char in Refs.gc.get_all_obtained_characters()]
            return self._generate_rank_break_quest(targets)
        elif quest_type == FAMILIARITY:
            targets = [char.get_id() for char in Refs.gc.get_all_obtained_characters()]
            return self._generate_familiarity_quest(targets)
        elif quest_type == SCORE:
            current_score = Refs.gc.get_current_party_score()
            return self._generate_score_quest(current_score)
        else:
            raise Exception("Unknown Quest Type!")

    def _generate_elimination_quest(self, enemy_ids):
        elimination_quest = EliminationQuest()

        # Enemy ID is random, no matter the Rank or Grade
        enemy_id = enemy_ids[randint(0, len(enemy_ids) - 1)]
        # The Boost is determined by the quest rank
        boost_spec = randint(ANY, GREATER_EQ)
        # The Actual Boost is also determined by the quest rank
        boost = choices(range(WORLD_DEVOURING + 1), [1 / x for x in range(1, WORLD_DEVOURING + 2)])[0]
        # The count is determined by the quest grade
        #  - The Lowest we want to eliminate will be 1
        #  - The Highest we want to eliminate will be 1000
        grade = 0
        count = round(min(1000, max(1, gauss(grade, uniform(sqrt(grade), sqrt(grade) * 3)))))
        # The reward renown points is calculated from quest grade
        elimination_quest.generate(enemy_id, boost_spec, boost, count)
        return elimination_quest

    def _generate_elimination_quests(self, a, b, append_callback):
        elimination_count = randint(a, b)
        max_explored_floor = Refs.gc.get_lowest_floor()
        enemy_ids = Refs.gc.get_enemies_to_floor(max_explored_floor)
        if len(enemy_ids) == 0:
            return
        for index in range(elimination_count):
            elimination_quest = self._generate_elimination_quest(enemy_ids)
            append_callback(elimination_quest)

    def _generate_elimination_stack(self, a, b):
        elimination_quest_stack = QuestStack()
        self._generate_elimination_quests(a, b, elimination_quest_stack.add_quest)
        return elimination_quest_stack

    def _generate_gathering_quest(self, item_ids):
        gathering_quest = GatheringQuest()
        item_id = item_ids[randint(0, len(item_ids) - 1)]
        count = randint(4, 24)
        gathering_quest.generate(item_id, count)
        return gathering_quest

    def _generate_gathering_quests(self, a, b, append_callback):
        gathering_count = randint(a, b)
        max_explored_floor = Refs.gc.get_lowest_floor()
        enemy_ids = Refs.gc.get_enemies_to_floor(max_explored_floor)
        if len(enemy_ids) == 0:
            return
        item_ids = Refs.gc.get_materials_to_floor(max_explored_floor)
        if len(item_ids) == 0:
            return
        for enemy_id in enemy_ids:
            enemy = Refs.gc['enemies'][enemy_id]
            item_ids += enemy.get_unqiue_drop_items()
        for index in range(gathering_count):
            gathering_quest = self._generate_gathering_quest(item_ids)
            append_callback(gathering_quest)

    def _generate_gathering_stack(self, a, b):
        gathering_quest_stack = QuestStack()
        self._generate_gathering_quests(a, b, gathering_quest_stack.add_quest)
        return gathering_quest_stack

    def _generate_progress_quest(self):
        progress_quest = ProgressQuest()
        max_explored_floor = Refs.gc.get_lowest_floor()
        floor_to_reach = randint(1, 60)
        progress_quest.generate(max_explored_floor, floor_to_reach)
        return progress_quest

    def _generate_progress_quests(self, a, b, append_callback):
        progress_count = randint(a, b)
        for index in range(progress_count):
            progress_quest = self._generate_progress_quest()
            append_callback(progress_quest)

    def _generate_progress_stack(self, a, b):
        progress_stack = QuestStack()
        self._generate_progress_quests(a, b, progress_stack.add_quest)
        return progress_stack

    def _generate_exploration_quest(self, node_ids):
        exploration_quest = ExplorationQuest()
        exploration_type = randint(ENCOUNTER_NODE, DISCOVER_NODE)
        node_id = node_ids[randint(0, len(node_ids) - 1)]
        count = randint(4, 24)
        exploration_quest.generate(exploration_type, node_id, count)
        return exploration_quest

    def _generate_exploration_quests(self, a, b, append_callback):
        node_ids = []
        max_explored_floor = Refs.gc.get_lowest_floor()
        if max_explored_floor == 0:
            return
        node_ids += Refs.gc.get_enemies_to_floor(max_explored_floor)
        for floor_index in range(max_explored_floor):
            floor_materials = Refs.gc['floors'][floor_index + 1].get_resources()
            node_ids += list(floor_materials['metals'].keys())
            node_ids += list(floor_materials['gems'].keys())
        exploration_count = randint(a, b)
        for index in range(exploration_count):
            exploration_quest = self._generate_exploration_quest(node_ids)
            append_callback(exploration_quest)

    def _generate_exploration_stack(self, a, b):
        exploration_stack = QuestStack()
        self._generate_exploration_quests(a, b, exploration_stack.add_quest)
        return exploration_stack

    def _generate_survival_quest(self):
        survival_quest = SurvivalQuest()
        count = randint(4, 24)
        survival_quest.generate(count)
        return survival_quest

    def _generate_survival_quests(self, a, b, append_callback):
        survival_count = randint(a, b)
        for index in range(survival_count):
            survival_quest = self._generate_survival_quest()
            append_callback(survival_quest)

    def _generate_survival_stack(self, a, b):
        survival_stack = QuestStack()
        self._generate_survival_quests(a, b, survival_stack.add_quest)
        return survival_stack

    def _generate_crafting_quest(self, item_ids):
        crafting_quest = CraftingQuest()
        item_id = item_ids[randint(0, len(item_ids) - 1)]
        count = randint(4, 24)
        crafting_quest.generate(item_id, count)
        return crafting_quest

    def _generate_crafting_quests(self, a, b, append_callback):
        crafting_count = randint(a, b)
        item_ids = [recipe.get_output_id() for recipe in Refs.gc.get_craftable_recipes()]
        print(item_ids)
        if len(item_ids) == 0:
            return
        for index in range(crafting_count):
            crafting_quest = self._generate_crafting_quest(item_ids)
            append_callback(crafting_quest)

    def _generate_crafting_stack(self, a, b):
        crafting_stack = QuestStack()
        self._generate_crafting_quests(a, b, crafting_stack.add_quest)
        return crafting_stack

    def _generate_growth_quest(self):
        growth_type = randint(ABILITY_POINTS, STATUS_SLOTS)
        if growth_type == ABILITY_POINTS:
            return self._generate_ability_growth_quest()
        elif growth_type == SKILL_POINTS:
            return self._generate_skill_growth_quest()
        elif growth_type == STATUS_SLOTS:
            return self._generate_status_growth_quest()
        else:
            raise Exception("Non a valid growth type!")

    def _generate_growth_quests(self, a, b, append_callback):
        growth_count = randint(a, b)
        for index in range(growth_count):
            growth_quest = self._generate_growth_quest()
            append_callback(growth_quest)

    def _generate_growth_stack(self, a, b):
        growth_stack = QuestStack()
        self._generate_growth_quests(a, b, growth_stack.add_quest)
        return growth_stack

    def _generate_ability_growth_quest(self):
        growth_quest = AbilityPointsGrowthQuest()
        specification = randint(ANY, GREATER_EQ)
        type = randint(HEALTH, DEXTERITY)
        count = randint(4, 24)
        growth_quest.generate(specification, type, count)
        return growth_quest

    def _generate_skill_growth_quest(self):
        growth_quest = SkillPointsGrowthQuest()
        count = randint(4, 24)
        growth_quest.generate(count)
        return growth_quest

    def _generate_status_growth_quest(self):
        growth_quest = StatusSlotGrowthQuest()
        specification = randint(ANY, GREATER_EQ)
        type = randint(STRENGTH, DEXTERITY)
        count = randint(4, 24)
        growth_quest.generate(specification, type, count)
        return growth_quest

    def _generate_recruitment_quest(self, targets):
        growth_type = randint(RANDOM_GROWTH, SPECIFIC_GROWTH)
        if growth_type == RANDOM_GROWTH:
            recruitment_quest = self._generate_random_recruitment_quest()
        else:
            recruitment_quest = self._generate_specific_recruitment_quest(targets)
        return recruitment_quest

    def _generate_random_recruitment_quest(self):
        recruitment_quest = RecruitmentQuest()
        count = randint(4, 24)
        recruitment_quest.generate(count)
        return recruitment_quest

    def _generate_specific_recruitment_quest(self, targets):
        recruitment_quest = SpecificRecruitmentQuest()
        target_1 = targets[randint(0, len(targets) - 1)]
        targets.remove(target_1)
        target_2 = targets[randint(0, len(targets) - 1)]
        targets.append(target_1)
        count = randint(4, 24)
        recruitment_quest.generate(target_1, target_2, count)
        return recruitment_quest

    def _generate_recruitment_quests(self, a, b, append_callback):
        recruitment_count = randint(a, b)
        targets = [char.get_id() for char in Refs.gc.get_all_obtained_characters()]
        for index in range(recruitment_count):
            recruitment_quest = self._generate_recruitment_quest(targets)
            append_callback(recruitment_quest)

    def _generate_recruitment_stack(self, a, b):
        recruitment_stack = QuestStack()
        self._generate_recruitment_quests(a, b, recruitment_stack.add_quest)
        return recruitment_stack

    def _generate_login_quest(self, start_time, end_time):
        login_quest = LoginPeriodQuest()
        login_quest.generate(start_time, end_time)
        return login_quest

    def _generate_login_quest_for_stack(self, start_time, end_time, append_callback):
        login_quest = self._generate_login_quest(start_time, end_time)
        append_callback(login_quest)

    def _generate_loyalty_quest(self, time_periods):
        loyalty_quest = LoyaltyQuest()
        loyalty_quest.generate(time_periods)
        return loyalty_quest

    def _generate_loyalty_quest_for_stack(self, time_periods, append_callback):
        loyalty_quest = self._generate_loyalty_quest(time_periods)
        append_callback(loyalty_quest)

    def _generate_rank_up_quest(self, targets):
        growth_type = randint(RANDOM_GROWTH, SPECIFIC_GROWTH)
        if growth_type == RANDOM_GROWTH:
            rank_up_quest = self._generate_random_rank_up_quest()
        else:
            rank_up_quest = self._generate_specific_rank_up_quest(targets)
        return rank_up_quest

    def _generate_random_rank_up_quest(self):
        rank_up_quest = RankUpQuest()
        count = randint(4, 24)
        rank_up_quest.generate(count)
        return rank_up_quest

    def _generate_specific_rank_up_quest(self, targets):
        rank_up_quest = SpecificRankUpQuest()
        target_1 = targets[randint(0, len(targets) - 1)]
        targets.remove(target_1)
        target_2 = targets[randint(0, len(targets) - 1)]
        targets.append(target_1)
        count = randint(4, 24)
        rank_up_quest.generate(target_1, target_2, count)
        return rank_up_quest

    def _generate_rank_up_quests(self, a, b, append_callback):
        rank_up_count = randint(a, b)
        targets = [char.get_id() for char in Refs.gc.get_all_obtained_characters()]
        for index in range(rank_up_count):
            rank_up_quest = self._generate_rank_up_quest(targets)
            append_callback(rank_up_quest)

    def _generate_rank_up_stack(self, a, b):
        rank_up_stack = QuestStack()
        self._generate_rank_up_quests(a, b, rank_up_stack.add_quest)
        return rank_up_stack

    def _generate_rank_break_quest(self, targets):
        growth_type = randint(RANDOM_GROWTH, SPECIFIC_GROWTH)
        if growth_type == RANDOM_GROWTH:
            rank_break_quest = self._generate_random_rank_break_quest()
        else:
            rank_break_quest = self._generate_specific_rank_break_quest(targets)
        return rank_break_quest

    def _generate_random_rank_break_quest(self):
        rank_break_quest = RankBreakQuest()
        count = randint(4, 24)
        rank_break_quest.generate(count)
        return rank_break_quest

    def _generate_specific_rank_break_quest(self, targets):
        rank_break_quest = SpecificRankBreakQuest()
        target_1 = targets[randint(0, len(targets) - 1)]
        targets.remove(target_1)
        target_2 = targets[randint(0, len(targets) - 1)]
        targets.append(target_1)
        count = randint(4, 24)
        rank_break_quest.generate(target_1, target_2, count)
        return rank_break_quest

    def _generate_rank_break_quests(self, a, b, append_callback):
        rank_break_count = randint(a, b)
        targets = [char.get_id() for char in Refs.gc.get_all_obtained_characters()]
        for index in range(rank_break_count):
            rank_break_quest = self._generate_rank_break_quest(targets)
            append_callback(rank_break_quest)

    def _generate_rank_break_stack(self, a, b):
        rank_break_stack = QuestStack()
        self._generate_rank_break_quests(a, b, rank_break_stack.add_quest)
        return rank_break_stack

    def _generate_familiarity_quest(self, targets):
        familiarity_type = randint(FAMILIARITY_RANDOM, FAMILIARITY_SPECIFIC)
        if len(targets) == 1 or familiarity_type == FAMILIARITY_RANDOM:
            familiarity_quest = self._generate_random_familiarity_quest()
        else:
            familiarity_quest = self._generate_specific_familiarity_quest(targets)
        return familiarity_quest

    def _generate_random_familiarity_quest(self):
        familiarity_quest = FamiliarityQuest()
        familiarity = randint(20, 1000)
        familiarity_quest.generate(familiarity)
        return familiarity_quest

    def _generate_specific_familiarity_quest(self, targets):
        familiarity_quest = SpecificFamiliarityQuest()
        target_1 = targets[randint(0, len(targets) - 1)]
        targets.remove(target_1)
        target_2 = targets[randint(0, len(targets) - 1)]
        targets.append(target_1)
        familiarity = randint(20, 1000)
        familiarity_quest.generate(target_1, target_2, familiarity)
        return familiarity_quest

    def _generate_familiarity_quests(self, a, b, append_callback):
        familiarity_count = randint(a, b)
        targets = [char.get_id() for char in Refs.gc.get_all_obtained_characters()]
        for index in range(familiarity_count):
            familiarity_quest = self._generate_familiarity_quest(targets)
            append_callback(familiarity_quest)

    def _generate_familiarity_stack(self, a, b):
        familiarity_stack = QuestStack()
        self._generate_familiarity_quests(a, b, familiarity_stack.add_quest)
        return familiarity_stack

    def _generate_score_quest(self, current_score):
        score_quest = ScoreQuest()
        goal_score = randint(100, 10000)
        score_quest.generate(current_score, goal_score)
        return score_quest

    def _generate_score_quests(self, a, b, append_callback):
        score_count = randint(a, b)
        current_score = Refs.gc.get_current_party_score()
        for index in range(score_count):
            score_quest = self._generate_score_quest(current_score)
            append_callback(score_quest)

    def _generate_score_stack(self, a, b):
        score_stack = QuestStack()
        self._generate_score_quests(a, b, score_stack.add_quest)
        return score_stack

    def _generate_completion_quest(self, quest_list):
        complete_quest = CompletionQuest()
        complete_quest.generate(quest_list)
        return complete_quest

    def _generate_completion_quest_for_stack(self, quest_list, append_callback):
        complete_quest = self._generate_completion_quest(quest_list)
        append_callback(complete_quest)

    def _generate_stack_completion_quest(self, stacks, completion_type):
        complete_stack_quest = CompletionStackQuest()
        complete_stack_quest.generate(stacks, completion_type)
        return complete_stack_quest

    def _generate_stack_completion_quest_for_stack(self, stacks, completion_type, append_callback):
        complete_stack_quest = self._generate_stack_completion_quest(stacks, completion_type)
        append_callback(complete_stack_quest)

    def load_quest(self, quest_data):
        quest_type = quest_data['type']
        if quest_type == ELIMINATION:
            quest = EliminationQuest()
        elif quest_type == GATHERING:
            quest = GatheringQuest()
        elif quest_type == PROGRESS:
            quest = ProgressQuest()
        elif quest_type == EXPLORATION:
            quest = ExplorationQuest()
        elif quest_type == SURVIVAL:
            quest = SurvivalQuest()
        elif quest_type == CRAFTING:
            quest = CraftingQuest()
        elif quest_type == GROWTH:
            growth_type = quest_data['growth_type']
            if growth_type == ABILITY_POINTS:
                quest = AbilityPointsGrowthQuest()
            elif growth_type == SKILL_POINTS:
                quest = SkillPointsGrowthQuest()
            elif growth_type == STATUS_SLOTS:
                quest = StatusSlotGrowthQuest()
            else:
                raise Exception("Unknown Growth Type Quest")
        elif quest_type == RECRUITMENT:
            if quest_data['recruitment_type'] == RANDOM_RECRUITMENT:
                quest = RecruitmentQuest()
            else:
                quest = SpecificRecruitmentQuest()
        elif quest_type == LOGIN_PERIOD:
            quest = LoginPeriodQuest()
        elif quest_type == LOYALTY:
            quest = LoyaltyQuest()
        elif quest_type == RANK_UP:
            if quest_data['growth_type'] == RANDOM_GROWTH:
                quest = RankUpQuest()
            else:
                quest = SpecificRankUpQuest()
        elif quest_type == RANK_BREAK:
            if quest_data['growth_type'] == RANDOM_GROWTH:
                quest = RankBreakQuest()
            else:
                quest = SpecificRankBreakQuest()
        elif quest_type == FAMILIARITY:
            if quest_data['familiarity_type'] == FAMILIARITY_RANDOM:
                quest = FamiliarityQuest()
            else:
                quest = SpecificFamiliarityQuest()
        elif quest_type == SCORE:
            quest = ScoreQuest()
        elif quest_type == COMPLETION:
            quest = CompletionQuest()
        elif quest_type == STACK_COMPLETION:
            quest = CompletionStackQuest()
        else:
            raise Exception(f"Unknown Quest Type {quest_type}!")
        quest.load_from_data(self, quest_data)
        return quest

    def generate_daily_quests(self):
        """
        2-4 Elimination Quests
        2-4 Gathering Quests
        1-2 Survival Quests
        1-2 Growth Quests
        Login From 12 PM - 11:59 AM
        Login From 12 AM - 11:59 PM
        Complete All Above Quests
        """

        Refs.log("Generate Daily Quests")

        # 2-4 Elimination Quests
        elimination_quest_stack = self._generate_elimination_stack(2, 4)
        # 2-4 Gathering Quests
        gathering_quest_stack = self._generate_gathering_stack(2, 4)
        # 1-2 Survival Quests
        survival_quest_stack = self._generate_survival_stack(1, 2)
        # 1-2 Growth Quests
        growth_quest_stack = self._generate_growth_stack(1, 2)

        login_quest_stack = QuestStack()
        complete_quest_stack = QuestStack()

        # Login from Midnight to Noon
        date = datetime.now().date()
        start_time = datetime(date.year, date.month, date.day, 0, 0, 0)
        end_time = datetime(date.year, date.month, date.day, 11, 59, 59)
        self._generate_login_quest_for_stack(start_time, end_time, login_quest_stack.add_quest)

        # Noon to Midnight
        start_time = datetime(date.year, date.month, date.day, 12, 0, 0)
        end_time = datetime(date.year, date.month, date.day, 23, 59, 59)
        self._generate_login_quest_for_stack(start_time, end_time, login_quest_stack.add_quest)

        stacks = [
            elimination_quest_stack,
            gathering_quest_stack,
            survival_quest_stack,
            growth_quest_stack,
            login_quest_stack
        ]

        # Complete all above quests
        self._generate_stack_completion_quest_for_stack(stacks, 'Daily', complete_quest_stack.add_quest)
        stacks.append(complete_quest_stack)
        return stacks

    def generate_weekly_quests(self):
        """
        8-12 Elimination Quests
        8-12 Gathering Quests
        4-8 Survival Quests
        4-8 Growth Quests
        2-4 Crafting Quests
        Login Every Day of the Week
        Complete All Above Quests
        """

        Refs.log("Generate Weekly Quests")

        # 8-12 Elimination Quests
        elimination_quest_stack = self._generate_elimination_stack(8, 12)
        # 8-12 Gathering Quests
        gathering_quest_stack = self._generate_gathering_stack(8, 12)
        # 4-8 Survival Quests
        survival_quest_stack = self._generate_survival_stack(4, 8)
        # 4-8 Growth Quests
        growth_quest_stack = self._generate_growth_stack(4, 8)
        # 2-4 Crafting Quests
        crafting_quest_stack = self._generate_crafting_stack(2, 4)

        loyalty_quest_stack = QuestStack()
        complete_quest_stack = QuestStack()

        # Login Every Day of the Week
        loyalty_quest = self.generate_quest(LOYALTY)
        loyalty_quest_stack.add_quest(loyalty_quest)

        stacks = [
            elimination_quest_stack,
            gathering_quest_stack,
            survival_quest_stack,
            growth_quest_stack,
            crafting_quest_stack,
            loyalty_quest_stack
        ]

        # Complete All Above Quests
        self._generate_stack_completion_quest_for_stack(stacks, 'Weekly', complete_quest_stack.add_quest)
        stacks.append(complete_quest_stack)
        return stacks

    def generate_monthly_quests(self):
        """
        24-36 Elimination Quests
        24-36 Gathering Quests
        18-24 Survival Quests
        18-24 Growth Quests
        10-16 Crafting Quests
        2-4 Familiarity Quests
        2-4 Score Quests
        2-4 Exploration Quests
        2-4 Progress Quests
        Login Every Day of the Month
        Login at least two days of the week
        Complete All Above Quests
        """

        Refs.log("Generate Monthly Quests")

        # 24-36 Elimination Quests
        elimination_quest_stack = self._generate_elimination_stack(8, 12)
        # 24-36 Gathering Quests
        gathering_quest_stack = self._generate_gathering_stack(8, 12)
        # 18-24 Survival Quests
        survival_quest_stack = self._generate_survival_stack(4, 8)
        # 18-24 Growth Quests
        growth_quest_stack = self._generate_growth_stack(4, 8)
        # 10-16 Crafting Quests
        crafting_quest_stack = self._generate_crafting_stack(2, 4)
        # 2-4 Familiarity Quests
        familiarity_quest_stack = self._generate_familiarity_stack(2, 4)
        # 2-4 Score Quests
        score_quest_stack = self._generate_score_stack(2, 4)
        # 2-4 Exploration Quests
        exploration_quest_stack = self._generate_exploration_stack(2, 4)
        # 2-4 Progress Quests
        progress_quest_stack = self._generate_progress_stack(2, 4)
        # Login Every Day of the Month
        login_quest_stack = QuestStack()
        date = datetime.now().date()
        week_day, day_count = monthrange(date.year, date.month)
        start_date = datetime(date.year, date.month, 1)
        for day in range(day_count):
            start_time = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0) + timedelta(days=day)
            end_time = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59) + timedelta(days=day)
            self._generate_login_quest_for_stack(start_time, end_time, login_quest_stack.add_quest)
        # Login at least two days of the week
        loyalty_quest_stack = QuestStack()
        start_date = datetime(date.year, date.month, 1) - timedelta(days=week_day)
        for week in range(ceil(day_count / 7)):
            periods = []
            for day in range(7):
                start_time = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0) + timedelta(days=day, weeks=week)
                end_time = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59) + timedelta(days=day, weeks=week)
                periods.append((start_time, end_time))
            loyalty_quest = self._generate_loyalty_quest(periods)
            loyalty_quest.set_goal(2)
            loyalty_quest_stack.add_quest(loyalty_quest)
        # Complete All Above Quests
        complete_quest_stack = QuestStack()

        stacks = [
            elimination_quest_stack,
            gathering_quest_stack,
            survival_quest_stack,
            growth_quest_stack,
            crafting_quest_stack,
            familiarity_quest_stack,
            score_quest_stack,
            exploration_quest_stack,
            progress_quest_stack,
            login_quest_stack,
            loyalty_quest_stack
        ]

        # Complete All Above Quests
        self._generate_stack_completion_quest_for_stack(stacks, 'Monthly', complete_quest_stack.add_quest)
        stacks.append(complete_quest_stack)
        return stacks

    # def generate_quest_grade(self, time_delta):




    def find_stack_by_type(self, quest_type):
        stacks = self._daily_quests + self._weekly_quests + self._monthly_quests + self._campaign_quests
        typed_stacks = []
        for stack in stacks:
            if stack.first().get_type() == quest_type:
                typed_stacks.append(stack)
        return typed_stacks

    def update_stack_after_quest_update(self, stack):
        while stack.first().finished():
            stack.increment_stack()
            stack.first().auto_update_progress()

    def find_quest_by_type(self, quest_type):
        stacks = self._daily_quests + self._weekly_quests + self._monthly_quests + self._campaign_quests
        quests = []
        for stack in stacks:
            for quest in stack:
                if quest.get_type() == quest_type:
                    quests.append(quest)
        return quests

    def find_quest_by_hash(self, quest_hash):
        stacks = self._daily_quests + self._weekly_quests + self._monthly_quests + self._campaign_quests
        for stack in stacks:
            for quest in stack:
                if quest.get_hash() == quest_hash:
                    return quest
        return None

    def find_quest_stack_by_hash(self, quest_stack_hash):
        stacks = self._daily_quests + self._weekly_quests + self._monthly_quests + self._campaign_quests
        for stack in stacks:
            if stack.get_hash() == quest_stack_hash:
                return stack
        return None

    def get_daily_quest_stacks(self):
        return self._daily_quests

    def get_weekly_quest_stacks(self):
        return self._weekly_quests

    def get_monthly_quest_stacks(self):
        return self._monthly_quests

    def get_campaign_quest_stacks(self):
        return self._campaign_quests


class QuestStack:
    def __init__(self):
        self._quests = []
        self._top_index = 0
        self._hash = time_ns() * randint(1, 10000)

    def __iter__(self):
        return iter(self._quests)

    def __next__(self):
        return next(self._quests)

    def __len__(self):
        return len(self._quests)

    def set_quests(self, quests):
        self._quests = quests
        self._top_index = self.first_uncompleted_index()

    def add_quest(self, quest):
        self._quests.append(quest)

    def get_data_to_save(self, manager):
        save_data = {'top_index': self._top_index}
        quest_data = []
        for quest in self._quests:
            quest_data.append(quest.get_data_to_save(manager))
        save_data['quest_data'] = quest_data
        save_data['hash'] = self._hash
        return save_data

    def load_from_data(self, manager, save_data):
        self._top_index = save_data['top_index']
        quest_list = []
        if len(save_data['quest_data']) > 0:
            for quest_data in save_data['quest_data']:
                quest = manager.load_quest(quest_data)
                quest_list.append(quest)
        self._quests = quest_list
        self._hash = save_data['hash']

    def get_hash(self):
        return self._hash

    def increment_index(self):
        self._top_index += 1

    def first(self):
        return self._quests[self._top_index]

    def first_uncompleted(self):
        for quest in self._quests:
            if quest.is_finished():
                continue
            return quest
        return None

    def all_uncompleted(self):
        for index in range(len(self._quests)):
            if self._quests[index].is_finished():
                continue
            return self._quests[index:]
        return []

    def first_uncompleted_index(self):
        for index in range(len(self._quests)):
            if self._quests[index].is_finished():
                continue
            return index
        return -1

    def all_completed(self):
        for index in range(len(self._quests)):
            if self._quests[index].is_finished():
                continue
            return self._quests[:index]
        return self._quests

    def auto_update_progress(self):
        while self.first().is_finished():
            self.increment_index()
            self.first().auto_update_progress()


class Quest:
    def __init__(self):
        self._type = UNSPECIFIED
        self._title = ''
        self._description = ''
        self._progress = 0
        self._goal = None
        self._claimed = False
        self._rewards = None
        self._hash = time_ns() * randint(1, 10000)

    def __str__(self):
        return f'<{self.__class__} {self._title}, {self._description}>'

    def generate(self, goal, *args):
        self._goal = goal

    def get_data_to_save(self, manager):
        save_data = {
            'type': self._type,
            'title': self._title,
            'description': self._description,
            'progress': self._progress,
            'goal': self._goal,
            'hash': self._hash
        }
        return save_data

    def load_from_data(self, manager, save_data):
        self._type = save_data['type']
        self._title = save_data['title']
        self._description = save_data['description']
        self._progress = save_data['progress']
        self._goal = save_data['goal']
        self._hash = save_data['hash']

    def form_memory_links(self, manager):
        pass

    def set_goal(self, goal):
        self._goal = goal

    def get_hash(self):
        return self._hash

    def get_type(self):
        return self._type

    def set_info(self, title, desc):
        self._title = title
        self._description = desc

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_info(self):
        return self._title, self._description

    def get_percent(self):
        return self._progress / self._goal

    def add_progress(self, progress):
        self._progress += progress
        if self._progress >= self._goal:
            self._progress = self._goal

    def set_progress(self, progress):
        self._progress = progress

    def get_progress(self):
        return self._progress

    def get_goal(self):
        return self._goal

    def is_finished(self):
        return self._progress == self._goal

    def get_rewards(self):
        return self._rewards

    def claimed(self):
        return self._claimed

    def claim(self):
        self._claimed = True
        # TODO: Give rewards to player

    def auto_update_progress(self):
        pass


BOOSTS_TO_STRING = ['', '{0}', '{0}or weaker ', '{0}or stronger ']
ANY        = 0
EQUAL      = 1
LESS_EQ    = 2
GREATER_EQ = 3

BOOSTT_TO_STRING = ['Normal ', 'Uncommon ', 'Abnormal ', 'Scary ', 'Freaky ', 'Beastly ', 'Menacing ', 'Nightmarish ', 'World Devouring ']
NORMAL          = 0
UNCOMMON        = 1
ABNORMAL        = 2
SCARY           = 3
FREAKY          = 4
BEASTLY         = 5
MENACING        = 6
NIGHTMARISH     = 7
WORLD_DEVOURING = 8


class EliminationQuest(Quest):
    def __init__(self):
        self._enemy_id = None
        self._boosts = None
        self._boostt = None
        super().__init__()
        self._type = ELIMINATION

    def generate(self, enemy_id, boost_specification, boost_type, count, *args):
        super().generate(count)
        self._enemy_id = enemy_id
        self._boosts = boost_specification
        self._boostt = boost_type

        enemy = Refs.gc['enemies'][enemy_id]
        enemy_name = enemy.get_name()

        nickname = BOOSTT_TO_STRING[boost_type]
        boost_string = BOOSTS_TO_STRING[boost_specification].format(nickname)
        if count == 1:
            if boost_specification == ANY:
                self._title = 'Defeat a {0}'.format(enemy_name)
                self._description = 'Defeat a {0} in combat. You do not have to score the last hit.'.format(enemy_name)
            else:
                self._title = 'Defeat an {0}{1}'.format(boost_string, enemy_name)
                self._description = 'Defeat an {0}{1} in combat. You do not have to score the last hit.'.format(boost_string, enemy_name)
        else:
            self._title = 'Defeat {0} {1}{2}s'.format(count, boost_string, enemy_name)
            self._description = 'Defeat {0} {1}{2}s in combat. You do not have to score the last hit.'.format(count, boost_string, enemy_name)

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['boosts'] = self._boosts
        save_data['boostt'] = self._boostt
        save_data['enemy_id'] = self._enemy_id
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._boosts = save_data['boosts']
        self._boostt = save_data['boostt']
        self._enemy_id = save_data['enemy_id']

    def get_enemy_id(self):
        return self._enemy_id

    def is_level(self, boost_level):
        if self._boosts == ANY:
            return True
        elif self._boosts == EQUAL:
            return boost_level == self._boostt
        elif self._boosts == LESS_EQ:
            return boost_level <= self._boostt
        elif self._boosts == GREATER_EQ:
            return boost_level >= self._boostt
        return False


class ItemQuest(Quest):
    def __init__(self):
        self._item_id = None
        super().__init__()

    def generate(self, item_id, count, *args):
        super().generate(count)
        self._item_id = item_id

    def get_item_id(self):
        return self._item_id

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['item_id'] = self._item_id
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._item_id = save_data['item_id']


class GatheringQuest(ItemQuest):
    def __init__(self):
        super().__init__()
        self._type = GATHERING

    def generate(self, drop_item_id, count, *args):
        super().generate(drop_item_id, count)

        item = Refs.gc.find_item(drop_item_id)
        item_name = item.get_name()
        if count == 1:
            self._title = 'Gather a {0}'.format(item_name)
            self._description = 'Gather a {0} from the dungeon. Buying this item will not count towards progress.'.format(item_name)
        else:
            self._title = 'Gather {0} {1}s'.format(count, item_name)
            self._description = 'Gather {0} {1}s from the dungeon. Buying this item will not count towards progress.'.format(count, item_name)


class ProgressQuest(Quest):
    def __init__(self):
        super().__init__()
        self._type = PROGRESS

    def generate(self, current_floor, floor_id, *args):
        super().generate(floor_id)
        self.set_progress(current_floor)

        number = Refs.gc.number_to_name(floor_id)
        self._title = f'Reach the {number} floor'
        self._description = f'Reach the end of the {number} floor and beat the floor boss.'


EXPLORATION_TYPE_TO_STIRNG = ['Encounter', 'Discover']
ENCOUNTER_NODE = 0
DISCOVER_NODE = 1


class ExplorationQuest(Quest):
    def __init__(self):
        self._exploration_type = None
        self._node_id = None
        super().__init__()
        self._type = EXPLORATION

    def generate(self, exploration_type, node_id, count, *args):
        self._exploration_type = exploration_type
        self._node_id = node_id  # Safe Zone, Material, Enemy
        super().generate(count)

        exploration_string = EXPLORATION_TYPE_TO_STIRNG[self._exploration_type]
        node_name = 'unknown'
        if count == 1:
            self._title = '{0} a {1} node in the dungeon'.format(exploration_string, node_name)
            self._description = 'Delve into the dungeon and {0} a {1} node while traversing the dungeon.'.format(exploration_string, node_name)
        else:
            self._title = '{0} {1} {2} node in the dungeon'.format(exploration_string, count, node_name)
            self._description = 'Delve into the dungeon and {0} {1} {2} node while traversing the dungeon.'.format(exploration_string, count, node_name)

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['exploration_type'] = self._exploration_type
        save_data['node_id'] = self._node_id
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._exploration_type = save_data['exploration_type']
        self._node_id = save_data['node_id']


class SurvivalQuest(Quest):
    def __init__(self):
        super().__init__()
        self._type = SURVIVAL

    def generate(self, count, *args):
        super().generate(count)

        if count == 1:
            self._title = 'Survive an encounter'
            self._description = 'Survive a single encounter in the dungeon. You must escape the dungeon for this to count.'
        else:
            self._title = 'Survive {0} encounters'.format(count)
            self._description = 'Survive {0} encounters in the dungeon. You must escape the dungeon for this to count.'.format(count)


class CraftingQuest(ItemQuest):
    def __init__(self):
        super().__init__()
        self._type = CRAFTING

    def generate(self, item_id, count, *args):
        super().generate(item_id, count)

        item = Refs.gc.find_item(item_id)
        item_name = item.get_name()
        if count == 1:
            self._title = 'Craft a {0}'.format(item_name)
            self._description = 'Craft a {0}. You will need the appropriate crafting skills.'.format(item_name)
        else:
            self._title = 'Craft {0} {1}s'.format(count, item_name)
            self._description = 'Craft {0} {1}s. You will need the appropriate crafting skills.'.format(count, item_name)

ABILITY_POINTS = 0
SKILL_POINTS   = 1
STATUS_SLOTS   = 2


class GrowthQuest(Quest):
    def __init__(self):
        self._growth_type = None
        super().__init__()
        self._type = GROWTH

    def generate(self, sub_type, count, *args):
        self._growth_type = sub_type
        super().generate(count)

    def get_growth_type(self):
        return self._growth_type

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['growth_type'] = self._growth_type
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._growth_type = save_data['growth_type']


ABILITY_POINT_TYPE_TO_STRING = ['', 'health', 'mana', 'strength', 'magic', 'endurance', 'agility', 'dexterity']
HEALTH    = 1
MANA      = 2
STRENGTH  = 3
MAGIC     = 4
ENDURANCE = 5
AGILITY   = 6
DEXTERITY = 7


class AbilityPointsGrowthQuest(GrowthQuest):
    def __init__(self):
        self._ability_points = None
        self._ability_pointt = None
        super().__init__()

    def generate(self, ability_point_specification, ability_point_type, count, *args):
        super().generate(ABILITY_POINTS, count)
        self._ability_points = ability_point_specification
        self._ability_pointt = ability_point_type

        point_name = ABILITY_POINT_TYPE_TO_STRING[ability_point_type]
        if count == 1:
            if self._ability_points == ANY:
                self._title = 'Gain an ability point'
                self._description = 'Fight in the dungeon enough to increase your adventurer\'s abilities by a point.'
            else:
                self._title = 'Gain a {0} ability point'.format(point_name)
                self._description = 'Fight in the dungeon enough to increase your adventurer\'s {0} abilities by a point.'.format(point_name)
        else:
            if self._ability_points == ANY:
                self._title = 'Gain {0} ability points'.format(count)
                self._description = 'Fight in the dungeon enough to increase your adventurer\'s abilities by {0} points.'.format(count)
            else:
                self._title = 'Gain {0} {1} ability points'.format(count, point_name)
                self._description = 'Fight in the dungeon enough to increase your adventurer\'s {0} abilities by {1} points.'.format(point_name, count)

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['ability_points'] = self._ability_points
        save_data['ability_pointt'] = self._ability_pointt
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._ability_points = save_data['ability_points']
        self._ability_pointt = save_data['ability_pointt']


class SkillPointsGrowthQuest(GrowthQuest):
    def generate(self, count, *args):
        super().generate(SKILL_POINTS, count)

        if count == 1:
            self._title = 'Gain a skill point'
            self._description = 'Collect money and relax in the tavern enough to gain a skill point.'
        else:
            self._title = 'Gain {0} skill points'.format(count)
            self._description = 'Collect money and relax in the tavern enough to gain {0} skill points.'.format(count)


class StatusSlotGrowthQuest(GrowthQuest):
    def __init__(self):
        self._status_slots = None
        self._status_slott = None
        super().__init__()

    def generate(self, status_slot_specification, status_slot_type, count, *args):
        super().generate(STATUS_SLOTS, count)
        self._status_slots = status_slot_specification
        self._status_slott = status_slot_type

        point_name = ABILITY_POINT_TYPE_TO_STRING[status_slot_type]
        if count == 1:
            if self._status_slots == ANY:
                self._title = 'Unlock a status board slot'
                self._description = 'Gather enough falna to unlock a status board slot for an adventurer.'
            else:
                self._title = 'Unlock a {0} status board slot'.format(point_name)
                self._description = 'Gather enough falna to unlock a {0} status board slot for an adventurer.'.format(point_name)
        else:
            if self._status_slots == ANY:
                self._title = 'Unlock {0} status board slots'.format(count)
                self._description = 'Gather enough falna to unlock {0} status board slots for your adventurers.'.format(count)
            else:
                self._title = 'Unlock {0} {1} status board slots'.format(count, point_name)
                self._description = 'Gather enough falna to unlock {0} {1} status board slots for your adventurers.'.format(count, point_name)

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['status_slots'] = self._status_slots
        save_data['status_slott'] = self._status_slott
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._status_slots = save_data['status_slots']
        self._status_slott = save_data['status_slott']


RANDOM_RECRUITMENT = 0
SPECIFIC_RECRUITMENT = 1


class RecruitmentQuest(Quest):
    def __init__(self):
        self._recruitment_type = RANDOM_RECRUITMENT
        super().__init__()
        self._type = RECRUITMENT

    def generate(self, count, *args):
        super().generate(count)

        if count == 1:
            self._title = 'Recruit an adventurer'
            self._description = 'Obtain materials and socialize in the tavern to recruit an adventurer.'
        else:
            self._title = f'Recruit {count} adventurers'
            self._description = f'Obtain materials and socialize in the tavern to recruit {count} adventurers.'

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['recruitment_type'] = self._recruitment_type
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._recruitment_type = save_data['recruitment_type']


class SpecificRecruitmentQuest(RecruitmentQuest):
    def __init__(self):
        self._char_id = None
        super().__init__()
        self._recruitment_type = SPECIFIC_RECRUITMENT

    def generate(self, char_id, *args):
        super().generate(1)

        char = Refs.gc.get_char_by_id(char_id)
        char_name = char.get_full_name()

        self._title = f'Recruit {char_name}'
        self._description = f'Obtain materials and socialize in the tavern to recruit {char_name}.'

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['char_id'] = self._char_id

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._char_id = save_data['char_id']


class TimeQuest(Quest):
    def check_time(self, current_time):
        pass

    def auto_update_progress(self):
        if self.is_finished():
            return
        time = datetime.now()
        self.check_time(time)


class LoginPeriodQuest(TimeQuest):
    def __init__(self):
        self._time_start = None
        self._time_end = None
        super().__init__()
        self._type = LOGIN_PERIOD

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['time_start'] = datetime.timestamp(self._time_start)
        save_data['time_end'] = datetime.timestamp(self._time_end)
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._time_start = datetime.fromtimestamp(save_data['time_start'])
        self._time_end = datetime.fromtimestamp(save_data['time_end'])
        return save_data

    def generate(self, time_start, time_end, *args):
        super().generate(1)
        self._time_start = time_start
        self._time_end = time_end

        if self._time_start.date() == self._time_end.date():
            stime = self._time_start.time()
            etime = self._time_end.time()
            self._title = f'Login from {stime.hour}:{stime.minute} to {etime.hour}:{etime.minute}'
            self._description = f'Login from {self._time_start.strftime("%I:%M %A, %B %d")} to {self._time_end.strftime("%I:%M %A, %B %d")}'
        else:
            sdate = self._time_start.date()
            stime = self._time_start.time()
            edate = self._time_end.date()
            etime = self._time_end.time()
            self._title = f'Login from {sdate.month}-{sdate.day}-{sdate.year} {stime.hour}:{stime.minute} to {edate.month}-{edate.day}-{edate.year} {etime.hour}:{etime.minute}'
            self._description = f'Login from {self._time_start.strftime("%I:%M %A, %B %d")} to {self._time_end.strftime("%I:%M %A, %B %d")}'

    def check_time(self, current_time):
        if self._time_start < current_time < self._time_end:
            self.add_progress(1)
            return True
        return False


class LoyaltyQuest(TimeQuest):
    def __init__(self):
        self._time_periods = []
        self._last_check_index = 0
        self._achieved = []
        super().__init__()
        self._type = LOYALTY

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        time_periods = []
        for (start_time, end_time) in self._time_periods:
            time_periods.append({
                'start_time': datetime.timestamp(start_time),
                'end_time': datetime.timestamp(end_time)
            })
        save_data['time_periods'] = time_periods
        save_data['last_index'] = self._last_check_index
        save_data['achieved'] = self._achieved
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        time_periods = []
        for time_period in save_data['time_periods']:
            start_time = datetime.fromtimestamp(time_period['start_time'])
            end_time = datetime.fromtimestamp(time_period['end_time'])
            time_periods.append((start_time, end_time))
        self._time_periods = time_periods
        self._last_check_index = save_data['last_index']
        self._achieved = save_data['achieved']

    def generate(self, time_periods, *args):
        self._time_periods = time_periods
        self._achieved = [False for _ in range(len(time_periods))]
        super().generate(len(time_periods))

        start_time, end_time = time_periods[0]
        time_delta = (end_time - start_time).seconds
        for (start_time, end_time) in time_periods[1:]:
            if (end_time - start_time).seconds != time_delta:
                return
        period = self.get_time_period_seconds(time_delta)
        self._title = f'Login {period}.'
        start_string = time_periods[0][0].strftime("%I:%M %A, %B %d")
        end_string = time_periods[-1][1].strftime("%I:%M %A, %B %d")
        self._description = f'Login {period} from {start_string} to {end_string}.'

    def set_goal(self, count):
        if 'every day' in self._title:
            self._title = self._title.replace('every day', f'at least {count} days this week')
            self._description = self._description.replace('every day', f'at least {count} days this week')
        if 'every week' in self._title:
            self._title = self._title.replace('every week', f'at least {count} weeks this month')
            self._description = self._description.replace('every week', f'at least {count} weeks this month')
        super().set_goal(count)

    def get_time_period_seconds(self, seconds):
        if seconds < 60:
            return f'every {seconds} seconds'
        elif seconds == 60:
            return f'every minute'
        else:
            return self.get_time_period_minutes(round(seconds / 60))

    def get_time_period_minutes(self, minutes):
        if minutes < 60:
            return f'every {minutes} minutes'
        elif minutes == 60:
            return f'every hour'
        else:
            return self.get_time_period_hours(round(minutes / 60))

    def get_time_period_hours(self, hours):
        if hours < 24:
            return f'every {hours} hours'
        elif hours == 24:
            return f'every day'
        else:
            return self.get_time_period_days(round(hours / 24))

    def get_time_period_days(self, days):
        if days < 7:
            return f'every {days} days'
        elif days == 7:
            return f'every week'
        else:
            return f'every {round(days / 7)} weeks'

    def check_time(self, current_time):
        for index, (start_time, end_time) in enumerate(self._time_periods[self._last_check_index:]):
            if current_time < start_time:
                return
            elif current_time < end_time:
                self._achieved[index] = True
                self._last_check_index += 1
                self.add_progress(1)
            else:
                continue

RANDOM_GROWTH = 0
SPECIFIC_GROWTH = 1


class RankGrowth(Quest):
    def __init__(self):
        self._growth_type = RANDOM_GROWTH
        super().__init__()

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['growth_type'] = self._growth_type
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._growth_type = save_data['growth_type']


class SpecificRankGrowth(RankGrowth):
    def __init__(self):
        self._char_id = None
        super().__init__()
        self._growth_type = SPECIFIC_GROWTH

    def generate(self, char_id, count, *args):
        self._char_id = char_id
        super().generate(count)

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['char_id'] = self._char_id
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._char_id = save_data['char_id']

    def is_char(self, char_id):
        return char_id == self._char_id


class RankUpQuest(RankGrowth):
    def __init__(self):
        super().__init__()
        self._type = RANK_UP

    def generate(self, count, *args):
        super().generate(count)

        if count == 1:
            self._title = 'Rank up an adventurer'
            self._description = 'Score the last hit on a strong monster to level up an adventurer.'
        else:
            self._title = f'Rank up adventurers {count} times'
            self._description = f'Score the last hit on a strong monster to level up {count} adventurers.'


class SpecificRankUpQuest(SpecificRankGrowth):
    def __init__(self):
        super().__init__()
        self._type = RANK_UP

    def generate(self, char_id, count, *args):
        super().generate(char_id, count)

        char = Refs.gc.get_char_by_id(char_id)
        char_name = char.get_full_name()
        number = Refs.gc.number_to_name(count, False)

        if count == 1:
            self._title = f'Rank up {char_name} once'
            self._description = f'Score the last hit on a strong monster to level up {char_name}.'
        else:
            self._title = f'Rank up {char_name} {number} times'
            self._description = f'Score the last hit on a strong monster to level up {char_name} {number} times.'


class RankBreakQuest(RankGrowth):
    def __init__(self):
        super().__init__()
        self._type = RANK_BREAK

    def generate(self, count, *args):
        super().generate(count)

        if count == 1:
            self._title = 'Rank break an adventurer'
            self._description = 'Overcome impossible odds to rank break an adventurer.'
        else:
            self._title = f'Rank break adventurers {count} times'
            self._description = f'Overcome impossible odds to rank break {count} adventurers.'


class SpecificRankBreakQuest(SpecificRankGrowth):
    def __init__(self):
        super().__init__()
        self._type = RANK_BREAK

    def generate(self, char_id, count, *args):
        super().generate(char_id, count)

        char = Refs.gc.get_char_by_id(char_id)
        char_name = char.get_full_name()
        number = Refs.gc.number_to_name(count, False)

        if count == 1:
            self._title = f'Rank break {char_name} once'
            self._description = f'Overcome impossible odds to rank break {char_name}.'
        else:
            self._title = f'Rank break {char_name} {number} times'
            self._description = f'Overcome impossible odds to rank break {char_name} {number} times.'

FAMILIARITY_RANDOM = 0
FAMILIARITY_SPECIFIC = 1


class FamiliarityQuest(Quest):
    def __init__(self):
        self._familiarity_type = FAMILIARITY_RANDOM
        super().__init__()
        self._type = FAMILIARITY

    def generate(self, familiarity, *args):
        super().generate(familiarity)

        self._title = f'Increase party familiarity by {familiarity}%'
        self._description = f'Improve the familiarity between your adventurers by {familiarity}%. The familiarity gain between two adventurers is only counted once.'

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['familiarity_type'] = self._familiarity_type
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._familiarity_type = save_data['familiarity_type']


class SpecificFamiliarityQuest(FamiliarityQuest):
    def __init__(self):
        self._target_1 = None
        self._target_2 = None
        super().__init__()
        self._familiarity_type = FAMILIARITY_SPECIFIC

    def generate(self, target_1_id, target_2_id, familiarity, *args):
        super().generate(familiarity)

        self._target_1 = target_1_id
        self._target_2 = target_2_id

        char_1 = Refs.gc.get_char_by_id(target_1_id)
        char_2 = Refs.gc.get_char_by_id(target_2_id)
        char_1_name = char_1.get_full_name()
        char_2_name = char_2.get_full_name()

        self._title = f'Increase familiarity of {char_1_name} and {char_2_name} by {familiarity}%'
        self._description = f'Delve into the dungeon with {char_1_name} and {char_2_name} to increase their familiarity by {familiarity}%.'

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        save_data['target_1'] = self._target_1
        save_data['target_2'] = self._target_2
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._target_1 = save_data['target_1']
        self._target_2 = save_data['target_2']

    def check_targets(self, target_1, target_2):
        return target_1 == self._target_1 and target_2 == self._target_2


class ScoreQuest(Quest):
    def __init__(self):
        super().__init__()
        self._type = SCORE

    def generate(self, current_score, goal_score, *args):
        super().generate(goal_score)
        self.set_progress(current_score)

        self._title = f'Reach the score {goal_score}'
        self._description = f'Improve your adventurers and their abilities to reach the party score {goal_score}.'

    def check_score(self, score):
        if score > self._progress:
            self.set_progress(score)

    def auto_update_progress(self):
        score = Refs.gc.get_current_party_score()
        self.check_score(score)


class CompletionQuest(Quest):
    def __init__(self):
        self._quests = None
        super().__init__()
        self._type = COMPLETION

    def generate(self, quest_list, *args):
        self._quests = quest_list
        super().generate(len(quest_list))
        self._title = 'Complete All Quests'
        self._description = 'Complete '
        for quest in self._quests:
            self._description += quest.get_title()
            self._description += ', '
        self._description = self._description[:-2]
        self._description, last_title = self._description.rsplit(', ', 1)
        self._description += f', and {last_title} quests.'

    def auto_update_progress(self):
        all_completed = True
        for quest in self._quests:
            all_completed &= quest.is_finished()

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        quest_list = []
        for quest in self._quests:
            quest_list.append(quest.get_hash())
        save_data['quest_list'] = quest_list
        return save_data

    def load_from_data(self, save_data, manager):
        super().load_from_data(save_data, manager)
        self._quests = save_data['quest_list']

    def form_memory_links(self, manager):
        quest_list = []
        for quest_hash in self._quests:
            quest = manager.find_quest_by_hash(quest_hash)
            quest_list.append(quest)
        self._quests = quest_list


class CompletionStackQuest(Quest):
    def __init__(self):
        self._quest_stacks = None
        super().__init__()
        self._type = STACK_COMPLETION

    def generate(self, quest_stack_list, completion_type, *args):
        self._quest_stacks = quest_stack_list
        quest_count = 0
        for quest_stack in quest_stack_list:
            quest_count += len(quest_stack)
        super().generate(quest_count)
        self._title = f'Complete All {completion_type} Quests'
        self._description = 'Complete '
        for quest_stack in self._quest_stacks:
            for quest in quest_stack:
                self._description += quest.get_title()
                self._description += ', '
        self._description = self._description[:-2]
        self._description, last_title = self._description.rsplit(', ', 1)
        self._description += f', and {last_title} quests.'

    def auto_update_progress(self):
        quest_count = 0
        for quest_stack in self._quest_stacks:
            for quest in quest_stack:
                if quest.is_finished():
                    quest_count += 1
        self.set_progress(quest_count)

    def get_data_to_save(self, manager):
        save_data = super().get_data_to_save(manager)
        quest_stack_list = []
        for quest_stack in self._quest_stacks:
            if quest_stack is None:
                continue
            quest_stack_list.append(quest_stack.get_hash())
        save_data['quest_stack_list'] = quest_stack_list
        return save_data

    def load_from_data(self, manager, save_data):
        super().load_from_data(manager, save_data)
        self._quest_stacks = save_data['quest_stack_list']

    def form_memory_links(self, manager):
        quest_stack_list = []
        for quest_stack_hash in self._quest_stacks:
            quest_stack = manager.find_quest_stack_by_hash(quest_stack_hash)
            quest_stack_list.append(quest_stack)
        self._quest_stacks = quest_stack_list
