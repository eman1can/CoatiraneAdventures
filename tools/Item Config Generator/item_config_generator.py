from random import choices, randint

compass = 'S, compass, Compass, general, single, 375\nnone\nHave trouble getting lost? Buy a compass and never get lost again!'
pocket_watch = 'S, pocket_watch, Pocket Watch, general, single, 375\nnone\nKeep losing track of time? Buy a watch and always know the time!'

tool_types = ['harvesting_knife', 'pickaxe', 'shovel', 'axe']
soft_materials = ['cloth', 'padded', 'leather', 'hardened_leather']
hard_materials = ['tin', 'copper', 'bronze', 'iron', 'steel', 'platinum', 'titanium', 'hardened_steel', 'tungsten', 'tungsten_carbide', 'dark steel', 'mithril', 'meteoric_iron', 'adamantite', 'golanthium', 'trinium']

magic_stone_types = ['tiny', 'small', 'medium', 'regular', 'large', 'huge']

"""
When a monster is killed:
- Non-havesting items dropped (Such as Egg)
- Use harvesting knife:
  - Magic Stones
  - Harvest Drops
    - Might consume items such as vials (for blood, venom), container (meat, tongue) 
  - Falna

On a floor, every time you move there is a 15% chance to have an encounter.
On specific nodes for each monster, the chance for that monster appearing is increased 10%, and all other monsters are reduced in equal amounts. On a node, monsters are 15% stronger, and encounters have a 25% chance to happen.
When mining/digging/chopping at the dungeon, there is a 5% chance to get a resource (1-2 units), and the resource is either a random gem, or a metal with the hardness corresponding to the floor. When mining/digging/chopping on a resource node, there is an 85% chance to get the corresponding resource. (2-10 units)
A tile that has a safe zone node has to made into a safe zone, and then will have a 0% encounter chance and allow for rest for 5 movement turns.
When using a material that has a hardness lower than the resource, success is reduced by 10% for every 1 hardness below. For every 1 hardness above a resource type, increase yield by 5% and increase chance of success by 5%.

When crafting an item, whatever equipment you are trying to craft will have a material unit amount for each type of material needed, and the higher the hardness of the ingredients, the higher the item stats.
An item can have up to three materials for the main material, and a main materials for the other requirements.
Each material will give effects to the resulting item.
The current softest (hard)material is tin at 1.5 hardness. The current hardest (hard)material is Trinium at 15.0-16.0 hardness.

Ex: Longsword
 - 15 Units hard material
 - 2 Units soft material
 
 - 10 Units Bronze (Hardness 3.0)
 - 2.5 Units Unicorn Horn (Hardness 3.5)
 - 2.5 Units Goblin Fang (Hardness 2.0)
 - 2 Units Imp Hide

    Hardness:
     Max: (3.0 * 10 + 3.5 * 2.5 + 2.0 * 2.5) / 15 = 2.9
     Min: (3.0 * 10 + 3.5 * 2.5 + 2.0 * 2.5) / 15 = 2.9
     Random from 2.9 → 2.9
    Effects:
        Element: Normal (Bronze - Defining)
        - Ailment Resist 100% (Unicorn Horn - Sub)
        - 10% Chance to inflict weak sickness (Goblin Fang - Sub)
        - 10% Chance to attack with dark element (Imp Hide - Sub)

Ex: Dagger
 - 5 Units hard material
 - 1 Unit soft material
 
 - 3 Units Goblin Fang (Hardness 2.0)
 - 1 Unit Titanium (Hardness 6.0)
 - 1 Unit Siren Fang (Hardness 5.5)
 
    Hardness:
    Max: (2.0 * 3 + 6.0 * 1 + 5.5 * 1) / 5 = 3.5
    Min: (2.0 * 3 + 6.0 * 1 + 5.5 * 1) / 5 = 3.5
    Random from 3.5 → 3.5
    Effects:
        Element: Dark (Goblin Fang - Defining)
        - 50% Chance to inflict strong sickness (Goblin Fang - Defining)
        - 10% Chance to inflict daze (Siren Fang - Sub)
"""

# List of current materials (soft) (natural)
# Cloth 0.5
# Padded 0.75
# Leather 1.0
# Hardened Leather 1.5
#
# List of current materials (hard) (natural)
# Tin 1.5
# Cadmium 2.0
# Coal 2.0-2.5
# Zinc 2.5
# Silver 2.5-3.0
# Copper 3.0
# Iron 4.5
# Platinum 4.0-4.5
# Titanium 6.0
# Tungsten 7.5
# Meteoric Iron 10.5-11.0
# Golanthium 13.0-15.0
#
# Item weight = Hardness * item units
# Weight limit = Str * 5
# Ex. A adventurer with Str. 4 can carry total equipment worth
# 20 weight units.
# For every 2.5 weights units above weight limit, reduce stats by 5%

# List of current materials (hard) (alloys)
# Bronze 3.0
# - 2 units copper
# - 1 units tin
# → 2 units bronze
# Defining Effect (weapon): Elemental Boost Damage +100%
# Defining Effect (armor): Elemental Resist +50%
# Sub Effect (weapon): Elemental Boost Damage +50%
# Sub Effect (armor): Elemental Resist +15%
# Steel 5.0-5.5
# - 3 units iron
# - 2 units coal
# → 2 units steel
# Defining Effect: Durability +100%
# Sub Effect: Durability +50%
# Hardened Steel 7.0-8.0
# - 5 units iron
# - 3 units coal
# - 2 units titanium
# → 5 units hardened steel
# Defining Effect: End. +100% (Item only)
# Sub Effect: End. +25%
# Tungsten Carbide 8.5-9.0
# - 2 units tungsten
# - 2 units coal
# → 2 units tungsten carbide
# Defining Effect: All equipment weight reduced by half.
# Sub Effect: All equipment weight reduced by a quarter.
# Dark Steel 9.0-9.5
# - 2 units hardened steel
# - 2 units tungsten carbide
# → 2 units dark steel
# Defining Effect: Increase Dark Atk. Dmg. by 100%. Dark Resist 100%.
# Sub Effect: Increase Dark Atk. Dmg. by 25%. Increase Dark Resist by 25%.
# Mithril 9.5-10.5
# - 2 units silver
# - 2 units dark steel
# → 2 units mithril
# Defining Effect: Mag. +50%
# Sub Effect: Mag. +50% (Item Only)
# Adamantite 11.0-13.0
# - 2 units mithril
# - 2 units meteoric iron
# → 2 units adamantite
# Defining Effect: Increase power level by 2 when using skill. (Can only happen once) Ex. Lo → High, High → Super
# Sub Effect: Increase power level by 1 when using skill. (Can only happen once) Ex. Lo → Mid, Mid → High
# Trinium 15.0-16.0
# - 2 units Adamantite
# - 2 units golanthium
# → 2 units Trinium
# Defining Effect: All Stats +25%
# Sub Effect: All Stats +25% (Item Only)

