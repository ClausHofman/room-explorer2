import unittest
from game.room import Room
from game.combatants import Combatant, Player, Monster
import game.combatant_data as combatant_data
from game.helper_functions import create_creature, create_player, create_companion
from game.managers import TurnManager

class TestRoom(unittest.TestCase):

    def setUp(self):
        """Setup method to create a fresh Room object before each test."""
        self.room = Room()
        self.turn_manager = TurnManager()
        self.player = create_player(
            creature_type="player",
            player_data=combatant_data.player_data,
            creature_traits=combatant_data.creature_traits_data,
            status_data=combatant_data.creature_status_data,
        )
        self.monster = create_creature(
            creature_type="dragon",
            creature_data=combatant_data.creature_data,
            creature_traits=combatant_data.creature_traits_data,
            status_data=combatant_data.creature_status_data,
        )
        self.companion = create_companion(
            creature_type="companion",
            companion_data=combatant_data.companion_data,
            creature_traits=combatant_data.creature_traits_data,
            status_data=combatant_data.creature_status_data
        )

    def test_room_initialization(self):
        """Test that a Room object is created with the correct default values."""
        self.assertEqual(self.room.room_name, "Default room name")
        self.assertIsNotNone(self.room.room_id)
        self.assertFalse(self.room.in_combat)
        self.assertFalse(self.room.always_track_turns)
        self.assertEqual(self.room.combat_rounds, 0)
        self.assertEqual(self.room.combatants, [])
        self.assertEqual(self.room.entities, [])
        self.assertEqual(self.room.room_exits, {})

    def test_room_initialization_with_custom_values(self):
        """Test that a Room object is created with custom values."""
        room = Room(room_name="Custom Room", room_id="custom_room_id", always_track_turns=True, in_combat=True, combat_rounds=5)
        self.assertEqual(room.room_name, "Custom Room")
        self.assertEqual(room.room_id, "custom_room_id")
        self.assertTrue(room.in_combat)
        self.assertTrue(room.always_track_turns)
        self.assertEqual(room.combat_rounds, 5)

    def test_room_count_increment(self):
        """Test that the room_count is incremented correctly."""
        initial_count = Room.room_count
        Room()
        self.assertEqual(Room.room_count, initial_count + 1)

    def test_to_dict(self):
        """Test that to_dict() returns a dictionary with the correct keys and values."""
        room_dict = self.room.to_dict()
        self.assertIsInstance(room_dict, dict)
        self.assertIn("room_name", room_dict)
        self.assertIn("room_id", room_dict)
        self.assertIn("in_combat", room_dict)
        self.assertIn("combat_rounds", room_dict)
        self.assertIn("always_track_turns", room_dict)
        self.assertIn("combatants", room_dict)
        self.assertIn("entities", room_dict)
        self.assertIn("room_exits", room_dict)

    def test_to_dict_with_combatants(self):
        """Test that to_dict() correctly serializes combatants."""
        self.room.add_combatant(self.monster)
        room_dict = self.room.to_dict()
        self.assertEqual(len(room_dict["combatants"]), 1)
        self.assertEqual(room_dict["combatants"][0]["type"], "Monster")
        self.assertEqual(room_dict["combatants"][0]["data"]["id"], self.monster.id)

    def test_to_dict_with_entities(self):
        """Test that to_dict() correctly serializes entities."""
        # Add an entity to the room
        class Entity:
            def __init__(self, name):
                self.name = name
            def to_dict(self):
                return {"name": self.name}
            @classmethod
            def from_dict(cls, data):
                return cls(data["name"])
        entity = Entity("Test Entity")
        self.room.entities.append(entity)
        room_dict = self.room.to_dict()
        self.assertEqual(len(room_dict["entities"]), 1)
        self.assertEqual(room_dict["entities"][0]["type"], "Entity")
        self.assertEqual(room_dict["entities"][0]["data"]["name"], "Test Entity")

    def test_to_dict_with_room_exits(self):
        """Test that to_dict() correctly serializes room_exits."""
        room2 = Room(room_id="room2")
        self.room.connect(room2, "north")
        room_dict = self.room.to_dict()
        self.assertEqual(room_dict["room_exits"], {"north": "room2"})

    def test_to_dict_updates_combatant_current_room(self):
        """Test that to_dict() updates the combatant.current_room before serialization."""
        self.room.add_combatant(self.monster)
        self.room.to_dict()
        self.assertEqual(self.monster.current_room, self.room.room_id)

    def test_from_dict(self):
        """Test that from_dict() correctly creates a Room object from a dictionary."""
        room_dict = self.room.to_dict()
        reconstructed_room = Room.from_dict(room_dict)
        self.assertEqual(reconstructed_room.room_name, self.room.room_name)
        self.assertEqual(reconstructed_room.room_id, self.room.room_id)
        self.assertEqual(reconstructed_room.in_combat, self.room.in_combat)
        self.assertEqual(reconstructed_room.combat_rounds, self.room.combat_rounds)
        self.assertEqual(reconstructed_room.always_track_turns, self.room.always_track_turns)

    def test_from_dict_with_combatants(self):
        """Test that from_dict() correctly deserializes combatants."""
        self.room.add_combatant(self.monster)
        room_dict = self.room.to_dict()
        reconstructed_room = Room.from_dict(room_dict)
        self.assertEqual(len(reconstructed_room.combatants), 1)
        self.assertIsInstance(reconstructed_room.combatants[0], Monster)
        self.assertEqual(reconstructed_room.combatants[0].id, self.monster.id)

    def test_from_dict_with_entities(self):
        """Test that from_dict() correctly deserializes entities."""
        class Entity:
            def __init__(self, name):
                self.name = name
            def to_dict(self):
                return {"name": self.name}
            @classmethod
            def from_dict(cls, data):
                return cls(data["name"])
        entity = Entity("Test Entity")
        self.room.entities.append(entity)
        room_dict = self.room.to_dict()
        reconstructed_room = Room.from_dict(room_dict)
        self.assertEqual(len(reconstructed_room.entities), 1)
        self.assertIsInstance(reconstructed_room.entities[0], Entity)
        self.assertEqual(reconstructed_room.entities[0].name, "Test Entity")

    def test_from_dict_with_room_exits(self):
        """Test that from_dict() correctly deserializes room_exits."""
        room2 = Room(room_id="room2")
        self.room.connect(room2, "north")
        room_dict = self.room.to_dict()
        reconstructed_room = Room.from_dict(room_dict)
        self.assertEqual(reconstructed_room.room_exits, {"north": "room2"})

    def test_from_dict_missing_room_id(self):
        """Test that from_dict() throws a ValueError if the room_id is missing."""
        room_dict = self.room.to_dict()
        del room_dict["room_id"]
        with self.assertRaises(ValueError):
            Room.from_dict(room_dict)

    def test_connect(self):
        """Test that connect() correctly adds a connection to room_exits."""
        room2 = Room(room_id="room2")
        self.room.connect(room2, "north")
        self.assertEqual(self.room.room_exits, {"north": "room2"})

    def test_connect_invalid_target_room(self):
        """Test that connect() throws a ValueError if target_room is not a Room object."""
        with self.assertRaises(ValueError):
            self.room.connect("not a room", "north")

    def test_connect_invalid_parameters(self):
        """Test that connect() throws a ValueError if the connection parameters are invalid."""
        room2 = Room(room_id="room2")
        with self.assertRaises(ValueError):
            self.room.connect(room2, "invalid_direction")

    def test_connect_special_connection(self):
        """Test that connect() correctly handles special connections."""
        room2 = Room(room_id="room2")
        self.room.connect(room2, "special_portal", portal_id="portal1")
        self.assertEqual(self.room.room_exits, {"special_portal": {"target_room": room2, "portal_id": "portal1"}})

    def test_advance_turn_always_track_turns(self):
        """Test that advance_turn() prints the correct message if always_track_turns is True."""
        self.room.always_track_turns = True
        self.room.advance_turn(1)

    def test_advance_turn_in_combat(self):
        """Test that advance_turn() increments combat_rounds if in_combat is True."""
        self.room.in_combat = True
        self.room.combat_start_turn = 0
        self.room.advance_turn(1)
        self.assertEqual(self.room.combat_rounds, 1)

    def test_on_turn_advanced_in_combat(self):
        """Test that on_turn_advanced() calls advance_combat_round() if in_combat is True."""
        self.room.in_combat = True
        self.room.on_turn_advanced(1)
        # We can't directly check if advance_combat_round() was called,
        # but we can check if combat_rounds was incremented, which happens in advance_combat_round()
        self.assertEqual(self.room.combat_rounds, 1)

    def test_advance_combat_round_not_in_combat(self):
        """Test that advance_combat_round() does not increment combat_rounds if in_combat is False."""
        self.room.in_combat = False
        self.room.advance_combat_round(1)
        self.assertEqual(self.room.combat_rounds, 0)

    def test_advance_combat_round_ends_combat_no_hostility(self):
        """Test that advance_combat_round() ends combat if there is no hostility."""
        self.room.in_combat = True
        self.room.combat_start_turn = 0
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.advance_combat_round(1)
        self.assertFalse(self.room.in_combat)

    def test_advance_combat_round_processes_combatants_turn(self):
        """Test that advance_combat_round() processes each combatant's turn."""
        self.room.in_combat = True
        self.room.combat_start_turn = 0
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.detect_hostility(self.turn_manager)
        self.room.advance_combat_round(1)
        self.assertTrue(self.room.in_combat)

    def test_advance_combat_round_removes_defeated_grudges(self):
        """Test that advance_combat_round() removes defeated combatants from grudges."""
        self.room.in_combat = True
        self.room.combat_start_turn = 0
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.detect_hostility(self.turn_manager)
        self.monster.stats["health"] = 0
        self.room.advance_combat_round(1)
        self.assertNotIn(self.monster.id, self.player.grudge_list)

    def test_advance_combat_round_ends_combat_victory(self):
        """Test that advance_combat_round() ends combat if the victory conditions are met."""
        self.room.in_combat = True
        self.room.combat_start_turn = 0
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.detect_hostility(self.turn_manager)
        self.monster.stats["health"] = 0
        self.room.advance_combat_round(1)
        self.assertFalse(self.room.in_combat)

    def test_add_combatant(self):
        """Test that add_combatant() correctly adds a Combatant to combatants."""
        self.room.add_combatant(self.monster)
        self.assertIn(self.monster, self.room.combatants)

    def test_add_combatant_already_in_room(self):
        """Test that add_combatant() does not add a Combatant if it's already in the room."""
        self.room.add_combatant(self.monster)
        initial_count = len(self.room.combatants)
        self.room.add_combatant(self.monster)
        self.assertEqual(len(self.room.combatants), initial_count)

    def test_add_combatant_sets_current_room(self):
        """Test that add_combatant() sets the combatant.current_room to the room_id."""
        self.room.add_combatant(self.monster)
        self.assertEqual(self.monster.current_room, self.room.room_id)

    def test_remove_combatant_by_id(self):
        """Test that remove_combatant_by_id() correctly removes a Combatant from combatants."""
        self.room.add_combatant(self.monster)
        self.room.remove_combatant_by_id(self.monster.id)
        self.assertNotIn(self.monster, self.room.combatants)

    def test_remove_combatant_by_id_not_in_room(self):
        """Test that remove_combatant_by_id() does nothing if the Combatant is not in the room."""
        initial_count = len(self.room.combatants)
        self.room.remove_combatant_by_id(self.monster.id)
        self.assertEqual(len(self.room.combatants), initial_count)

    def test_remove_combatant_by_id_sets_current_room_none(self):
        """Test that remove_combatant_by_id() sets the combatant.current_room to None."""
        self.room.add_combatant(self.monster)
        self.room.remove_combatant_by_id(self.monster.id)
        self.assertIsNone(self.monster.current_room)

    def test_add_new_combatant(self):
        """Test that add_new_combatant() correctly adds a Combatant to combatants."""
        self.room.add_new_combatant(self.monster)
        self.assertIn(self.monster, self.room.combatants)

    def test_detect_hostility(self):
        """Test that detect_hostility() correctly detects hostility."""
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)

    def test_detect_hostility_adds_grudges(self):
        """Test that detect_hostility() correctly adds grudges."""
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.detect_hostility(self.turn_manager)
        self.assertIn(self.monster.id, self.player.grudge_list)
        self.assertIn(self.player.id, self.monster.grudge_list)

    def test_detect_hostility_starts_combat(self):
        """Test that detect_hostility() starts combat if there is hostility."""
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.detect_hostility(self.turn_manager)
        self.assertTrue(self.room.in_combat)

    def test_has_hostility_true(self):
        """Test that has_hostility() returns True if there is hostility."""
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.detect_hostility(self.turn_manager)
        self.assertTrue(self.room.has_hostility())

    def test_has_hostility_false(self):
        """Test that has_hostility() returns False if there is no hostility."""
        self.room.add_combatant(self.player)
        self.assertFalse(self.room.has_hostility())

    def test_update_grudges_new_combatant(self):
        """Test that update_grudges() correctly adds grudges for the new combatant."""
        self.room.add_combatant(self.player)
        self.room.update_grudges(self.monster)
        self.assertIn(self.player.id, self.monster.grudge_list)

    def test_update_grudges_existing_combatants(self):
        """Test that update_grudges() correctly updates existing combatants' grudges."""
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.update_grudges(self.companion)
        self.assertIn(self.companion.id, self.player.grudge_list)
        self.assertIn(self.companion.id, self.monster.grudge_list)

    def test_start_combat(self):
        """Test that start_combat() sets in_combat to True and initializes combat_rounds."""
        self.room.start_combat(1)
        self.assertTrue(self.room.in_combat)
        self.assertEqual(self.room.combat_start_turn, 1)
        self.assertEqual(self.room.combat_rounds, 0)

    def test_end_combat(self):
        """Test that end_combat() sets in_combat to False and resets combat_rounds."""
        self.room.in_combat = True
        self.room.combat_start_turn = 1
        self.room.combat_rounds = 5
        self.room.end_combat()
        self.assertFalse(self.room.in_combat)
        self.assertEqual(self.room.combat_start_turn, 0)
        self.assertEqual(self.room.combat_rounds, 0)

    def test_remove_defeated_grudges(self):
        """Test that remove_defeated_grudges() correctly removes the defeated combatant from all grudge lists."""
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.detect_hostility(self.turn_manager)
        self.room.remove_defeated_grudges(self.monster.id)
        self.assertNotIn(self.monster.id, self.player.grudge_list)

    def test_select_target_valid_target(self):
        """Test that select_target() returns a valid target."""
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.room.detect_hostility(self.turn_manager)
        target = self.room.select_target(self.monster)
        self.assertIsNotNone(target)
        self.assertIn(target.id, self.monster.grudge_list)

    def test_select_target_no_valid_targets(self):
        """Test that select_target() returns None if there are no valid targets."""
        self.room.add_combatant(self.player)
        target = self.room.select_target(self.monster)
        self.assertIsNone(target)

    def test_check_victory_player_defeated(self):
        """Test that check_victory() returns True if the player has been defeated."""
        self.player.stats["health"] = 0
        self.room.add_combatant(self.player)
        self.assertTrue(self.room.check_victory())

    def test_check_victory_all_monsters_defeated(self):
        """Test that check_victory() returns True if all monsters are defeated."""
        self.monster.stats["health"] = 0
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.assertTrue(self.room.check_victory())

    def test_check_victory_no_victory(self):
        """Test that check_victory() returns False if neither victory condition is met."""
        self.room.add_combatant(self.player)
        self.room.add_combatant(self.monster)
        self.assertFalse(self.room.check_victory())

    def test_trigger_reinforcements(self):
        """Test that trigger_reinforcements() adds a new goblin to the room."""
        initial_combatant_count = len(self.room.combatants)
        self.room.trigger_reinforcements()
        self.assertEqual(len(self.room.combatants), initial_combatant_count + 1)
        # You might want to add more specific checks here, like checking the type of the new combatant

    def test_spawn_monsters(self):
        """Test that spawn_monsters() adds the correct number of monsters to the room."""
        initial_combatant_count = len(self.room.combatants)
        self.room.spawn_monsters(["dragon", "dragon"])
        self.assertEqual(len(self.room.combatants), initial_combatant_count + 2)

    def test_spawn_monsters_invalid_monster_type(self):
        """Test that spawn_monsters() throws a ValueError if the monster type does not exist."""
        with self.assertRaises(ValueError):
            self.room.spawn_monsters("invalid_monster_type")
