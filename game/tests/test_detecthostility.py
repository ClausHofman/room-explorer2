import unittest
from unittest.mock import MagicMock
from room import Room
from managers import TurnManager

class TestRoomCombatantMethods(unittest.TestCase):

    def setUp(self):
        """Set up a Room instance with mock data before each test."""
        self.room = Room(room_name="Test Room", room_id="room1")
        self.mock_combatant1 = MagicMock(
            name="Combatant1",
            id="combatant1",
            hates_all=False,
            hates_player_and_companions=False,
            hates=["goblin"],
            monster_type="orc",
            grudge_list=[],
            is_alive=lambda: True,
        )
        self.mock_combatant2 = MagicMock(
            name="Combatant2",
            id="combatant2",
            hates_all=True,
            grudge_list=[],
            is_alive=lambda: True,
        )
        self.room.combatants = [self.mock_combatant1]

    def test_add_combatant(self):
        """Test adding a combatant to the room."""
        self.room.add_combatant(self.mock_combatant2)
        self.assertIn(self.mock_combatant2, self.room.combatants)  # Ensure the combatant is added
        self.assertEqual(self.mock_combatant2.current_room, self.room.room_id)  # Verify the room assignment

    def test_add_new_combatant(self):
        """Test adding a new combatant and updating grudges."""
        self.room.update_grudges = MagicMock()  # Mock update_grudges method
        self.room.add_new_combatant(self.mock_combatant2)
        self.room.update_grudges.assert_called_once_with(self.mock_combatant2)  # Verify grudges are updated
        self.assertIn(self.mock_combatant2, self.room.combatants)  # Ensure the combatant is added

    def test_has_hostility_true(self):
        """Test has_hostility returns True when hostility exists."""
        self.mock_combatant1.grudge_list = ["combatant2"]  # Simulate hostility
        self.room.combatants.append(self.mock_combatant2)  # Add another combatant
        self.assertTrue(self.room.has_hostility())  # Expect hostility detection to be True

    def test_has_hostility_false(self):
        """Test has_hostility returns False when no hostility exists."""
        self.mock_combatant1.grudge_list = []  # No hostility
        self.assertFalse(self.room.has_hostility())  # Expect hostility detection to be False

    def test_update_grudges(self):
        """Test updating grudges for a new combatant."""

def test_update_grudges(self):
    """Test updating grudges for a new combatant."""
    self.mock_combatant1.hates_all = True
    self.mock_combatant1.is_alive = MagicMock(return_value=True)
    self.mock_combatant2.is_alive = MagicMock(return_value=True)

    self.room.add_combatant(self.mock_combatant1)
    self.room.add_combatant(self.mock_combatant2)
    
    self.room.update_grudges(self.mock_combatant1)
    self.room.update_grudges(self.mock_combatant2)

    print(f"Combatant1 grudges: {self.mock_combatant1.grudge_list}")
    print(f"Combatant2 grudges: {self.mock_combatant2.grudge_list}")

    self.assertIn("combatant1", self.mock_combatant2.grudge_list)
    self.assertIn("combatant2", self.mock_combatant1.grudge_list)


if __name__ == "__main__":
    unittest.main()

# Run only failing tests:
# python -m unittest tests.test_detecthostility.TestRoomCombatantMethods.test_update_grudges