# Chrysocolla 2.5-3.5
# Serpentine 3.0-6.0
# Azurite 3.5-4.0
# Malachite 3.5-4.0
# Rhodochrosite 3.5-4.0
# Ammolite 3.5-4.5
# Fluorite 4.0
# Kyanite 4.5-7.0
# Apatite 5.0
# Lapis Lazuli 5.0-5.5
# Titanite 5.0-5.5
# Obsidian 5.0-6.0
# Turquoise 5.0-6.0
# Opal 5.5-6.0
# Rhodonite 5.5-6.0
# Sodalite 5.5-6.0
# Diopside 5.5-6.5
# Tanzanite 6-6.5
# Indraneelam 6.0
# Andesine 6.0-6.5
# Labradorite 6.0-6.5
# Moonstone 6.0-6.5
# Prehnite 6.0-6.5
# Sunstone 6.0-6.5
# Zoisite 6.0-6.5
# Blizzard Stone 6.0-7.0
# Jade 6.0-7.0
# Zoisite 6.0-7.0
# Aventurine 6.5
# Petalite 6.5
# Spectrolite 6.5
# Agate 6.5-7.0
# Jasper 6.5-7.0
# Kunzite 6.5-7.0
# Onyx 6.5-7.0
# Peridot 6.5-7.0
# Garnet 6.5-7.5
# Garnet 6.5-7.5
# Hessonite 6.5-7.5
# Amethyst 7.0
# Ametrine 7.0
# Bloodstone 7.0
# Citrine 7.0
# Quartz 7.0
# Rutilated Quartz 7.0
# Spessartite 7.0
# eye 7.0 Tiger
# Danburite 7.0-7.5
# Iolite 7.0-7.5
# Tsavorite 7.0-7.5
# Zircon 7.5
# Aquamarine 7.5-8.0
# Beryl 7.5-8.0
# Bixbite 7.5-8.0
# Emerald 7.5-8.0
# Goshenite 7.5-8.0
# Heliodor 7.5-8.0
# Morganite 7.5-8.0
# Spinel 7.5-8.0
# Topaz 8.0
# Chrysoberyl 8.5
# Taaffeite 8.5
# Sang-E-Maryam 8.6
# Neelam 9.0
# Padparadscha 9.0
# Ruby 9.0
# Sapphire 9.0




