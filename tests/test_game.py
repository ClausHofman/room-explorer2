import unittest
import game.room
import game.creatures
from game.player import Player
from game.inventory import Item, Inventory
from game.managers import RoomManager, EquipmentManager, SaveLoadManager, EventManager
from game.equipment import Equipment

class TestRoom(unittest.TestCase):
    def setUp(self):
        self.room = game.room.Room("Test Room", "A test room")

    def test_connect(self):
        room2 = game.room.Room("Room 2", "Another room")
        self.room.connect("north", room2)
        self.assertEqual(self.room.exits["north"], room2.room_id)

    def test_connect_invalid_direction(self):
        room2 = game.room.Room("Room 2", "Another room")
        with self.assertRaises(ValueError):
            self.room.connect("invalid", room2)

    def test_add_creature(self):
        creature = game.creatures.Creature("Goblin", "A green goblin", 10)
        self.room.add_creature(creature)
        self.assertIn(creature, self.room.creatures)

    def test_add_non_creature(self):
        with self.assertRaises(TypeError):
            self.room.add_creature("not a creature")

    def test_add_object(self):
        obj = game.room.GameObject("Table", "A wooden table")
        self.room.add_object(obj)
        self.assertIn(obj, self.room.objects)

    def test_add_non_object(self):
        with self.assertRaises(TypeError):
            self.room.add_object("not an object")

    def test_list_creatures(self):
        creature = game.creatures.Creature("Goblin", "A green goblin", 10)
        self.room.add_creature(creature)
        self.assertEqual(len(self.room.creatures), 1)

    def test_to_from_dict(self):
        room2 = game.room.Room("Room 2", "Another room")
        self.room.connect("north", room2)
        creature = game.creatures.Creature("Goblin", "A green goblin", 10)
        self.room.add_creature(creature)
        obj = game.room.GameObject("Table", "A wooden table")
        self.room.add_object(obj)
        dict_data = self.room.to_dict()
        new_room = game.room.Room.from_dict(dict_data)
        self.assertEqual(self.room.name, new_room.name)
        self.assertEqual(self.room.description, new_room.description)
        self.assertEqual(self.room.exits, new_room.exits)
        self.assertEqual(len(self.room.objects), len(new_room.objects))
        self.assertEqual(len(self.room.creatures), len(new_room.creatures))


class TestGameObject(unittest.TestCase):
    def setUp(self):
        self.obj = game.room.GameObject("Table", "A wooden table")
        self.item = Item("Book", "A dusty book", 5)

    def test_add_item(self):
        self.obj.add_item(self.item)
        self.assertIn(self.item, self.obj.inventory)
        self.assertEqual(len(self.obj.inventory), 1)

    def test_to_from_dict(self):
        self.obj.add_item(self.item)
        dict_data = self.obj.to_dict()
        new_obj = game.room.GameObject.from_dict(dict_data)
        self.assertEqual(self.obj.name, new_obj.name)
        self.assertEqual(self.obj.description, new_obj.description)
        self.assertEqual(len(self.obj.inventory), len(new_obj.inventory))


class TestCreature(unittest.TestCase):
    def setUp(self):
        self.creature = game.creatures.Creature("Goblin", "A green goblin", 10)

    def test_take_damage(self):
        self.creature.take_damage(5)
        self.assertEqual(self.creature.health, 5)

    def test_take_lethal_damage(self):
        self.creature.take_damage(15)
        self.assertEqual(self.creature.health, 0)

    def test_heal(self):
        self.creature.take_damage(5)
        self.creature.heal(3)
        self.assertEqual(self.creature.health, 8)
    
    def test_to_from_dict(self):
        dict_data = self.creature.to_dict()
        new_creature = game.creatures.Creature.from_dict(dict_data)
        self.assertEqual(self.creature.name, new_creature.name)
        self.assertEqual(self.creature.description, new_creature.description)
        self.assertEqual(self.creature.health, new_creature.health)


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.item = Item("Potion", "A healing potion", 10)

    def test_add_item(self):
        self.inventory.add_item(self.item)
        self.assertIn(self.item, self.inventory.items)

    def test_remove_item(self):
        self.inventory.add_item(self.item)
        removed_item = self.inventory.remove_item("Potion")
        self.assertEqual(removed_item, self.item)
        self.assertNotIn(self.item, self.inventory.items)

    def test_remove_nonexistent_item(self):
        removed_item = self.inventory.remove_item("Nonexistent Item")
        self.assertIsNone(removed_item)
        self.assertEqual(len(self.inventory.items), 0)
    
    def test_to_from_dict(self):
        self.inventory.add_item(self.item)
        dict_data = self.inventory.to_dict()
        new_inventory = Inventory.from_dict(dict_data)
        self.assertEqual(len(self.inventory.items), len(new_inventory.items))

