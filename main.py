import sys, os
sys.path.append(f'{os.getcwd()}\game')
from game.combatants import *
from game.combatant_data import *
from game.room import Room
from game.helper_functions import *
from game.managers import *

# Example usage
selected_traits_for_dragon = ["flight", "fire_resistance"]
dragon1 = create_creature(
    creature_type="dragon",
    creature_data=creature_data,
    creature_traits=creature_traits_data,
    status_data=creature_status_data,
    selected_traits=selected_traits_for_dragon
)
player = create_player(
    creature_type="player",
    player_data=player_data,
    creature_traits=creature_traits_data,
    status_data=creature_status_data,
)
companion1 = create_companion(
    creature_type="companion",
    companion_data=companion_data,
    creature_traits=creature_traits_data,
    status_data=creature_status_data
)

turn_manager = TurnManager()
room_manager = RoomManager()
turn_manager.room_manager = room_manager

room1 = Room()
room_manager.add_room(room1)
room2 = Room()
room_manager.add_room(room2)

room1.connect(room2, "north")
room2.connect(room1, "south")
# pprint(dir(room))
# print("---------------------------------")
# pprint(vars(room))

turn_manager.start_timer(interval_seconds=3)

room1.add_combatant(player)
print(player.current_room)


room1.add_combatant(companion1)
room1.add_combatant(dragon1)
room1.spawn_monsters(["dragon", "dragon"])
# room1.detect_hostility(turn_manager)
# dragon1.combatant_manager.add_buff("strength_boost", 5, 10)
room2.spawn_monsters("dragon")
room2.spawn_monsters(["goblin", "wolf", "wolf", "wolf", "wolf", "rabbit"])
# room2.detect_hostility(turn_manager)


# pprint(dir(player))
# print("---------------------------------")
# pprint(vars(player))
# print(player.stats["health"])

# SAVE AND LOAD
SaveLoadManager.save_to_file("serialization/save_game.json", turn_manager)

# print(RoomManager)  # Should display <class 'RoomManager'>
# print(hasattr(RoomManager, "from_dict"))  # Should display True


room_manager = None
turn_manager = None
# # Load the game and optional data
turn_manager = SaveLoadManager.load_from_file(
    "serialization/save_game.json")

print(player.current_room)

# print((turn_manager))


# dragon1.combatant_manager.decrement_buff_durations()
# print(dragon1.describe())
# print(dragon1.type)

# selected_traits_for_dragon2 = ["regeneration"]
# dragon2 = create_creature(
#     creature_type="dragon",
#     creature_data=creature_data,
#     creature_traits=creature_traits_data,
#     status_data=creature_status_data,
#     selected_traits=selected_traits_for_dragon2
# )

# dragon1.stats["health"] -= 20
# print(f"Flame Wyvern HP: {dragon1.stats['health']}")
# print(f"Flame Wyvern HP: {dragon2.stats['health']}")
# print(dragon1.describe())
# print(dragon1.hates_all)

# dragon2.stats["health"] += 20
# print(f"Flame Wyvern HP: {dragon1.stats['health']}")
# print(f"Flame Wyvern HP: {dragon2.stats['health']}")
# dragon2.combatant_manager.add_buff("strength_boost", 5, 5)
# print(dragon2.describe())

# print("---------------------")
# pprint(dir(dragon1))
# pprint(vars(dragon1.combatant_manager))
# pprint(help(dragon1))
# pprint(hasattr(dragon1, 'x'))
# pprint(getattr(dragon1, 'x', 'Attribute not found'))


# player.combatant_manager.add_buff("strength_boost", 5, 5)
# pprint(dir(player))
# pprint(f"[DEBUG Dragon]{vars(dragon1.combatant_manager)}")
# pprint(f"[DEBUG Dragon]{vars(dragon2.combatant_manager)}")
# pprint(vars(player))
# pprint(vars(companion1))



# Get information about rooms / a room
# room_manager.display_map()
# print(room_manager.get_room_info("room1"))
# print(room_manager.get_room_info("room2"))



while True:
    time.sleep(1)
