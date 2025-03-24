import random
import json

class MonsterActionManager:
    def __init__(self):
        pass

    def use_monster_skill(self, monster, skill_category):
        """
        Triggers the monster to use a skill from a specific category, if it decides to.
        The monster's AI logic determines if and how a skill is used.
        """
        monster.use_skill(skill_category)  # Delegate to the monster's AI


class Monster:
    def __init__(self, name, monster_id):
        self.name = name
        self.id = monster_id
        self.skills = {}  # Changed to a dictionary of categories

    def use_skill(self, skill_category):
        """
        This method contains the monster's AI logic for using skills.
        """
        # Check if the monster has skills in the specified category
        if skill_category in self.skills and self.skills[skill_category]:
            if random.random() < 0.5:  # 50% chance
                skill_name = random.choice(list(self.skills[skill_category].keys()))  # Choose a random skill name
                print(f"{self.name} (ID: {self.id}) is using {skill_name} (category: {skill_category})!")
                # Dynamically call the skill method based on its name
                skill_method = getattr(self, skill_name)
                skill_method(self)
            else:
                print(f"{self.name} (ID: {self.id}) decides not to use a skill from category {skill_category}.")
        else:
            print(f"{self.name} (ID: {self.id}) has no skills in category {skill_category}.")

    def bite(self, monster):
        """Example skill: Wolf's bite."""
        print(f"{monster.name} (ID: {monster.id}) bites!")
        # ... (skill implementation: deal damage to a random combatant in the room) ...

    def howl(self, monster):
        """Example skill: Wolf's howl."""
        print(f"{monster.name} (ID: {monster.id}) howls!")
        # ... (skill implementation: buff other monsters in the room) ...

    def rest(self, monster):
        """Example skill: Monster rests."""
        print(f"{monster.name} (ID: {monster.id}) rests!")
        # ... (skill implementation: recover some health) ...

    def add_skill(self, skill_category, skill_name, skill_info):
        """
        Adds a skill to the monster's repertoire under a specific category.
        """
        if hasattr(self, skill_name) and callable(getattr(self, skill_name)):
            if skill_category not in self.skills:
                self.skills[skill_category] = {}  # Create category if it doesn't exist
            self.skills[skill_category][skill_name] = skill_info  # Store skill info in the dictionary
        else:
            raise ValueError(f"Skill '{skill_name}' is not a valid method of Monster.")

    def to_dict(self):
        """
        Converts the monster object to a dictionary for serialization.
        """
        return {
            "name": self.name,
            "id": self.id,
            "skills": self.skills,  # Now a dictionary of categories
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a monster object from a dictionary (deserialization).
        """
        monster = cls(data["name"], data["id"])
        for skill_category, skills in data["skills"].items():
            for skill_name, skill_info in skills.items():
                monster.add_skill(skill_category, skill_name, skill_info)
        return monster


class Room(MonsterActionManager):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.monsters = []

    def add_monster(self, monster):
        self.monsters.append(monster)

    def trigger_monster_skills(self, skill_category):
        print(f"--- {self.name}: Triggering Monster {skill_category} Skills ---")
        for monster in self.monsters:
            self.use_monster_skill(monster, skill_category)
        print(f"--- {self.name}: End of Monster {skill_category} Skills ---\n")

    def to_dict(self):
        """
        Converts the room object to a dictionary for serialization.
        """
        return {
            "name": self.name,
            "monsters": [monster.to_dict() for monster in self.monsters],
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a room object from a dictionary (deserialization).
        """
        room = cls(data["name"])
        for monster_data in data["monsters"]:
            monster = Monster.from_dict(monster_data)
            room.add_monster(monster)
        return room


# Example Usage:
if __name__ == "__main__":
    # Create some monsters
    wolf1 = Monster("Wolfy", 1)
    wolf1.add_skill("combat", "bite", {"damage": 10, "type": "physical"})  # Added skill info
    wolf1.add_skill("combat", "howl", {"buff": "attack", "duration": 3})  # Added skill info
    wolf1.add_skill("general", "rest", {"heal": 5})

    wolf2 = Monster("Fang", 2)
    wolf2.add_skill("combat", "bite", {"damage": 12, "type": "physical"})  # Added skill info
    wolf2.add_skill("general", "rest", {"heal": 3})

    spider1 = Monster("Webby", 3)
    spider1.add_skill("combat", "bite", {"damage": 8, "type": "poison"})  # Added skill info
    spider1.add_skill("general", "rest", {"heal": 2})

    # Create a room and add monsters to it
    forest = Room("Dark Forest")
    forest.add_monster(wolf1)
    forest.add_monster(wolf2)

    cave = Room("Spooky Cave")
    cave.add_monster(spider1)

    # Trigger monster skills in the room
    forest.trigger_monster_skills("combat")
    cave.trigger_monster_skills("combat")
    forest.trigger_monster_skills("general")

    # --- Serialization ---
    # Convert the room to a dictionary
    forest_data = forest.to_dict()

    # Serialize the dictionary to a JSON string
    forest_json = json.dumps(forest_data, indent=4)
    print("\n--- Serialized Room (JSON) ---\n")
    print(forest_json)

    # --- Deserialization ---
    # Deserialize the JSON string back to a dictionary
    loaded_forest_data = json.loads(forest_json)

    # Create a new room object from the dictionary
    loaded_forest = Room.from_dict(loaded_forest_data)

    print("\n--- Deserialized Room: Triggering Skills ---\n")
    loaded_forest.trigger_monster_skills("combat")
    loaded_forest.trigger_monster_skills("general")

creature_skills = {
    "level": 3,
    "fireball_power": lambda level: level * 5,
    "ice_shard_power": lambda level: level * 3
}

# Accessing skills dynamically
current_level = creature_skills["level"]
fireball = creature_skills["fireball_power"](current_level)
ice_shard = creature_skills["ice_shard_power"](current_level)

print(f"Fireball Power: {fireball}")
print(f"Ice Shard Power: {ice_shard}")





# import random
# import json

# class MonsterActionManager:
#     def __init__(self):
#         pass

#     def use_monster_skill(self, monster, skill_category):
#         """
#         Triggers the monster to use a skill from a specific category, if it decides to.
#         The monster's AI logic determines if and how a skill is used.
#         """
#         monster.use_skill(skill_category)  # Delegate to the monster's AI


# class Monster:
#     def __init__(self, name, monster_id, level=1, strength=1):
#         self.name = name
#         self.id = monster_id
#         self.level = level
#         self.strength = strength
#         self.skills = {}  # Changed to a dictionary of categories

#     def use_skill(self, skill_category):
#         """
#         This method contains the monster's AI logic for using skills.
#         """
#         # Check if the monster has skills in the specified category
#         if skill_category in self.skills and self.skills[skill_category]:
#             if random.random() < 0.5:  # 50% chance
#                 skill_name = random.choice(list(self.skills[skill_category].keys()))  # Choose a random skill name
#                 print(f"{self.name} (ID: {self.id}) is using {skill_name} (category: {skill_category})!")
#                 # Dynamically call the skill method based on its name
#                 skill_method = getattr(self, skill_name)
#                 skill_method(self, self.skills[skill_category][skill_name]) # Pass skill info
#             else:
#                 print(f"{self.name} (ID: {self.id}) decides not to use a skill from category {skill_category}.")
#         else:
#             print(f"{self.name} (ID: {self.id}) has no skills in category {skill_category}.")

#     def bite(self, monster, skill_info):
#         """Example skill: Wolf's bite."""
#         base_damage = skill_info.get("damage", 0)  # Get base damage from skill info
#         damage_type = skill_info.get("type", "physical")
#         # Apply formula to calculate actual damage
#         actual_damage = int(base_damage * (1 + (monster.strength / 10)) * (1 + (monster.level / 20)))
#         print(f"{monster.name} (ID: {monster.id}) bites for {actual_damage} {damage_type} damage!")
#         # ... (skill implementation: deal damage to a random combatant in the room) ...

#     def howl(self, monster, skill_info):
#         """Example skill: Wolf's howl."""
#         buff_type = skill_info.get("buff", "attack")
#         duration = skill_info.get("duration", 3)
#         print(f"{monster.name} (ID: {monster.id}) howls, buffing {buff_type} for {duration} turns!")
#         # ... (skill implementation: buff other monsters in the room) ...

#     def rest(self, monster, skill_info):
#         """Example skill: Monster rests."""
#         heal_formula = skill_info.get("heal")
#         if callable(heal_formula):
#             actual_heal = int(heal_formula(monster))
#         else:
#             actual_heal = int(heal_formula)
#         print(f"{monster.name} (ID: {monster.id}) rests and heals for {actual_heal}!")
#         # ... (skill implementation: recover some health) ...

#     def add_skill(self, skill_category, skill_name, skill_info):
#         """
#         Adds a skill to the monster's repertoire under a specific category.
#         """
#         if hasattr(self, skill_name) and callable(getattr(self, skill_name)):
#             if skill_category not in self.skills:
#                 self.skills[skill_category] = {}  # Create category if it doesn't exist
#             self.skills[skill_category][skill_name] = skill_info  # Store skill info in the dictionary
#         else:
#             raise ValueError(f"Skill '{skill_name}' is not a valid method of Monster.")

#     def to_dict(self):
#         """
#         Converts the monster object to a dictionary for serialization.
#         """
#         # We need to handle the callable in the skill info
#         serializable_skills = {}
#         for category, skills in self.skills.items():
#             serializable_skills[category] = {}
#             for skill_name, skill_info in skills.items():
#                 serializable_skill_info = {}
#                 for key, value in skill_info.items():
#                     if callable(value):
#                         # Store a string representation of the formula
#                         serializable_skill_info[key] = "formula"
#                     else:
#                         serializable_skill_info[key] = value
#                 serializable_skills[category][skill_name] = serializable_skill_info

#         return {
#             "name": self.name,
#             "id": self.id,
#             "level": self.level,
#             "strength": self.strength,
#             "skills": serializable_skills,  # Now a dictionary of categories
#         }

#     @classmethod
#     def from_dict(cls, data):
#         """
#         Creates a monster object from a dictionary (deserialization).
#         """
#         monster = cls(data["name"], data["id"], data["level"], data["strength"])
#         for skill_category, skills in data["skills"].items():
#             for skill_name, skill_info in skills.items():
#                 deserialized_skill_info = {}
#                 for key, value in skill_info.items():
#                     if value == "formula":
#                         if key == "heal":
#                             deserialized_skill_info[key] = lambda m: 2 * m.level
#                     else:
#                         deserialized_skill_info[key] = value
#                 monster.add_skill(skill_category, skill_name, deserialized_skill_info)
#         return monster


# class Room(MonsterActionManager):
#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#         self.monsters = []

#     def add_monster(self, monster):
#         self.monsters.append(monster)

#     def trigger_monster_skills(self, skill_category):
#         print(f"--- {self.name}: Triggering Monster {skill_category} Skills ---")
#         for monster in self.monsters:
#             self.use_monster_skill(monster, skill_category)
#         print(f"--- {self.name}: End of Monster {skill_category} Skills ---\n")

#     def to_dict(self):
#         """
#         Converts the room object to a dictionary for serialization.
#         """
#         return {
#             "name": self.name,
#             "monsters": [monster.to_dict() for monster in self.monsters],
#         }

#     @classmethod
#     def from_dict(cls, data):
#         """
#         Creates a room object from a dictionary (deserialization).
#         """
#         room = cls(data["name"])
#         for monster_data in data["monsters"]:
#             monster = Monster.from_dict(monster_data)
#             room.add_monster(monster)
#         return room


# # Example Usage:
# if __name__ == "__main__":
#     # Create some monsters
#     wolf1 = Monster("Wolfy", 1, level=5, strength=3)  # Added level and strength
#     wolf1.add_skill("combat", "bite", {"damage": 10, "type": "physical"})  # Added skill info
#     wolf1.add_skill("combat", "howl", {"buff": "attack", "duration": 3})  # Added skill info
#     wolf1.add_skill("general", "rest", {"heal": lambda m: 2 * m.level}) # heal formula

#     wolf2 = Monster("Fang", 2, level=3, strength=5)  # Added level and strength
#     wolf2.add_skill("combat", "bite", {"damage": 12, "type": "physical"})  # Added skill info
#     wolf2.add_skill("general", "rest", {"heal": lambda m: 2 * m.level}) # heal formula

#     spider1 = Monster("Webby", 3, level=2, strength=2)  # Added level and strength
#     spider1.add_skill("combat", "bite", {"damage": 8, "type": "poison"})  # Added skill info
#     spider1.add_skill("general", "rest", {"heal": lambda m: 2 * m.level}) # heal formula

#     # Create a room and add monsters to it
#     forest = Room("Dark Forest")
#     forest.add_monster(wolf1)
#     forest.add_monster(wolf2)

#     cave = Room("Spooky Cave")
#     cave.add_monster(spider1)

#     # Trigger monster skills in the room
#     forest.trigger_monster_skills("combat")
#     cave.trigger_monster_skills("combat")
#     forest.trigger_monster_skills("general")

#     # --- Serialization ---
#     # Convert the room to a dictionary
#     forest_data = forest.to_dict()

#     # Serialize the dictionary to a JSON string
#     forest_json = json.dumps(forest_data, indent=4)
#     print("\n--- Serialized Room (JSON) ---\n")
#     print(forest_json)

#     # --- Deserialization ---
#     # Deserialize the JSON string back to a dictionary
#     loaded_forest_data = json.loads(forest_json)

#     # Create a new room object from the dictionary
#     loaded_forest = Room.from_dict(loaded_forest_data)

#     print("\n--- Deserialized Room: Triggering Skills ---\n")
#     loaded_forest.trigger_monster_skills("combat")
#     loaded_forest.trigger_monster_skills("general")
