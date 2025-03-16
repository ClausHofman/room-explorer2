from game.player import Player
from game.inventory import Item
from game.managers import RoomManager, SaveLoadManager, spawn_creature
from game.equipment import Equipment
from game.room import Room, GameObject
from game.creatures import Creature
import logging

room_manager = RoomManager()

starting_room = Room("Hallway", "A long narrow corridor.")
room2 = Room("A room", "A strange room.")
starting_room.connect("north", room2)
room2.connect("south", starting_room)

goblin = Creature("Goblin", "A small green creature.", 30)
room2.add_creature(goblin)

book = Item("Book", "A dusty old book", 50)
table = GameObject("Table", "A wooden dining table.")
table.add_item(book)

room2.add_object(table)

room_manager.add_room(starting_room)
room_manager.add_room(room2)
player = Player("Claus", starting_room, room_manager)

# for room in room_manager.game_rooms:
#     print(room.to_dict())  # Ensure all rooms are serializable

# Moving between rooms
# player.move("north")
# room2.list_creatures()

# Managing inventory
potion = Item("Potion", "A healing potion.", "50")
player.inventory.add_item(potion)
# player.inventory.display()

# Equipping items
sword = Equipment("A gleaming sword", "hand")
player.equipment.equip_item(sword)
# player.equipment.list_equipment()

# SAVE
SaveLoadManager.save_game(player, room_manager)

# LOAD
player, rooms = SaveLoadManager.load_game()
room_manager.game_rooms = rooms # Update the room manager with the loaded rooms

# print(room_manager.room_lookup)
# print(room_manager.game_rooms)
# print(player.current_room.room_id)
# print(player.equipment)
# print(player.inventory)
# for room in rooms:
#     print(room.name, room.description)
#     for obj in room.objects:
#         print(f"{obj.name}: {obj.description}")
#         for item in obj.inventory:
#             print(f"  - {item.name}: {item.description}")

# --- Spawn a new creature ---
new_room = Room("Forest Edge", "The edge of a dark forest.")
room_manager.add_room(new_room)
creature_data = {
    "creature_name": "Wolf",
    "creature_description": "A large, grey wolf.",
    "room_name": "Forest Edge",  # Make sure this matches a room name
    "creature_health": 75,
}

spawn_creature(Creature, creature_data, room_manager)
# Let's verify that the creature is in the room
# for room in room_manager.game_rooms:
#     room.list_creatures()
