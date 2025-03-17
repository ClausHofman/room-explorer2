import sys, os
sys.path.append(f'{os.getcwd()}\game')
from game.combatants import Player, Companion
from game.combatant_data import player_data, companions_data
from game.combatant_data import *
from game.managers import RoomManager, TurnManager, SaveLoadManager
from game.rooms import Room
import time
import logging


# Initialize RoomManager and TurnManager
room_manager = RoomManager()
turn_manager = TurnManager()

# Link RoomManager to TurnManager
turn_manager.room_manager = room_manager

# Create a Room and add it to RoomManager
rooms = Room(always_track_turns=True)  # Enable turn tracking for this room
room_manager.add_room(rooms)
room2 = Room(always_track_turns=False)  # Enable turn tracking for this room
room_manager.add_room(room2)
rooms.connect(room2, "north")
room2.connect(rooms, "south")

# Add Player to the Room
player = Player(player_data)
rooms.add_combatant(player)

# Add Companion to the Room
companion = Companion("companion1", companions_data["companion1"])
rooms.add_combatant(companion)

# Spawn Monsters in the Room
rooms.spawn_monsters(["goblin", "wolf", "rabbit"])

# Start the TurnManager's timer
turn_manager.start_timer(interval_seconds=5)

# Detect Hostility and Start Combat
rooms.detect_hostility()
rooms.start_combat(turn_manager.current_turn)  # Pass the current world turn

# Get information about rooms / a room
room_manager.display_map()
print(room_manager.get_room_info("room1"))
print(room_manager.get_room_info("room2"))

# Save the TurnManager to a file
SaveLoadManager.save_to_file("serialization/save_game.json", turn_manager)

room_manager = None
turn_manager = None
# Load the game and optional data
turn_manager, optional_data = SaveLoadManager.load_from_file(
    "serialization/save_game.json",
    extra_monsters="serialization/creatures.json",
)

# Access the loaded data
if turn_manager:
    print(f"[DEBUG Load TurnManager] Loaded TurnManager with {len(turn_manager.room_manager.game_rooms)} rooms.")
if optional_data:
    print(f"[DEBUG optional_data] Loaded optional data: {optional_data.keys()}")

# Example: Access creatures from optional_data
if "creatures" in optional_data:
    for creature in optional_data["creatures"]:
        print(f"Creature: {creature['name']}")

# Verify deserialized data
if turn_manager:
    print(f"[DEBUG Load] Loaded {turn_manager} rooms.")
    for rooms in turn_manager.room_manager.game_rooms:
        print(f"[DEBUG Load] Room ID: {rooms.room_id}")
        for combatant in rooms.combatants:
            print(f"[DEBUG Load combatants] Type: {type(combatant)} Combatant: {combatant.name} (ID: {combatant.id})")

# Access the loaded creatures as a dictionary
if "extra_monsters" in optional_data:
    extra_monsters = optional_data["extra_monsters"]
    for monster in extra_monsters:
        print(f"Monster Name: {monster['name']}")

# Keep the main program alive
while True:
    time.sleep(1)
