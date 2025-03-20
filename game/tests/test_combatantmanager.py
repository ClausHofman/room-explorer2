import unittest
import copy
from managers import CombatantManager

# python -m unittest discover -s tests -v

class TestCombatantManager(unittest.TestCase):
    def setUp(self):
        """Set up reusable test fixtures before each test."""
        self.traits = {"Strength": 10, "Agility": 8, "Intelligence": 7}
        self.status_effects = {
            "buffs": {"Power Surge": [2, 5]},
            "debuffs": {"Slow": [1, 2]}
        }
        self.manager = CombatantManager(self.traits, self.status_effects, ["Strength", "Agility"])

    def test_initialization(self):
        """Test that the manager initializes correctly."""
        self.assertEqual(self.manager.all_traits, self.traits)
        self.assertIn("Strength", self.manager.selected_traits)
        self.assertEqual(self.manager.selected_traits["Strength"], 10)
        self.assertEqual(self.manager.buffs["Power Surge"], [2, 5])
        self.assertEqual(self.manager.debuffs["Slow"], [1, 2])

    def test_describe_traits(self):
        """Test the description of selected traits."""
        description = self.manager.describe_traits()
        self.assertIn("Strength: 10", description)
        self.assertIn("Agility: 8", description)

    def test_add_buff(self):
        """Test adding a new buff."""
        self.manager.add_buff("Adrenaline Rush", 3, 4)
        self.assertIn("Adrenaline Rush", self.manager.buffs)
        self.assertEqual(self.manager.buffs["Adrenaline Rush"], [3, 4])
        self.assertEqual(self.manager.current_power, 4)

    def test_remove_buff(self):
        """Test removing an existing buff."""
        self.manager.remove_buff("Power Surge")
        self.assertNotIn("Power Surge", self.manager.buffs)

    def test_decrement_buff_durations(self):
        """Test decrementing buff durations."""
        self.manager.decrement_buff_durations()
        self.assertEqual(self.manager.buffs["Power Surge"][0], 1)  # Reduced duration
        self.manager.decrement_buff_durations()
        self.assertNotIn("Power Surge", self.manager.buffs)  # Buff removed

    def test_describe_status(self):
        """Test status description of buffs and debuffs."""
        description = self.manager.describe_status()
        self.assertIn("Power Surge (Duration: 2, Strength: 5)", description)
        self.assertIn("Slow (Duration: 1, Strength: 2)", description)

if __name__ == "__main__":
    unittest.main()