class TestItem(unittest.TestCase):
    def setUp(self):
        self.item = Item("Potion", "A healing potion", 10)
    
    def test_to_from_dict(self):
        dict_data = self.item.to_dict()
        new_item = Item.from_dict(dict_data)
        self.assertEqual(self.item.name, new_item.name)
        self.assertEqual(self.item.description, new_item.description)
        self.assertEqual(self.item.value, new_item.value)

class TestEquipmentManager(unittest.TestCase):
    def setUp(self):
        self.equipment_manager = EquipmentManager()
        self.sword = Equipment("Sword", "hand")
        self.shield = Equipment("Shield", "offhand")
        self.potion = Item("Potion", "A healing potion", 10)

    def test_equip_item(self):
        self.equipment_manager.equip_item(self.sword)
        self.assertIn("hand", self.equipment_manager.equipment)
        self.assertEqual(self.equipment_manager.equipment["hand"], self.sword)

    def test_equip_already_equipped(self):
        self.equipment_manager.equip_item(self.sword)
        self.equipment_manager.equip_item(self.sword)
        self.assertEqual(len(self.equipment_manager.equipment), 1)

    def test_equip_non_equipment(self):
        self.equipment_manager.equip_item(self.potion)
        self.assertEqual(len(self.equipment_manager.equipment), 0)

    def test_unequip_item(self):
        self.equipment_manager.equip_item(self.sword)
        unequipped_item = self.equipment_manager.unequip_item("hand")
        self.assertEqual(unequipped_item, self.sword)
        self.assertNotIn("hand", self.equipment_manager.equipment)

    def test_unequip_nonexistent_item(self):
        unequipped_item = self.equipment_manager.unequip_item("hand")
        self.assertIsNone(unequipped_item)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.room_manager = RoomManager()
        self.starting_room = game.room.Room("Hallway", "A narrow corridor")
        self.room2 = game.room.Room("Room 2", "Another room")
        self.starting_room.connect("north", self.room2)
        self.room2.connect("south", self.starting_room)
        self.room_manager.add_room(self.starting_room)
        self.room_manager.add_room(self.room2)
        self.player = Player("Test Player", self.starting_room, self.room_manager)

    def test_move(self):
        self.player.move("north")
        self.assertEqual(self.player.current_room, self.room2)

    def test_move_invalid(self):
        self.player.move("west")
        self.assertEqual(self.player.current_room, self.starting_room)

    def test_to_from_dict(self):
        dict_data = self.player.to_dict()
        new_player = Player.from_dict(dict_data, self.room_manager)
        self.assertEqual(self.player.name, new_player.name)
        self.assertEqual(self.player.current_room.name, new_player.current_room.name)
        self.assertEqual(len(self.player.inventory.items), len(new_player.inventory.items))
        self.assertEqual(len(self.player.equipment.equipment), len(new_player.equipment.equipment))


class TestRoomManager(unittest.TestCase):
    def setUp(self):
        self.room_manager = RoomManager()
        self.room = game.room.Room("Test Room", "A test room")

    def test_add_room(self):
        self.room_manager.add_room(self.room)
        self.assertIn(self.room, self.room_manager.game_rooms)
        self.assertEqual(self.room_manager.room_lookup[self.room.room_id], self.room)

class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.event_type = "test_event"
        self.listener = lambda event_type, data: print(f"Event '{event_type}' handled with data: {data}")

    def test_add_listener(self):
        self.event_manager.add_listener(self.event_type, self.listener)
        self.assertIn(self.event_type, self.event_manager.handlers)
        self.assertIn(self.listener, self.event_manager.handlers[self.event_type])

    def test_remove_listener(self):
        self.event_manager.add_listener(self.event_type, self.listener)
        self.event_manager.remove_listener(self.event_type, self.listener)
        self.assertNotIn(self.listener, self.event_manager.handlers.get(self.event_type, []))

    def test_add_event(self):
        self.event_manager.add_listener(self.event_type, self.listener)
        self.event_manager.add_event(self.event_type)
        self.assertTrue(True)

class TestSaveLoadManager(unittest.TestCase):
    def setUp(self):
        self.room_manager = RoomManager()
        self.starting_room = game.room.Room("Hallway", "A narrow corridor")
        self.room2 = game.room.Room("Room 2", "Another room")
        self.starting_room.connect("north", self.room2)
        self.room2.connect("south", self.starting_room)
        self.room_manager.add_room(self.starting_room)
        self.room_manager.add_room(self.room2)
        self.player = Player("Test Player", self.starting_room, self.room_manager)

    def test_save_load_game(self):
        SaveLoadManager.save_game(self.player, self.room_manager)
        loaded_player, loaded_rooms = SaveLoadManager.load_game()
        self.assertEqual(loaded_player.name, self.player.name)
        self.assertEqual(len(loaded_rooms), len(self.room_manager.game_rooms))
        self.assertEqual(loaded_player.current_room.name, self.player.current_room.name)

if __name__ == '__main__':
    unittest.main()

# python -m unittest discover -s tests -v