# Floor Hardness (What hardness you need to mine / dig (Mining is 60%(ore)/40%(gem), Digging is 40%(ore)/60%(gem)))
# Floor 1 → Hardness 1.0
#    - None
#
# Floor 2 → Hardness 1.0
#    - None
#
# Floor 3 → Hardness 1.5
#    - None
#
# Floor 4 → Hardness 1.5
#    - None
#
# Floor 5 → Hardness 2.0
#    - Tin
#
# Floor 6 → Hardness 2.0
#    - Tin
#
# Floor 7 → Hardness 2.5
#    - Cadmium, Tin, Coal
#
# Floor 8 → Hardness 3.0
#    - Zinc, Cadmium, Tin, Silver, Coal
#    - Chrysocolla
#
# Floor 9 → Hardness 3.0
#    - Zinc, Cadmium, Tin, Silver, Coal
#    - Chrysocolla
#
# Floor 10 → Hardness 3.0
#    - Zinc, Cadmium, Tin, Silver, Coal
#    - Chrysocolla
#
# Floor 11 → Hardness 3.5
#    - Zinc, Cadmium, Silver, Coal, Copper
#    - Serpentine, Chrysocolla
#
# Floor 12 → Hardness 3.5
#    - Zinc, Cadmium, Silver, Coal, Copper
#    - Serpentine, Chrysocolla
#
# Floor 13 → Hardness 3.5
#    - Zinc, Cadmium, Silver, Coal, Copper
#    - Serpentine, Chrysocolla
#
# Floor 14 → Hardness 4.0
#    - Zinc, Silver, Coal, Copper
#    - Malachite, Azurite, Ammolite, Serpentine, Rhodochrosite, Chrysocolla
#
# Floor 15 → Hardness 4.5
#    - Platinum, Silver, Copper
#    - Malachite, Azurite, Ammolite, Serpentine, Rhodochrosite, Chrysocolla, Fluorite
#
# Floor 16 → Hardness 4.5
#    - Platinum, Silver, Copper
#    - Malachite, Azurite, Ammolite, Serpentine, Rhodochrosite, Chrysocolla, Fluorite
#
# Floor 17 → Hardness 5.0
#    - Platinum, Iron
#    - Malachite, Azurite, Ammolite, Serpentine, Rhodochrosite, Kyanite, Chrysocolla, Fluorite
#
# Floor 18 → Hardness 5.0
#    - Platinum, Iron
#    - Malachite, Azurite, Ammolite, Serpentine, Rhodochrosite, Kyanite, Chrysocolla, Fluorite
#
# Floor 19 → Hardness 5.5
#    - Platinum, Iron
#    - Malachite, Apatite, Azurite, Lapis Lazuli, Turquoise, Ammolite, Serpentine, Obsidian, Titanite, Rhodochrosite, Kyanite, Chrysocolla, Fluorite
#
# Floor 20 → Hardness 5.5
#    - Platinum, Iron
#    - Malachite, Apatite, Azurite, Lapis Lazuli, Turquoise, Ammolite, Serpentine, Obsidian, Titanite, Rhodochrosite, Kyanite, Chrysocolla, Fluorite
#
# Floor 21 → Hardness 6.0
#    - Platinum, Iron
#    - Malachite, Apatite, Azurite, Lapis Lazuli, Turquoise, Diopside, Ammolite, Rhodonite, Serpentine, Obsidian, Titanite, Rhodochrosite, Kyanite, Chrysocolla, Opal, Sodalite, Fluorite
#
# Floor 22 → Hardness 6.0
#    - Platinum, Iron
#    - Malachite, Apatite, Azurite, Lapis Lazuli, Turquoise, Diopside, Ammolite, Rhodonite, Serpentine, Obsidian, Titanite, Rhodochrosite, Kyanite, Chrysocolla, Opal, Sodalite, Fluorite
#
# Floor 23 → Hardness 6.5
#    - Titanium
#    - Malachite, Tanzanite, Prehnite, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Kyanite, Sodalite, Indraneelam, Apatite, Andesine, Rhodonite, Fluorite, Azurite, Lapis Lazuli, Diopside, Obsidian, Chrysocolla, Opal, Blizzard Stone, Turquoise, Sunstone, Moonstone, Zoisite
#
# Floor 24 → Hardness 6.5
#    - Titanium
#    - Malachite, Tanzanite, Prehnite, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Kyanite, Sodalite, Indraneelam, Apatite, Andesine, Rhodonite, Fluorite, Azurite, Lapis Lazuli, Diopside, Obsidian, Chrysocolla, Opal, Blizzard Stone, Turquoise, Sunstone, Moonstone, Zoisite
#
# Floor 25 → Hardness 7.0
#    - Titanium
#    - Malachite, Tanzanite, Prehnite, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Kyanite, Sodalite, Indraneelam, Apatite, Andesine, Rhodonite, Onyx, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Spectrolite, Obsidian, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Peridot, Sunstone, Petalite, Moonstone, Zoisite, Agate, Kunzite
#
# Floor 26 → Hardness 7.0
#    - Titanium
#    - Malachite, Tanzanite, Prehnite, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Kyanite, Sodalite, Indraneelam, Apatite, Andesine, Rhodonite, Onyx, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Spectrolite, Obsidian, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Peridot, Sunstone, Petalite, Moonstone, Zoisite, Agate, Kunzite
#
# Floor 27 → Hardness 7.0
#    - Titanium
#    - Malachite, Tanzanite, Prehnite, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Kyanite, Sodalite, Indraneelam, Apatite, Andesine, Rhodonite, Onyx, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Spectrolite, Obsidian, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Peridot, Sunstone, Petalite, Moonstone, Zoisite, Agate, Kunzite
#
# Floor 28 → Hardness 7.5
#    - Titanium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Andesine, Rhodonite, Iolite, Onyx, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Peridot, Sunstone, Tsavorite, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 29 → Hardness 7.5
#    - Titanium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Andesine, Rhodonite, Iolite, Onyx, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Peridot, Sunstone, Tsavorite, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 30 → Hardness 7.5
#    - Titanium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Andesine, Rhodonite, Iolite, Onyx, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Peridot, Sunstone, Tsavorite, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 31 → Hardness 8.0
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sunstone, Tsavorite, Heliodor, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 32 → Hardness 8.0
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sunstone, Tsavorite, Heliodor, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 33 → Hardness 8.0
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sunstone, Tsavorite, Heliodor, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 34 → Hardness 8.5
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 35 → Hardness 8.5
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 36 → Hardness 8.5
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 37 → Hardness 9.0
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 38 → Hardness 9.0
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 39 → Hardness 9.0
#    - Tungsten
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Aquamarine, Citrine, Spectrolite, Obsidian, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 40 → Hardness 9.5
#    -
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 41 → Hardness 9.5
#    -
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 42 → Hardness 9.5
#    -
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 43 → Hardness 10.0
#    -
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 44 → Hardness 10.5
#    -
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 45 → Hardness 11.0
#    - Meteoric Iron
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 46 → Hardness 11.5
#    - Meteoric Iron
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 47 → Hardness 12.0
#    - Meteoric Iron
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 48 → Hardness 12.5
#    - Meteoric Iron
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 49 → Hardness 13.0
#    -
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 50 → Hardness 13.0
#    -
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 51 → Hardness 13.5
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 52 → Hardness 13.5
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 53 → Hardness 14.0
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 54 → Hardness 14.0
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 55 → Hardness 14.5
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 56 → Hardness 14.5
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 57 → Hardness 15.0
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 58 → Hardness 15.0
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 59 → Hardness 15.5
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite
#
# Floor 60 → Hardness 16.0
#    - Golanthium
#    - Malachite, Tanzanite, Prehnite, Quartz, Garnet, Jasper, Ammolite, Labradorite, Jade, Serpentine, Titanite, Padparadscha, Rhodochrosite, Goshenite, Kyanite, Ametrine, Sodalite, Taaffeite, Indraneelam, Apatite, Amethyst, Spinel, Emerald, Andesine, Rhodonite, Zircon, Iolite, Onyx, Beryl, Danburite, Fluorite, Aventurine, Azurite, Lapis Lazuli, Diopside, Morganite, Neelam, Aquamarine, Citrine, Spectrolite, Obsidian, Sapphire, Bloodstone, Rutilated Quartz, Chrysocolla, Opal, Ruby, Hessonite, Blizzard Stone, Turquoise, Bixbite, Peridot, Sang-E-Maryam, Sunstone, Tsavorite, Topaz, Heliodor, Petalite, Chrysoberyl, Spessartite, Moonstone, Zoisite, Tiger eye, Agate, Kunzite


# Unit conversion is for crafting only, but should be reflected in prices too.

# Generate Magic Stone Types
magic_stone_text = {'tiny': 'sliver', 'small': 'fragment', 'medium': 'chunk', 'regular': '', 'large': 'crystal', 'huge': 'cluster'}
magic_stone_sub_text = {'tiny': 'A {0} sliver of a magic stone',
                        'small': 'A {0} fragment of a magic stone',
                        'medium': 'A {0} chunk of a magic stone',
                        'regular': 'A {0} magic stone',
                        'large': 'A {0} magic stone crystal',
                        'huge': 'A {0} cluster of magic stones'}

magic_stones = []
for large_type in magic_stone_types:
    for small_type in magic_stone_types:
        definition = f'D, {large_type}_{small_type}_magic_stone, {small_type.title()} Magic Stone {magic_stone_text[large_type]}, multi, {100}, {200}\n{magic_stone_sub_text[large_type].format(small_type)}.\n'
        magic_stones.append(definition)
print(f'{len(magic_stones)} Magic Stones.')

# All enemy shit
ENCOUNTER_CHANCE = 0.15

gems = ['']

floor_ids = [f'floor_{x + 1}' for x in range(60)]
floor_sizes = [13, 14, 17, 18, 18, 19, 19, 20, 21,  21,
               22, 22, 23, 24, 24, 25, 26, 26, 27,  27,
               28, 29, 29, 30, 31, 31, 32, 32, 33,  34,
               34, 35, 36, 36, 37, 37, 38, 39, 39,  40,
               41, 43, 45, 47, 49, 51, 53, 55, 57,  57,
               59, 61, 64, 66, 68, 71, 73, 75, 78,  80,
               82, 85, 87, 89, 92, 94, 96, 99, 101, 103]
