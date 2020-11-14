class DungeonBattle(Screen):
    level = NumericProperty(1)
    boss = BooleanProperty(False)
    level_label = ObjectProperty(None)
    encounterLabel = ObjectProperty(None)
    turn_label = ObjectProperty(None)
    currentTurn = NumericProperty(1)

    def __init__(self, boss, encounternum, floor, floorManager, **kwargs):
        super(DungeonBattle, self).__init__(**kwargs)
        self.chars = []
        self.floor = floor
        self.floorManager = floorManager
        self.boss = boss
        self.level = self.floor.floornum
        if (self.boss):
            self.level_label.text = 'Level %d BOSS' % self.level
            self.encounter_label.text = ''
        else:
            self.level_label.text = 'Level %d' % self.level
            self.encounter_label.text = 'Encounter %d' % encounternum
        if self.boss:
            self.enemies = self.floor.generateBoss()
        else:
            self.enemies = self.floor.generateEnemies()
        # self.enemyLocations = ((1500, 800), (1500, 1000), (1500, 600), (1700, 700), (1700, 900), (1700, 1100), (1700, 500), (1500, 1200), (1500, 400), (1900, 800), (1900, 1000), (1900, 600))
        # self.enemyAmounts = (3, 3, 4, 5, 6)

    def run(self):
        anim = Animation(opacity=0, duration=2.5)
        anim.start(self.level_label)
        anim = Animation(opacity=0, duration=3.5)
        anim.start(self.encounter_label)
        Clock.schedule_once(lambda dt: self.make_gui(), 4)

    def on_currentTurn(self, *args):
        self.turn_label.text = 'Turn: %d' % self.currentTurn
        self.textbox.text = self.textbox.text + "\nIt is now turn %d!" % self.currentTurn

    def make_gui(self):
        currentparty = []
        # print(str("Showing GUI"))
        self.turn_label.text = 'Turn: %d' % self.currentTurn
        self.attackButton = customButton(size=(270, 180), source='res/AttackButton.png', pos=(2000, 100),
                                         size_hint=(None, None), on_touch_down=self.attack)
        self.add_widget(self.attackButton)
        self.text = ScrollView(size=(2160, 890), pos=(200, 370), size_hint=(None, None), do_scroll_x=False)
        self.textbox = TextInput(text="You have delved into the dungeon!", size=(2160, 890), size_hint=(None, None),
                                 pos=(200, 370), multiline=True, readonly=True)
        self.text.add_widget(self.textbox)
        self.add_widget(self.text)
        count = 0
        for x in range(len(App.currentparty)):
            if not App.currentparty[x] == None:
                char = App.characterArray[App.currentparty[x]]
                self.textbox.text = self.textbox.text + "\n" + char.getdisplayname() + " has entered the dungeon!"
                preview = CharPreview(char, (250 * count + 200, 50))
                self.chars.append(preview)
                preview.id = 'charid%d' % x
                preview.source = char.getpreviewimage()
                count += 1
                self.add_widget(preview)

        if self.boss:
            self.textbox.text = self.textbox.text + "\nBOSS Encountered!"
        else:
            self.textbox.text = self.textbox.text + "\nEnemies Encountered!"
        for x in self.enemies:
            self.textbox.text = self.textbox.text + "\nA " + x.name + " appears! " + str(x.health) + " health."

        # for x in range(len(currentparty)):
        #     # print(currentparty[x].getname() + shownparty[x].getname())
        #     preview = CharPreview(currentparty[x])
        #     sprite = Image()
        #     sprite.id = 'sprite%d' % x
        #     sprite.source = currentparty[x].getsprite()
        #     sprite.center = 450, 600 + (200*x)
        #     sprite.size = 200, 200
        #     sprite.keep_ratio = True
        #     sprite.allow_stretch = True
        #     sprite.size_hint = None, None
        #     preview.id = 'charid%d' % x
        #     preview.source = currentparty[x].getpreviewimage()
        #     preview.pos = (225 * x + 200, 50)
        #
        #     self.main_layout.add_widget(sprite)
        #     self.screen.add_widget(preview)
        # numofenemys = random.randint(0, self.enemyAmounts[0]-1) + 1 #generate enemys
        # for x in range(numofenemys):
        #     enemy = Enemy()
        #     enemy.health = 100
        #     enemy.id = 'enemy%d' % x
        #     enemy.source = 'res/wolf.gif'
        #     enemy.size = 200, 200
        #     enemy.size_hint = None, None
        #     enemy.center = self.enemyLocations[x]
        #     self.enemy_layout.add_widget(enemy)
        # bar = MoveBarObject()
        # self.main_layout.add_widget(bar)

    def moveBarPressed(self, char):
        pass

    def attack(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if not instance.disabled:
                objects = []
                speeds = []
                attackOrder = []
                for x in self.chars:
                    speeds.append(x.char.generateSpeed())
                    objects.append(x)
                for x in self.enemies:
                    speeds.append(x.generateSpeed())
                    objects.append(x)
                for x in range(len(speeds)):
                    y = speeds.index(min(speeds))
                    attackOrder.append(objects.pop(y))
                    speeds.pop(y)

                for x in attackOrder:
                    if isinstance(x, Enemy):
                        move = x.generateMove()
                        damage = move.generateDamage(x.str, x.mag)
                        nextUndead = self.next_undead(self.chars)
                        if move.getname() == "EnmyAttack":
                            self.textbox.text = self.textbox.text + "\n " + x.name + " attacks " + nextUndead.char.getname() + "!"
                        else:
                            self.textbox.text = self.textbox.text + "\n " + x.name + " attacks " + nextUndead.char.getname() + " with " + move.getname() + "!"
                        damage = nextUndead.processDamage(damage, x.agi)
                        if damage > 0:
                            self.textbox.text = self.textbox.text + " " + x.name + " deals " + str(
                                damage) + " damage to " + nextUndead.char.getname() + "!"
                            if nextUndead.health > 0:
                                self.textbox.text = self.textbox.text + " " + nextUndead.char.getname() + " took " + str(
                                    damage) + " damage. Health is now: " + str(nextUndead.health)
                            else:
                                self.textbox.text = self.textbox.text + " " + nextUndead.char.getname() + " is now dead."
                        # finish enemy attack against a single char, if multi move than attack all. Add a attack targeting type to move class
                        # Add player addack all enemies targeting. Add countering. Add guarding as the endurance block. Add Critical hits. Add penetration as agi boost
                        # Move bar, mp from attacks, drop items. look at danmachi wiki
                        # Add Unguard type to moves. Fix ascend. Add more floors. Add character death.
                    else:
                        # print(str(x.ids.move_box.text))
                        move = x.char.getmove(x.selectedMove)
                        self.textbox.text = self.textbox.text + "\n" + x.char.getdisplayname() + " uses " + move.getname() + "!"
                        damage = move.generateDamage(x.char.totalPhysicalAttack, x.char.totalMagicalAttack)
                        if len(self.enemies) > 0:
                            damage = self.enemies[0].processDamage(damage, x.char.totalAgility)
                            if damage > 0:
                                self.textbox.text = self.textbox.text + " " + x.char.getdisplayname() + " deals " + str(
                                    damage) + " damage to " + self.enemies[0].name + "."
                                if self.enemies[0].health > 0:
                                    self.textbox.text = self.textbox.text + " " + self.enemies[0].name + " took " + str(
                                        damage) + " damage. Health is now: " + str(self.enemies[0].health)
                                else:
                                    self.textbox.text = self.textbox.text + " The " + self.enemies[
                                        0].name + " is now dead."
                                    self.enemies.remove(self.enemies[0])
                            else:
                                self.textbox.text = self.textbox.text + " " + x.char.getdisplayname() + " deals no damage to " + \
                                                    self.enemies[0].name + "."
                if len(self.enemies) == 0:
                    self.textbox.text = self.textbox.text + "\n" + "This encounter has been won!"
                    self.attackButton.disabled = True
                    self.winBackground = Image(source='res/SuccessBackground.png', size_hint=(None, None), pos=(0, 0),
                                               size=(2560, 1440), opacity=0)
                    self.winLabel = Label(text='Success!', size_hint=(None, None), pos=(1280, 720), font_size=120,
                                          color=(.2, 0, .65, 1))
                    self.add_widget(self.winBackground)
                    self.winBackground.add_widget(self.winLabel)
                    anim = Animation(opacity=1, duration=3.5)
                    anim.start(self.winBackground)
                    anim = Animation(opacity=1, duration=2.5)
                    anim.start(self.winLabel)
                    Clock.schedule_once(lambda dt: self.floorManager.run(), 4)
                    # print(str(damage))
                    # print()

                # print all moves
                # for fights lasting more than 15 turns, incur a 10% speed penalty and a 5% attack penalty
                # for fights lasting more than 20, incur an addl 10% speed penalty and a 10% attack penalty
                # for fights lasting more than 25 turns incur an addl 10% speed penalty and a 10% attack penalty

                self.currentTurn += 1
                # print("Turn %d" % self.currentTurn)
                # self.textbox.text = self.textbox.text + "It is now turn %d!" % self.currentTurn
            # print("Turn: " + str(self.currentTurn))
            # numofchars = 4
            # maxfoes = len(self.enemy_layout.children)
            # if (maxfoes > 0):
            #     for y in range(maxfoes):
            #         print("Enemy #%d" % y)
            #         print("\tHealth: " + str(self.enemy_layout.children[maxfoes - 1 - y].health))
            #     for x in range(numofchars):
            #         maxfoes = len(self.enemy_layout.children)
            #         if maxfoes > 0:
            #             attack = self.children[numofchars - 1 - x].char.getmove(self.children[numofchars - 1 - x].selectedMove)
            #             foenum = -1
            #             if attack.ttype == 0:
            #                 foenum = attack.findfoe(maxfoes-1)
            #             print("DEBUG: " + str(foenum) + " " + str(maxfoes))
            #             print("\u001B[32m" + self.children[numofchars-1-x].char.getname() + " uses " + attack.name)
            #             print("\tAttack Targeting Type: " + str(attack.ttypeS))
            #             print("\tAttack Type: " + attack.type)
            #             damage = attack.generateDamage(self.children[numofchars - 1 - x].char.getattack(attack.type))
            #             print("\tAttack Damage: " + str(damage) + "\u001B[29m")
            #             if foenum == -1:
            #                 pass
            #             else:
            #                 health = self.enemy_layout.children[maxfoes - 1 - foenum].health
            #                 self.enemy_layout.children[maxfoes - 1 - foenum].health = health - damage
            #                 health = self.enemy_layout.children[maxfoes - 1 - foenum].health
            #                 if (health < 0):
            #                     print("\u001B[31mEnemy #" + str(foenum) + " defeated! Removed from children list.\u001B[29m")
            #                     self.enemy_layout.remove_widget(self.enemy_layout.children[maxfoes - 1 - foenum])
            #                 print("\u001B[33mEnemy #" + str(foenum) + " takes " + str(damage) + " damage. Health is now " + str(health) + "\u001B[29m")
            #         else:
            #             print("You have won!")
            #             break

    @staticmethod
    def next_undead(chars):
        return all(chars.health > 0)