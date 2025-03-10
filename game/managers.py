import game.room
import game.player
import json

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



    # @staticmethod
    # def save_game(player, room_manager, filepath="serialization/test1.json"):
    #     # Get all rooms from the RoomManager and serialize them
    #     rooms = room_manager.game_rooms
    #     try:
    #         with open(filepath, "w") as file:
    #             json.dump([room.to_dict() for room in rooms], file, indent=4)
    #     except IOError as e:
    #        print(f"Error saving rooms: {e}")
    #     print(f"Rooms saved to {filepath}")

    # @staticmethod
    # def load_rooms(filepath="serialization/test1.json"):
    #     try:
    #         with open(filepath, "r") as file:
    #             room_data = json.load(file)
    #     except IOError as e:
    #         print(f"Error loading rooms: {e}")
    #     except json.JSONDecodeError as e:
    #         print(f"Invalid JSON format: {e}")
            
    #     # Reset room count before deserialization
    #     game.room.Room.room_count = -1
    #     # Deserialize rooms
    #     rooms = [game.room.Room.from_dict(data) for data in room_data]
    #     return rooms