map_types = ['path_map', 'full_map', 'safe_zone_map']
enemies = ['goblin', 'kobold', 'jack_bird', 'dungeon_lizard', 'frog_shooter', 'war_shadow', 'killer_ant', 'purple_moth', 'needle_rabbit', 'blue_papilio',
           'orc', 'imp', 'bad_bat', 'hard_armored', 'infant_dragon', 'silverback', 'black_wyvern', 'wyvern', 'crystal_mantis', 'lamia mormos', 'hellhound',
           'almiraj', 'dungeon_worm', 'minotaur', 'lygerfang', 'bugbear', 'battle_boar', 'lizardman', 'firebird', 'vouivre',
           'mad_beetle', 'mammoth_fool', 'dark_fungus', 'gun_libellula', 'sword_stag', 'troll', 'deadly_hornet', 'bloody_hive', 'green_dragon',
           'hobgoblin', 'viscum', 'moss huge', 'metal_rabbit', 'poison_vermis', 'raider_fish', 'harpy', 'siren', 'blue_crab', 'aqua_serpent',
           'crystal_turtle', 'devil_mosquito', 'light_quartz', 'crystaroth_urchin', 'iguazu', 'mermaid', 'merman', 'kelpie', 'afanc', 'dodora',
           'lamia', 'voltimeria', 'bloodsaurus', 'power_bull', 'grand_treant', 'worm_well', 'spartoi', 'barbarian', 'lizardman_elite',
           'obsidian_soldier', 'skull_sheep', 'loup_garou', 'peluda', 'flame_rock', 'fomoire', 'black_rhino', 'deformis_spider', 'cadmus',
           'venom_scorpion', 'thunder_snake', 'silver_worm', 'ill_wyvern', 'valgang_dragon', 'titan_alm', 'unicorn', 'dungeon_fly', 'ogre',
           'gargoyle', 'gryphon', 'arachne', 'hippogriff', 'armarosaurus', 'old_bison', 'ape', 'vulture']


