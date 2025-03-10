import game.creatures
import game.inventory

class GameObject:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.inventory = []
    
    def add_item(self, item):
        self.inventory.append(item)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "inventory": [item.to_dict() for item in self.inventory],
            "type": self.__class__.__name__  # Store object type for deserialization
        }

    @staticmethod
    def from_dict(data):
        obj = GameObject(data["name"], data["description"])
        obj.inventory = [game.inventory.Item.from_dict(item) for item in data["inventory"]]
        return obj

class Room:
    room_count = -1

    def __init__(self, name, description):
        Room.room_count += 1
        self.name = name
        self.room_id = None  # Assigned by RoomManager
        self.description = description
        self.room_id = f"room{self.room_count}"
        self.objects = []
        self.creatures = []
        self.exits = {}

        print(f"Created room: {self.room_id}")

    def connect(self, direction, neighbor_room):
        if direction in self.available_directions():
            self.exits[direction] = neighbor_room.room_id
        else:
            raise ValueError(f"Invalid direction '{direction}' for room '{self.name}'")
    
    def add_creature(self, creature):
        if isinstance(creature, game.creatures.Creature):
            self.creatures.append(creature)
        else:
            raise TypeError("Only instances of Creature can be added.")

    def list_creatures(self):
        print(f"Creatures in {self.name}:")
        for creature in self.creatures:
            print(f"- {creature.name}: {creature.description} (Health: {creature.health})")

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "name": self.name,
            "description": self.description,
            "exits": self.exits,  # Serialize exits with room_id references
            "objects": [obj.to_dict() for obj in self.objects],  # Serialize all objects
            "creatures": [creature.to_dict() for creature in self.creatures]
        }

    @staticmethod
    def from_dict(data):
        room = Room(data["name"], data["description"])
        room.room_id = data["room_id"]
        room.exits = data["exits"]  # Restore exits
        room.objects = [GameObject.from_dict(obj) for obj in data["objects"]]  # Rebuild objects
        room.creatures = [game.creatures.Creature.from_dict(creature) for creature in data["creatures"]]
        return room


    def add_object(self, obj):
        if isinstance(obj, GameObject):
            self.objects.append(obj)
        else:
            raise TypeError("Only objects inheriting from GameObject can be added to a room.")

    @staticmethod
    def available_directions():
        return ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest', 'up', 'down']
    