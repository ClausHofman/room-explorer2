import json

class MovementManager:
    def __init__(self, room_manager, player):
        self.room_manager = room_manager
        self.player = player

    def to_dict(self):
        return {
            "room_manager": str(self.room_manager),  # Example conversion
            "player": str(self.player),             # Example conversion
        }

    @staticmethod
    def from_dict(data):
        return MovementManager(data["room_manager"], data["player"])

movement_manager = MovementManager("RoomManagerExample", "PlayerExample")
data = movement_manager.to_dict()

# Serialize to JSON
with open("movement_manager.json", "w") as f:
    json.dump(data, f)

# Deserialize from JSON
with open("movement_manager.json", "r") as f:
    loaded_data = json.load(f)
    movement_manager = MovementManager.from_dict(loaded_data)