floor_spawns = {'floor_1': {'goblin': 1, 'kobold': 2, 'jack_bird': 5},
                'floor_2': {'goblin': 1, 'kobold': 1, 'jack_bird': 5},
                'floor_3': {'goblin': 1, 'kobold': 1, 'jack_bird': 5},
                'floor_4': {'goblin': 2, 'kobold': 1, 'dungeon_lizard': 2},
                'floor_5': {'goblin': 2, 'kobold': 1, 'dungeon_lizard': 2},
                'floor_6': {'kobold': 1, 'dungeon_lizard': 1, 'frog_shooter': 2},
                'floor_7': {'kobold': 1, 'dungeon_lizard': 2, 'war_shadow': 3, 'killer_ant': 2, 'orc': 3},
                'floor_8': {'war_shadow': 4, 'killer_ant': 2, 'purple_moth': 3, 'orc': 1, 'imp': 1},
                'floor_9': {'war_shadow': 4, 'killer_ant': 2, 'purple_moth': 3, 'blue_papilio': 5, 'orc': 1, 'imp': 1},
                'floor_10': {'killer_ant': 1, 'purple_moth': 4, 'blue_papilio': 5, 'bad_bat': 3, 'hard_armored': 2},
                'floor_11': {'purple_moth': 4, 'blue_papilio': 5, 'imp': 2, 'bad_bat': 3, 'hard_armored': 1},
                'floor_12': {'blue_papilio': 5, 'imp': 2, 'hard_armored': 1, 'silverback': 3, 'infant_dragon': 5},
                'floor_13': {'hard_armored': 1, 'infant_dragon': 5, 'silverback': 2, 'black_wyvern': 4},
                'floor_14': {'hard_armored': 1, 'silverback': 1, 'black_wyvern': 4, 'wyvern': 4, 'metal_rabbit': 1},
                'floor_15': {'black_wyvern': 4, 'wyvern': 4, 'crystal_mantis': 3, 'hellhound': 1, 'metal_rabbit': 1},
                'floor_16': {'black_wyvern': 4, 'wyvern': 4, 'crystal_mantis': 3, 'hellhound': 1, 'imp': 2, 'needle_rabbit': 1},
                'floor_17': {'crystal_mantis': 3, 'wyvern': 4, 'lamia mormos': 3, 'hellhound': 1, 'almiraj': 1, 'imp': 2, 'needle_rabbit': 1},
                'floor_18': {'crystal_mantis': 3, 'wyvern': 4, 'lamia mormos': 3, 'hellhound': 2, 'imp': 2, 'armarosaurus': 4},
                'floor_19': {'wyvern': 4, 'lamia mormos': 2, 'hellhound': 1, 'almiraj': 1, 'imp': 2, 'poison_vermis': 4},
                'floor_20': {'lamia mormos': 2, 'hellhound': 1, 'almiraj': 1, 'imp': 2, 'minotaur': 3, 'poison_vermis': 4},

                # The "Middle" Levels
                'floor_21': {'dungeon_worm': 4, 'minotaur': 2, 'lygerfang': 1, 'bugbear': 1, 'hobgoblin': 1, 'flame_rock': 2, 'old_bison': 3, 'needle_rabbit': 2},
                'floor_22': {'dungeon_worm': 4, 'minotaur': 2, 'lygerfang': 1, 'bugbear': 1, 'hobgoblin': 1, 'flame_rock': 2, 'old_bison': 3, 'needle_rabbit': 2},
                'floor_23': {'dungeon_worm': 4, 'minotaur': 2, 'lygerfang': 1, 'lizardman': 1, 'hobgoblin': 2, 'flame_rock': 2, 'needle_rabbit': 2},
                'floor_24': {'dungeon_worm': 3, 'minotaur': 2, 'lygerfang': 2, 'battle_boar': 1, 'metal_rabbit': 2, 'dungeon_fly': 2, 'armarosaurus': 3},
                'floor_25': {'dungeon_worm': 3, 'minotaur': 2, 'lygerfang': 2, 'battle_boar': 1, 'metal_rabbit': 2, 'dungeon_fly': 2, 'armarosaurus': 3},
                'floor_26': {'lygerfang': 1, 'bugbear': 2, 'battle_boar': 2, 'lizardman': 1, 'firebird': 3, 'poison_vermis': 4, 'needle_rabbit': 1},
                'floor_27': {'lizardman': 1, 'firebird': 3, 'mad_beetle': 1, 'deadly_hornet': 2, 'bloody_hive': 2, 'dungeon_fly': 1, 'arachne': 1},
                'floor_28': {'lizardman': 1, 'firebird': 3, 'vouivre': 5, 'mad_beetle': 1, 'mammoth_fool': 3, 'metal_rabbit': 2, 'arachne': 2},
                'floor_29': {'lizardman': 1, 'firebird': 3, 'vouivre': 5, 'mad_beetle': 1, 'mammoth_fool': 3, 'metal_rabbit': 2, 'arachne': 2},
                'floor_30': {'vouivre':  5, 'mad_beetle': 1, 'mammoth_fool': 1, 'dark_fungus': 1, 'green_dragon': 3, 'dungeon_fly': 2, 'arachne': 2},
                'floor_31': {'mad_beetle': 1, 'mammoth_fool': 1, 'dark_fungus': 2, 'deadly_hornet': 2, 'bloody_hive': 2, 'dungeon_fly': 2, 'arachne': 3},
                'floor_32': {'mad_beetle': 2, 'mammoth_fool': 1, 'dark_fungus': 1, 'deadly_hornet': 2, 'bloody_hive': 2, 'unicorn': 5, 'gryphon': 4},
                'floor_33': {'mammoth_fool': 1, 'dark_fungus': 1, 'gun_libellula': 2, 'deadly_hornet': 3, 'bloody_hive': 3, 'unicorn': 5, 'gryphon': 4},
                'floor_34': {'mammoth_fool': 1, 'dark_fungus': 1, 'gun_libellula': 1, 'deadly_hornet': 3, 'bloody_hive': 3, 'unicorn': 5, 'gryphon': 3},
                'floor_35': {'dark_fungus': 2, 'gun_libellula': 1, 'sword_stag': 2, 'green_dragon': 3, 'hobgoblin': 2, 'unicorn': 5, 'ogre': 3},
                'floor_36': {'dark_fungus': 2, 'gun_libellula': 1, 'sword_stag': 2, 'green_dragon': 4, 'hobgoblin': 2, 'dungeon_fly': 2, 'ogre': 3},
                'floor_37': {'gun_libellula': 2, 'sword_stag': 1, 'green_dragon': 3, 'viscum': 3, 'moss huge': 2, 'metal_rabbit': 1, 'unicorn': 5},
                'floor_38': {'gun_libellula': 1, 'sword_stag': 1, 'green_dragon': 3, 'hobgoblin': 1, 'viscum': 3, 'moss huge': 2, 'ogre': 2},
                'floor_39': {'green_dragon': 2, 'hobgoblin': 1, 'viscum': 3, 'moss huge': 2, 'metal_rabbit': 1, 'poison_vermis': 3, 'unicorn': 4},

                # The "Water" Levels
                'floor_40': {'raider_fish': 1, 'blue_crab': 1, 'devil_mosquito': 2, 'crystaroth_urchin': 3, 'afanc': 3, 'lamia': 2, 'vulture': 3, 'troll': 2},
                'floor_41': {'raider_fish': 1, 'blue_crab': 1, 'aqua_serpent': 2, 'crystal_turtle': 3, 'crystaroth_urchin': 2, 'afanc': 3, 'lamia': 2, 'vulture': 3, 'troll': 3},
                'floor_42': {'raider_fish': 1, 'harpy': 4, 'blue_crab': 2, 'aqua_serpent': 2, 'crystaroth_urchin': 3, 'afanc': 3, 'lamia': 2, 'vulture': 3, 'troll': 2},
                'floor_43': {'raider_fish': 1, 'harpy': 3, 'blue_crab': 1, 'aqua_serpent': 1, 'crystaroth_urchin': 3, 'kelpie': 3, 'afanc': 2, 'lamia': 1, 'voltimeria': 3, 'vulture': 3},
                'floor_44': {'raider_fish': 1, 'harpy': 2, 'siren': 4, 'blue_crab': 1, 'devil_mosquito': 2, 'iguazu': 3, 'mermaid': 5, 'kelpie': 3, 'dodora': 4, 'voltimeria': 3},
                'floor_45': {'raider_fish': 1, 'harpy': 2, 'siren': 3, 'blue_crab': 1, 'devil_mosquito': 2, 'iguazu': 3, 'mermaid': 5, 'merman': 4, 'kelpie': 3, 'dodora': 4, 'voltimeria':3},
                'floor_46': {'raider_fish': 1, 'siren': 3, 'blue_crab': 1, 'crystal_turtle': 4, 'devil_mosquito': 3, 'iguazu':2, 'mermaid': 4, 'merman': 4, 'kelpie': 3, 'dodora': 4, 'voltimeria': 2},
                'floor_47': {'siren': 2, 'blue_crab': 1, 'aqua_serpent': 1, 'light_quartz': 3, 'iguazu': 2, 'mermaid': 4, 'merman': 4, 'dodora': 3, 'voltimeria': 2},
                'floor_48': {'siren': 2, 'aqua_serpent': 1, 'crystal_turtle': 4, 'light_quartz': 3, 'iguazu': 2, 'mermaid': 3, 'merman': 3, 'dodora': 3, 'voltimeria': 2},

                # The "Deep" Levels
                'floor_49': {'bloodsaurus': 1, 'grand_treant': 2, 'worm_well': 5, 'spartoi': 1, 'loup_garou': 1, 'black_rhino': 1, 'venom_scorpion': 3, 'titan_alm': 3, 'gargoyle': 4, 'armarosaurus': 4, 'ape':  2},
                'floor_50': {'bloodsaurus': 1, 'grand_treant': 2, 'worm_well': 5, 'spartoi': 1, 'loup_garou': 1, 'black_rhino': 1, 'venom_scorpion': 3, 'titan_alm': 3, 'gargoyle': 4, 'armarosaurus': 4, 'ape':  2},
                'floor_51': {'bloodsaurus': 1, 'worm_well': 5, 'spartoi': 1, 'skull_sheep': 2, 'loup_garou': 1, 'flame_rock': 3, 'black_rhino': 2, 'ill_wyvern': 3, 'titan_alm': 3, 'gargoyle': 3, 'ape':  1},
                'floor_52': {'power_bull': 1, 'worm_well': 4, 'spartoi': 1, 'barbarian': 1, 'skull_sheep': 2, 'flame_rock': 3, 'black_rhino': 2, 'ill_wyvern': 3, 'titan_alm': 3, 'armarosaurus': 4, 'ape':  1},
                'floor_53': {'power_bull': 1, 'worm_well': 4, 'spartoi': 2, 'barbarian': 1, 'skull_sheep': 2, 'flame_rock': 3, 'venom_scorpion': 2, 'ill_wyvern': 3, 'gargoyle': 3, 'old_bison': 1, 'ape':  1},
                'floor_54': {'power_bull': 1, 'worm_well': 4, 'barbarian': 1, 'lizardman_elite': 1, 'peluda': 3, 'fomoire': 2, 'venom_scorpion': 2, 'valgang_dragon': 5, 'old_bison': 1, 'ape':  2},
                'floor_55': {'grand_treant': 1, 'worm_well': 4, 'barbarian': 1, 'lizardman_elite': 1, 'peluda': 2, 'fomoire': 2, 'deformis_spider': 1, 'valgang_dragon': 4, 'gryphon': 3, 'old_bison': 2, 'ape':  2},
                'floor_56': {'grand_treant': 1, 'worm_well': 3, 'barbarian': 2, 'lizardman_elite': 1, 'peluda': 2, 'fomoire': 2, 'deformis_spider': 1, 'valgang_dragon': 4, 'gryphon': 3, 'old_bison': 2, 'ape':  2},
                'floor_57': {'worm_well': 4, 'barbarian': 2, 'lizardman_elite': 1, 'obsidian_soldier': 2, 'fomoire': 1, 'deformis_spider': 1, 'cadmus': 3, 'silver_worm': 3, 'hippogriff': 3, 'ape':  3},
                'floor_58': {'worm_well': 4, 'lizardman_elite': 1, 'obsidian_soldier': 2, 'fomoire': 1, 'cadmus': 3, 'thunder_snake': 3, 'silver_worm': 3, 'valgang_dragon': 3, 'hippogriff': 3, 'ape':  3},
                'floor_59': {'worm_well': 4, 'lizardman_elite': 1, 'obsidian_soldier': 2, 'fomoire': 1, 'cadmus': 3, 'thunder_snake': 2, 'silver_worm': 3, 'valgang_dragon': 3, 'hippogriff': 3, 'ape':  3},
                'floor_60': {'worm_well': 4, 'lizardman_elite': 1, 'obsidian_soldier': 1, 'cadmus': 3, 'thunder_snake': 2, 'silver_worm': 2, 'hippogriff': 3, 'ape':  2, 'valgang_dragon': 2}}

