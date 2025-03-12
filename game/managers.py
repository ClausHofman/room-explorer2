import game.room
import game.player
import json
# import game.creatures as Creature

class EquipmentManager:
    def __init__(self):
        self.equipment = {}

    def equip_item(self, item):
        if not hasattr(item, 'slot'):
            print("You can only wield equipment.")
            return False
        slot = item.slot
        if slot in self.equipment:
            print(f"You are already wielding {self.equipment[slot].name}.")
            return False
        self.equipment[slot] = item
        print(f"You wield {item.name}.")
        return True

    def unequip_item(self, slot_name):
        if slot_name in self.equipment:
            item = self.equipment.pop(slot_name)
            print(f"You unequipped {item.name}.")
            return item
        else:
            print(f"No item equipped in {slot_name} slot.")
            return None

    def list_equipment(self):
        print("Currently equipped items:")
        for slot, item in self.equipment.items():
            print(f"- {slot}: {item.name}")

class RoomManager:
    def __init__(self):
        self.game_rooms = []
        self.room_lookup = {}  # Maps room_id to Room objects

    def add_room(self, room):
        self.game_rooms.append(room)
        self.room_lookup[room.room_id] = room  # Add to lookup


class SaveLoadManager:
    @staticmethod
    def save_game(player, room_manager, filepath="serialization/game_save.json"):
        try:
            game_data = {
                "rooms": [room.to_dict() for room in room_manager.game_rooms],
                "player": player.to_dict()
            }
            with open(filepath, "w") as file:
                json.dump(game_data, file, indent=4)
        except IOError as e:
            print(f"Error saving game: {e}")
        print(f"Game saved to {filepath}")

    @staticmethod
    def load_game(filepath="serialization/game_save.json"):
        try:
            with open(filepath, "r") as file:
                game_data = json.load(file)
        except IOError as e:
            print(f"Error loading game: {e}")
            return None, None
        except json.JSONDecodeError as e:
            print(f"Invalid JSON format: {e}")
            return None, None

        # Reset room count before deserialization
        game.room.Room.room_count = -1

        # Deserialize rooms
        rooms = [game.room.Room.from_dict(data) for data in game_data["rooms"]]

        # Rebuild room manager and its lookup
        room_manager = RoomManager()
        room_manager.game_rooms = rooms
        room_manager.room_lookup = {room.room_id: room for room in rooms}

        # Deserialize player
        player = game.player.Player.from_dict(game_data["player"], room_manager)

        return player, rooms

# Maybe fiddle with this later
# class EventManager:
#     def __init__(self):
#         self.handlers = {}

#     def add_listener(self, event_type, listener):
#         """Add a listener to a specific event type."""
#         if event_type not in self.handlers:
#             self.handlers[event_type] = []
#         self.handlers[event_type].append(listener)

#     def remove_listener(self, event_type, listener):
#         """Remove a listener from a specific event type."""
#         if event_type in self.handlers:
#             self.handlers[event_type].remove(listener)

#     def add_event(self, event_type, data=None):
#         """Add an event to be handled by listeners."""
#         if event_type in self.handlers:
#             for handler in self.handlers[event_type]:
#                 handler(event_type, data)


def spawn_creature(creature_class, data, room_manager):
    print(f"Creature class being used: {creature_class}")

    creature_name = data.get("creature_name")
    creature_description = data.get("creature_description")
    room_name = data.get("room_name")
    creature_health = data.get("creature_health")

    if not all(data.get(key) for key in ["creature_name", "creature_description", "room_name", "creature_health"]):
        print("Error: Missing data for creature spawn.")
        print(f"Data provided: {data}")
        return

    print(f"Spawning creature with data: {data}")
    print(f"Number of rooms in room_manager: {len(room_manager.game_rooms)}")
    print(room_manager.room_lookup)

    # Find the room where the creature should be added
    for room in room_manager.game_rooms:
        print(f"Available room name: '{room.name}'")
        if room.name == room_name:
            # Create a new creature instance
            new_creature = creature_class(creature_name, creature_description, creature_health)
            print(new_creature.to_dict())
            # Add the creature to the room
            room.add_creature(new_creature)
            print(f"Spawned {creature_name} in {room_name}.")
            return

    print(f"Room '{room_name}' not found.")
