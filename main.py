from game.player import Player
from game.inventory import Item
from game.managers import RoomManager, SaveLoadManager
from game.equipment import Equipment
from game.room import Room, GameObject
from game.creatures import Creature

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
player.move("north")
room2.list_creatures()

# Managing inventory
potion = Item("Potion", "A healing potion.", "50")
player.inventory.add_item(potion)
player.inventory.display()

# Equipping items
sword = Equipment("A gleaming sword", "hand")
player.equipment.equip_item(sword)
player.equipment.list_equipment()


SaveLoadManager.save_game(player, room_manager)
player, rooms = SaveLoadManager.load_game()
# Update the room manager with the loaded rooms
room_manager.game_rooms = rooms
print(room_manager.game_rooms)
print(room_manager.room_lookup)

# print(player.current_room.room_id)
# print(player.equipment)
# print(player.inventory)

# Check the results
# for room in rooms:
#     print(room.name, room.description)  # Living Room A cozy room with a fireplace.
#     for obj in room.objects:
#         print(f"{obj.name}: {obj.description}")
#         for item in obj.inventory:
#             print(f"  - {item.name}: {item.description}")
#     for creature in room.creatures:
#         print(f"{creature.name}: {creature.description}")
# print(room_manager.game_rooms)