drop_types = {
    'claw': {
        'goblin': 1,
        'kobold': 1,
        'dungeon_lizard': 1,
        'war_shadow': 1,
        'imp': 1,
        'hard_armored': 1,
        'infant_dragon': 1,
        'wyvern': 1,
        'lamia mormos': 1,
        'minotaur': 1,
        'bugbear': 1,
        'battle_boar': 1,
        'lizardman': 1,
        'vouivre': 1,
        'green_dragon': 1,
        'hobgoblin': 1,
        'moss huge': 1,
        'harpy': 1,
        'siren': 1,
        'blue_crab': 1,
        'afanc': 1,
        'dodora': 1,
        'lamia': 1,
        'spartoi': 1,
        'lizardman_elite': 1,
        'deformis_spider': 1
    }, 'fang': {
        'goblin': 1,
        'kobold': 1,
        'dungeon_lizard': 1,
        'imp': 1,
        'infant_dragon': 1,
        'black_wyvern': 1,
        'wyvern': 1,
        'hellhound': 1,
        'almiraj': 1,
        'dungeon_worm': 1,
        'minotaur': 1,
        'lygerfang': 1,
        'vouivre': 1,
        'battle_boar': 1,
        'mammoth_fool': 1,
        'green_dragon': 1,
        'hobgoblin': 1,
        'raider_fish': 2,
        'siren': 2,
        'devil_mosquito': 1,
        'crystaroth_urchin': 1,
        'afanc': 1,
        'bloodsaurus': 1,
        'worm_well': 1,
        'loup_garou': 1,
        'thunder_snake': 1,
        'silver_worm': 1,
        'valgang_dragon': 1,
        'vulture': 1
    }, 'egg': {
        'jack_bird': 0,
        'vouivre': 0,
        'flame_rock': 1
    }, 'hide': {
        'kobold': 2,
        'jack_bird': 2,
        'needle_rabbit': 2,
        'orc': 2,
        'imp': 2,
        'silverback': 2,
        'hellhound': 2,
        'almiraj': 2,
        'minotaur': 2,
        'lygerfang': 2,
        'bugbear': 2,
        'battle boar': 2,
        'mammoth_fool': 2,
        'sword_stag': 2,
        'troll': 2,
        'moss huge': 2,
        'metal_rabbit': 2,
        'kelpie': 2,
        'power_bull': 2,
        'grand_treant': 2,
        'barbarian': 2,
        'skull_sheep': 2,
        'loup_garou': 2,
        'fomoire': 2,
        'black_rhino': 2,
        'deformis_spider': 2,
        'titan_alm': 2,
        'unicorn': 3,
        'ogre': 2,
        'gryphon': 2,
        'arachne': 2,
        'hippogriff': 2,
        'old_bison': 2,
        'ape': 2,
        'battle_boar': 2
    }, 'scale': {
        'dungeon_lizard': 2,
        'frog_shooter': 2,
        'killer_ant': 2,
        'hard_armored': 2,
        'infant_dragon': 2,
        'black_wyvern': 2,
        'wyvern': 2,
        'lamia mormos': 2,
        'lizardman': 2,
        'vouivre': 2,
        'mad_beetle': 2,
        'deadly_hornet': 2,
        'green_dragon': 2,
        'raider_fish': 2,
        'blue_crab': 2,
        'aqua_serpent': 2,
        'crystal_turtle': 2,
        'mermaid': 2,
        'merman': 2,
        'dodora': 2,
        'lamia': 2,
        'voltimeria': 2,
        'bloodsaurus': 2,
        'worm_well': 2,
        'lizardman_elite': 2,
        'obsidian_soldier': 2,
        'peluda': 2,
        'cadmus': 2,
        'venom_scorpion': 2,
        'thunder_snake': 2,
        'silver_worm': 2,
        'ill_wyvern': 2,
        'valgang_dragon': 2,
        'gargoyle': 2,
        'armarosaurus': 2
    }, 'wing': {
        'purple_moth': 2,
        'blue_papilio': 3,
        'bad_bat': 2,
        'crystal_mantis': 2,
        'firebird': 3,
        'mad_beetle': 2,
        'gun_libellula': 2,
        'deadly_hornet': 2,
        'harpy': 3,
        'siren': 3,
        'aqua_serpent': 2,
        'devil_mosquito': 2,
        'iguazu': 2,
        'kelpie': 2,
        'ill_wyvern': 2,
        'dungeon_fly': 2
    }, 'tongue': {
        'dungeon_lizard': 1,
        'frog_shooter': 1,
        'vulture': 1
    }, 'meat': {
        'jack_bird': 1,
        'needle_rabbit': 1,
        'infant_dragon': 1,
        'blue_crab': 1,
        'light_quartz': 1,
        'afanc': 1,
        'bloodsaurus': 1,
        'barbarian': 1,
        'titan_alm': 1,
        'ogre': 1
    }, 'blood': {
        'killer_ant': 3,
        'infant_dragon': 3,
        'bloody_hive': 3,
        'mermaid': 5,
        'deformis_spider': 3,
        'unicorn': 4
    }, 'horn': {
        'needle_rabbit': 1,
        'sword_stag': 1,
        'crystaroth_urchin': 2,
        'iguazu': 1,
        'power_bull': 2,
        'skull_sheep': 2,
        'peluda': 2,
        'fomoire': 2,
        'black_rhino': 2,
        'unicorn': 5
    }, 'venom': {
        'purple_moth': 2,
        'blue_papilio': 3,
        'black_wyvern': 2,
        'dungeon_worm': 2,
        'dark_fungus': 2,
        'deadly_hornet': 2,
        'bloody_hive': 2,
        'viscum': 2,
        'poison_vermis': 2,
        'crystaroth_urchin': 2,
        'dodora': 2,
        'worm_well': 2,
        'peluda': 2,
        'venom_scorpion': 2,
        'arachne': 2
    }
}

