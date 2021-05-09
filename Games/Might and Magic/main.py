from classes.game import Person, bcolors
from classes.magic import Spell

# create black magic
fire = Spell("fire", 10, 100, "black")
thunder = Spell("thunder", 10, 100, "black")
blizzard = Spell("blizzard", 10, 100, "black")
meteor = Spell("meteor", 20, 200, "black")
quake = Spell("quake", 14, 140, "black")

# create white magic
cure = Spell("cure", 12, 120, "white")
cura = Spell("cura", 18, 200, "white")

# list of dictionaries

player = Person(460, 65, 60, 34, [fire,thunder,blizzard,meteor,cure,cura])
enemy = Person(1200, 65, 45, 25, [])

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)


while running:
# player choose attack or magic, using 1 or 2
# then it attacks the enemy

    print("==============================")
    player.choose_action()
    choice = input("Choose action:")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damange(dmg)
        print("You attacked for", dmg, "points of damage")
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("Choose magic:")) -1


        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()



        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
        elif spell.type =="black":
            enemy.take_damange(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)


    enemy_choice = 1
    enemy_dmg = enemy.generate_damage()
    player.take_damange(enemy_dmg)
    print("enemy attacks for", enemy_dmg)

    print("---------------------------")
    print("Enemey HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")

    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
    print("Your MP:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False
"""
print(player.generate_damage())
print(player.generate_spell_damage(0))
print(player.generate_spell_damage(1))
"""