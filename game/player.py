import game.inventory
import game.managers
import game.equipment
import game.room

class Player:
    def __init__(self, name, current_room, room_manager):
        self.name = name
        self.current_room = current_room
        self.inventory = game.inventory.Inventory()
        self.equipment = game.managers.EquipmentManager()
        self.room_manager = room_manager
    
    def move(self, direction):
        # Check if the direction exists in current_room's exits
        if direction in self.current_room.exits:
            next_room_id = self.current_room.exits[direction]  # Get the room_id
            # Use the RoomManager to resolve the room_id to the actual Room
            if next_room_id in self.room_manager.room_lookup:
                self.current_room = self.room_manager.room_lookup[next_room_id]
                print(f"You moved {direction} to {self.current_room.name}.")
            else:
                print(f"Room with ID '{next_room_id}' not found.")
        else:
            print("You can't go that way.")

    def to_dict(self):
        return {
            "name": self.name,
            "current_room": self.current_room.room_id if self.current_room else None,
            "inventory": self.inventory.to_dict(),  # Example
            "equipment": self.equipment.to_dict() if hasattr(self.equipment, "to_dict") else {}
        }

    @staticmethod
    def from_dict(data, room_manager):
        player = Player(
            name=data["name"],
            current_room=room_manager.room_lookup.get(data["current_room"], None),
            room_manager=room_manager
        )
        player.inventory = game.inventory.Inventory.from_dict(data["inventory"])
        if "equipment" in data and hasattr(player.equipment, "from_dict"):
            player.equipment = game.managers.EquipmentManager.from_dict(data["equipment"])
        return player