print('There are', len(enemies), 'monsters')

file = open('output.txt', 'w', encoding='utf-8')
for index, enemy in enumerate(enemies):
    file.write('# ' + enemy.replace('_', ' ').title() + '\n')
    floors = []
    for floor, spawns in floor_spawns.items():
        if enemy in spawns.keys():
            floors.append(floor[6:])
    file.write(f'# Found on Floors {floors[0]}')
    for floor in floors[1:-1]:
        file.write(', ' + floor)
    if len(floors) > 1:
        if len(floors) > 2:
            file.write(',')
        file.write(f' and {floors[-1]}' + '\n')
    drops = []
    for drop, drop_type, in drop_types.items():
        if enemy in drop_type:
            drops.append(drop.title())
    file.write('#' + '\n')
    file.write('# Type: ' + '\n')
    hard = soft = False
    for hard_type in ['Fang', 'Claw', 'Scale', 'Horn']:
        if hard_type in drops:
            hard = True
    for soft_type in ['Hide']:
        if soft_type in drops:
            soft = True
    file.write(f'# Hardness: {"" if hard else None}(hard), {"" if soft else None}(soft)' + '\n')
    file.write(f'# Defining Effect: {"" if (hard or soft) else None}' + '\n')
    file.write(f'# Sub Effect: {"" if (hard or soft) else None}' + '\n')

    file.write(f'# Drops: {drops[0]}')
    for drop in drops[1:-1]:
        file.write(', ' + drop)
    if len(drops) > 1:
        if len(drops) > 2:
            file.write(',')
        file.write(f' and {drops[-1]}')
    file.write('\n\n')
file.close()

# Generate Common items
common_items = []
common_items.append(compass)
common_items.append(pocket_watch)

# Generate mob drops
drops = []
for drop, enemy_list in drop_types.items():
    for enemy in enemy_list:
        drops.append(f'{drop}_{enemy}')
# Generate ore types
for material in hard_materials:
    pass

# Generate gems
for gem in gems:
    pass

# Generate tools
tools = []

for tool in tool_types:
    for material in hard_materials:
        pass
        'S, {tool}_{material}, {names[material]} {names[tool]}, tools, single, cost\nfloor, floor_start\ntext\nWarning: floor_end'

# Generate floor maps
for floor in floor_ids:
    for map_type in map_types:
        pass

# Generate Resource maps
for floor in floor_ids:
    for ore in hard_materials:
        pass
    for gem in gems:
        pass
    for enemy in enemies:
        pass

# Generate plants

# Generate woods

# Generate Ingredients
#- Vials

# Generate Potions

# Generate Equipment

# Weapon and off-hand weapon types
# Dagger - 1 hand
# 5 units hard material
# 1 unit soft material
# A small dagger that allows for swift attacks at short range.

# Knuckleduster - 1 hand
# 5 units hard material
# For those who like to punch things

# Wood handled Axe - 1 hand
# 5 units hard material
# 5 units wood
# 2 units soft material
# An axe, good for chopping up your enemies!

# Wood handled Spear - 2 hand
# 5 units hard material
# 10 units wood
# 5 units soft material
# A big spear, good for poking.

# Wood handled Pike - 2 hand
# 5 units hard material
# 15 units wood
# 5 units soft material
# A big, big, big spear, good for poking.

# Wood handled Halberd. - 2 hand
# 10 units hard material
# 10 units wood
# 5 unist soft material
# Love baby between a spear and an axe

# Curved Dagger - 1 hand
# 6 units hard material
# 1 unit soft material
# The tool of assassins

# Claws - 1 hand
# 6 units hard material
# 2 units soft material
# You must like to slash things.

# Kukri - 1 hand
# 8 units hard material
# 2 units soft material
# Curved, long daggers. *slice*

# Cutlass - 1 hand
# 10 units hard material
# 2 units soft material
# A curved sword.

# Short Sword - 1 hand
# 10 units hard material
# 1 unit soft material
# A normal, everyday short sword.

# Short Staff - 1 hand
# 10 units hard material
# 5 units soft material
# 5 units gems
# A shorter and weaker staff

# Rapier - 2 hand
# 15 units hard material
# 1 unit soft material
# Pokity, poke, poke

# Mace - 1 hand
# 10 units hard material
# 2 units soft material
# Good for smacking things.

# Axe - 1 hand
# 10 units hard material
# 2 units soft material
# An axe, good for chopping up your enemies!

# Spear - 2 hand
# 15 units hard material
# 5 units soft material
# A big spear, good for poking.

# Staff - 2 hand
# 15 units hard material
# 5 units soft material
# 10 units gems
# Exploosssiiooonnn

# Pike - 2 hand
# 20 units hard material
# 5 units soft material
# A big, big, big spear, good for poking.

# Halberd. - 2 hand
# 20 units hard material
# 5 unist soft material
# Love baby between a spear and an axe

# Longsword - 2 hand
# 15 units hard material
# 2 units soft material
# A normal, everyday sword, that's longer than a short sword.

# Katana - 1 hand
# 15 units hard material
# 2 units soft material
# A long, curved sword.

# Broadsword - 2 hand
# 20 units hard material
# 3 units soft material
# A large broadsword that allows you to bash your enemies.

# Giant Axe
# 30 units hard material
# 5 units soft material
# Even better for chopping.

# Double-ended broadsword - 2 hand
# 50 units hard material
# 5 units soft material
# An absolute beast of a sword.

# Double-headed Giant Axe
# 50 units hard material
# 5 units soft material
# An absolute beast of an axe, best for chopping heads.

# Hammer - 2 hand
# 30 units hard material
# 5 units soft material
# A giant hammer than allows you to pulverize your enemies.

# Double-headed Hammer - 2 hand
# 50 units hard material
# 5 units soft material
# A giant hammer than allows you to pulverize your enemies.

# Generate Home Supplies
# Forge
# Blacksmithing tools


# Generate unique items (undine cloth, etc.)

# Generate other

# Higher rarity = less spawn
rarities = [1, 2, 3, 4, 5]
rarities_weights = [1 / (2 ** rarities[x]) for x in range(5)]

enemy_drops = {}
for drop_type, drop_list in drop_types.items():
    for enemy_name, drop_rarity in drop_list.items():
        if enemy_name not in enemy_drops:
            enemy_drops[enemy_name] = {}
        enemy_drops[enemy_name][drop_type] = drop_rarity


