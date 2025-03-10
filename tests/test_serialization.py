# import unittest
# from game.room import GameObject, Room
# from game.managers import RoomManager, SaveLoadManager
# from game.player import Player


# class TestPlayer(unittest.TestCase):
#     def test_save_and_load(self):
#         Room.room_count = -1
#         self.room_manager = RoomManager()
#         self.room = Room("First room", "Test Room")  # room_id room0
#         self.room2 = Room("Second room", "Test Room")  # room_id room1
#         self.room.connect("north", self.room2)
#         self.room2.connect("south", self.room)
#         self.room_manager.add_room(self.room)
#         self.room_manager.add_room(self.room2)
#         self.player = Player("TestPlayer", self.room, self.room_manager)

#         # Save the rooms to a file
#         SaveLoadManager.save_rooms(self.room_manager, "test.json")

#         # Load the rooms back
#         loaded_room_list = SaveLoadManager.load_rooms("test.json")  # Assuming you have a load_rooms method

#         # Verify the number of rooms loaded
#         self.assertEqual(len(loaded_room_list), 2)

#         # Rebuild the room_lookup dictionary
#         self.room_manager.room_lookup = {room.room_id: room for room in loaded_room_list}
#         print(self.room_manager.room_lookup)

#         # Verify the exits are properly restored
#         self.assertIn("north", self.room_manager.room_lookup["room0"].exits)
#         self.assertEqual(self.room_manager.room_lookup["room0"].exits["north"], "room1")  # Check the exit is correct
#         self.assertEqual(self.room_manager.room_lookup["room1"].exits["south"], "room0")  # Verify reverse connection
