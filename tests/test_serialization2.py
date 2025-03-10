import unittest
from game.room import GameObject, Room
from game.managers import RoomManager, SaveLoadManager
from game.player import Player


class TestPlayer(unittest.TestCase):
    def test_save_and_load_game(self):
        Room.room_count = -1
        self.room_manager = RoomManager()
        self.room = Room("First room", "Test Room")  # room_id room0
        self.room2 = Room("Second room", "Test Room")  # room_id room1
        self.room.connect("north", self.room2)
        self.room2.connect("south", self.room)
        self.room_manager.add_room(self.room)
        self.room_manager.add_room(self.room2)
        self.player = Player("TestPlayer", self.room, self.room_manager)

        SaveLoadManager.save_game(self.player, self.room_manager, "game_test.json")
        loaded_player, loaded_room_list = SaveLoadManager.load_game("game_test.json")

        self.assertEqual(self.player.name, loaded_player.name)
        self.assertEqual(self.player.current_room.room_id, loaded_player.current_room.room_id)
        self.assertEqual(len(loaded_room_list), 2)
        self.room_manager.room_lookup = {room.room_id: room for room in loaded_room_list}        
        self.assertIn("north", self.room_manager.room_lookup["room0"].exits)
        self.assertEqual(self.room_manager.room_lookup["room0"].exits["north"], "room1")