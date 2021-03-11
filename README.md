# CoatiraneAdventures
Coatirane Adventures - A RPG dungeon crawler inspired by memoria freese

Heavily relies on concepts introduced by Danmachi / Is it Wrong to Try to Pick up Girls in a Dungeon?, such as the idea of a dungeon, and the leveling and progression system.

You are a diety, a being that lives on another plane of existance, and as a vacation from your normal work, you are allowed to travel to Gekkai (Lower World), and partake in their activities. One thing that intrests you most about this world is Coatirane, a small town that is built around a dungeon, and is home to many adventurers who delve into its depths in search of treasure. With your power, you can bestow adventurers with skills and magic, allowing them to grow far stronger than they could normally and join you family, as you guide them in the dungeon.

As a deity, you have a name, a domain, and a symbol. In the physical prototype, the symbol doesn't affect anything and is not included, but your domain is what you are the god of. There are many options, such as battle, which will increase your adventurers fighting prowess or crafting which helps your adventurers be better at crafting. There will also be skill trees that you can invest points in when you grow as a family, and unlock new things such as teach adventurers how to be crafters or smiths or potioneers, etc. There will also be general perks that give more power or boost to your family.

The adventurers themselves are gained by recruitment around town, and each adventurer can be leveled from Rank 1 → 10. Each rank, the adventurer has a status board - that must be fully unlocked - giving them higher stats as well as rank growths - increased by fighting in the dungeon - before you can increase their rank. Increasing a adventurers rank allows them to gain new skills and abilities. Skills are predetermined and unlocked at different levels, and abilities are chosen and are dependent on what that specific adventurer has done. To increase in rank, and adventurer must defeat or score the last hit on a monster or boss that is at least one rank above them.

There is also a slew of equipment that you can craft and equip on your adventurers. Equipment can give a great boost to your adventurers early on, but becomes very expensive and resourse intensive later on.

In terms of getting resources, when in the dungeon, you can mine, hack, and dig to try to find gems, ore, and other resources within the dungeon. Resources and monsters spawn in certain areas on floors, and can either be found by consulting a resourse map or by trial and error. The dungeon itself is a maze, containing one entrance and one exit, and a single path between the two. Moving around the dungeon, agthering resources, and fighting enemies consumes stamina, which can only be recovered by resting in a safe zone, which are in some, but not all, dead ends. Running out of stamina or losing all health will render a character incapacitated, and when incapicatated, a cahracter will increase the stamina consumption of all other characters. When all chagracters are incapacitated, you lose and must restore from a save. The game is saved every entrance or exit from a floor and can be saved any time in the town as well as upon exit. You can also use potions to restore health or stamia, but be sure to balance reward vs risk and ensure you don't run out.

There are two different types of adventurers, adventurers and supporters. Adventurers are the ones that have skills, and do the fighting, while supporters lend their stats to the adventurers they are assigned to and use special skills to improve stats or other boost during battle. Supporters do not have stamina and cannot perform actions in the dungeon, but do double the amount of stamina an adventurer has if they are assigned to them. Supporters are an excellent way to give a large stat boost to an adventuer, many times essentially doubling fighting power.

Of adventurers and supporters, there are five different combat types, Physical, Magical, Hybrid, Healing and Defensive. There are also seven different elements, Earth, Water, Fire, Wind, Thunder, Light and Dark. Adventurers with element will be more effective or less effective against monsters with corresponding elements. The same goes for attack types. The element wheel is Earth → Thunder → Water → Fire → Wind → Earth & Light ↔ Dark

For example, Goblins are Physical, Earth and Dark types, and are weak from Magical, Wind and Light adventurers. Hybrid adventurers are considered to be a blend of magical and physical.

When performing actions within the dungeon (fighting, moving, harvesting), adventuerers gain stats proportinate to what they did and how well they did it. This allows you to grind certain stats such as agility by running around, or strength by mining. Magic is harder to increase, as it can only be increased during battle.

Crafting items, such as equipment, potions or other items, can only be done when a adventurer or supporter in your family has the corresponding perk. Some adventurers/supporters will already have this perk or can be given it through the skill tree. This will require you to purchase a lot of equipment and items at first, but save a lot in the long run by making items yourself with items you gain yourself.

In the long run - Things to consider for game balance
Eventually, this will be a psuedo multiplayer game. While fighting is strictly turn based currently, battling will be gesture and time based in the long run, where 1 turn is equivilent to around 5 seconds. You will be able to delve into the dungeon with friends, having at least 1 of the 8 slots be from each person playing, up to a total of 8 people. There will also be a special mode, expeditions, where each player, of up to four players all delve into the dungeon with 8 characters, and have to name a succession order, as you can only have 8 characters at a single time. Characters that are not in that cound of 8 will not impact the game until utilized. This is for the ultimate goal of getting much further in the dungeon than possible with just eight characters. This is likely going to be difficult to implement however, and will most likely not be in the version of the game that is reasleased at the end of my capstone.

## Physical Prototype
- First Release → 3/26/2021

The physical prototype is a text based adventure version of the full game that makes use of a different screen manager, but operated on entierly the same backend code, so that the digital prototype will only require a facelift to work exactly the same. All saves and data will easily translate.

The main file for the physical prototype is `src/text_main.py` and mainly uses the files in `src/game`, `src/loading`, and `src/text`. `src/spine`, `src/lwf`, and `src/uix` are not utilized at all and are solely for the digital prototype.

## Digital Prototype

...

## Tools
A random assortment of helpful tools to better generate data for the game.
