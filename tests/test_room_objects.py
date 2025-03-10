import unittest
from game.room import GameObject, Room
from game.managers import RoomManager
from game.player import Player
from game.creatures import Creature

class TestPlayer(unittest.TestCase):
    def test_room_objects(self):
        Room.room_count = -1
        room_manager = RoomManager()
        self.room = Room("First room", "Test Room") # room_id room0
        self.room2 = Room("Second room", "Test Room") # room_id room1
        self.room.connect("north", self.room2)
        self.room2.connect("south", self.room)
        room_manager.add_room(self.room)
        room_manager.add_room(self.room2)

        test_object = GameObject("Key", "A shiny key.")
        self.room2.objects.append(test_object)

        test_creature = Creature("Goblin", "A small goblin with sharp teeth.", 30)
        self.room2.creatures.append(test_creature)

        self.player = Player("TestPlayer", self.room, room_manager)
        print("Current room before move:", self.player.current_room.room_id)
        self.player.move("north")
        print("Current room after move:", self.player.current_room.room_id)
        print("Room objects:", self.player.current_room.objects)
        print("Room creatures:", self.player.current_room.creatures)

        self.assertIn(test_object, self.player.current_room.objects)  # Verify object is present in the room
        self.assertIn(test_creature, self.player.current_room.creatures)  # Verify creature is in the room        