def get_drop_item(drop_rarities):
    drop_list = drop_rarities[choices(rarities, rarities_weights, k=1)[0]]
    if len(drop_list) > 0:
        item = drop_list[randint(0, len(drop_list) - 1)]
        if item is None:
            return [None]
        # item_count = int(item[:item.index(' ')])
        # if item_count > 4:
        #     enemy_name, item_name = item[item.index(' ') + 1:item.rindex(' ')], item[item.rindex(' ') + 1:]
        #     enemy_id = enemy_name.replace(' ', '_').lower()
        #     replace_count = randint(0, item_count - 4)
        #     if replace_count > 0 and len(enemy_drops[enemy_id]) > 1:
        #         first_item = f'{item_count - replace_count} {enemy_name} {item_name}'
        #         new_item = None
        #         while new_item is None:
        #             print(enemy_drops[enemy_id])
        #             new_item = list(enemy_drops[enemy_id].keys())[randint(0, len(enemy_drops[enemy_id].keys()))]
        #             if new_item == item_name.lower():
        #                 new_item = None
        #         second_item = f'{replace_count} {enemy_name} {new_item.title()}'
        #         return [first_item, second_item]
        return [item]
    return [None]


def simulate_ecounters(floor_spawn_rarities, drop_rarities, guarrenteed):
    spawn_count_total, spawn_counts, spawn_count_totals, drop_counts, drop_count_totals, first_encounters = 0, {}, {}, {}, {}, {}
    # Set all counters to 0
    for enemy, boost_list in drop_rarities.items():
        spawn_count_totals[enemy] = 0
        drop_count_totals[enemy] = {}
        first_encounters[enemy] = None
        if enemy in guarrenteed:
            for drop_item in guarrenteed[enemy]:
                drop_count_totals[drop_item[2:]] = 0
        for boost, rarity_list in boost_list.items():
            spawn_counts[f'{enemy} Level {boost + 1}'] = 0
            drop_counts[f'{enemy} Level {boost + 1}'] = {}
            for drop_list in rarity_list.values():
                for drop_name in drop_list:
                    if drop_name is None:
                        continue
                    drop_count_totals[enemy][drop_name[drop_name.index(' ') + 1:]] = 0
                    drop_counts[f'{enemy} Level {boost + 1}'][drop_name] = 0
    # Do 1 million encounters
    for x in range(1000000):
        # Choose a random number of enemies to spawn
        count = choices([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], k=1)[0]
        spawn_count_total += count

        # Choose rarities to spawn
        spawn = choices(rarities, rarities_weights, k=count)
        for rarity in spawn:
            # From the spawn rarity list, choose a random enemy to spawn
            if len(floor_spawn_rarities[rarity]) > 0:
                name = floor_spawn_rarities[rarity][randint(0, len(floor_spawn_rarities[rarity]) - 1)]

                # Individual counts
                spawn_counts[name] += 1

                # Total counts
                total_name = name[:-8]
                spawn_count_totals[total_name] += 1

                if not first_encounters[total_name]:
                    first_encounters[total_name] = x

                # Drop Item
                boost = int(name[name.rindex(' ') + 1:]) - 1
                dropped_item_list = get_drop_item(drop_rarities[total_name][boost])
                for dropped_item in dropped_item_list:
                    if dropped_item is not None:
                        drop_counts[name][str(dropped_item)] += 1
                        drop_count_totals[total_name][str(dropped_item)[str(dropped_item).index(' ') + 1:]] += 1
                if total_name in guarrenteed:
                    for drop_item in guarrenteed[total_name]:
                        drop_count_totals[drop_item[2:]] += 1
    return spawn_count_total, spawn_counts, spawn_count_totals, drop_counts, drop_count_totals, first_encounters


floors = {}
# Make the dictionary of the spawn rarities
for floor_id in list(floor_spawns.keys()):
    floors[floor_id] = {1: [], 2: [], 3: [], 4: [], 5: []}
    for enemy, rarity in floor_spawns[floor_id].items():
        name = enemy.replace("_", " ").title()
        for new_rarity in range(rarity, 6):
            level_name = f'{name} Level {new_rarity + 1 - rarity}'
            floors[floor_id][new_rarity].append(level_name)

for floor_id, spawn_rarities in floors.items():
    drop_rarities = {}
    guarrenteed = {}
    for spawn_list in spawn_rarities.values():
        for enemy in spawn_list:
            name, boost = enemy[:-8], int(enemy[-1]) - 1
            if name not in drop_rarities:
                drop_rarities[name] = {}
            if boost not in drop_rarities[name]:
                drop_rarities[name][boost] = {1: [None], 2: [], 3: [], 4: [], 5: []}
            for drop_type, drop_list in drop_types.items():
                if name.lower().replace(" ", "_") in drop_list.keys():
                    rarity = drop_list[name.lower().replace(" ", "_")]
                    if rarity == 0:
                        if name not in guarrenteed:
                            guarrenteed[name] = []
                        guarrenteed[name].append(f'1 {name} {drop_type.title()}')
                        continue
                    for new_rarity in range(rarity, 6):
                        drop_rarities[name][boost][new_rarity].append(f'{1 + new_rarity - 1 + boost} {name} {drop_type.title()}')
    spawn_count_total, spawn_counts, spawn_count_totals, drop_counts, drop_count_totals, first_encounters = simulate_ecounters(spawn_rarities, drop_rarities, guarrenteed)

    print(floor_id.title().replace('_', ' ') + ':')
    for name, count in spawn_count_totals.items():
        print('\t' + name, str(round(count / spawn_count_total * 100, 2)) + '%', '-', first_encounters[name])
        if name in guarrenteed:
            for drop_item in guarrenteed[name]:
                print('\t\t' + drop_item[2:], str(round(drop_count_totals[drop_item[2:]] / count * 100, 2)) + '%', '/', str(round(drop_count_totals[drop_item[2:]] / spawn_count_total * 100, 2)) + '%')
        for drop_item, drop_count in sorted(drop_count_totals[name].items()):
            print('\t\t' + drop_item, str(round(drop_count / count * 100, 2)) + '%', '/', str(round(drop_count / spawn_count_total * 100, 2)) + '%')
    print()
    for name, count in spawn_counts.items():
        print('\t' + name, str(round(count / spawn_count_total * 100, 2)) + '%')
        if name[:-8] in guarrenteed:
            for drop_item in guarrenteed[name[:-8]]:
                print('\t\t' + drop_item, str(round(drop_count_totals[drop_item[2:]] / count * 100, 2)) + '%', '/', str(round(drop_count_totals[drop_item[2:]] / spawn_count_total * 100, 2)) + '%')
        for drop_item, drop_count in sorted(drop_counts[name].items()):
            print('\t\t' + drop_item, str(round(drop_count / count * 100, 2)) + '%', '/', str(round(drop_count / spawn_count_total * 100, 2)) + '%')
    print('\n')


