import unittest
from game.player import Player
from game.room import Room
from game.managers import RoomManager

class TestPlayer(unittest.TestCase):
    def setUp(self):
        Room.room_count = -1
        room_manager = RoomManager()
        self.room = Room("First room", "Test Room") # room_id room0
        self.room2 = Room("Second room", "Test Room") # room_id room1
        self.room.connect("north", self.room2)
        self.room2.connect("south", self.room)
        room_manager.add_room(self.room)
        room_manager.add_room(self.room2)
        self.player = Player("TestPlayer", self.room, room_manager)

    def test_move(self):
        self.player.move("north")
        self.assertEqual(self.player.current_room.room_id, f"{self.room2.room_id}")  # Replace with room object when appropriate

    def test_invalid_move(self):
        self.player.move("west")  # West is not connected
        self.assertEqual(self.player.current_room.room_id, "room0")  # Should remain in the same room

    def test_complex_map(self):
        Room.room_count = -1
        room_manager = RoomManager()
        self.room = Room("First room", "Test Room") # room_id room0
        self.room2 = Room("Second room", "Test Room") # room_id room1
        self.room3 = Room("Third room", "Test Room 3")
        self.room.connect("north", self.room2)
        self.room2.connect("south", self.room)        
        self.room2.connect("east", self.room3)  # Connect room2 -> room3
        room_manager.add_room(self.room)
        room_manager.add_room(self.room2)        
        room_manager.add_room(self.room3)
        self.player = Player("TestPlayer", self.room, room_manager)        

        self.player.move("north")  # Move to room1
        self.assertEqual(self.player.current_room.room_id, "room1")

        self.player.move("east")  # Move to room2 (room3)
        self.assertEqual(self.player.current_room.room_id, "room2")  # Check final position



if __name__ == '__main__':
    unittest.main()

# python -m unittest discover -s tests -v
