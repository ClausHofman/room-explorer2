# In game/combatant_data.py

companion_data = {
    "companion": {
        "id": "companion",
        "name": "Companion A",
        "health": 100,
        "spell_points": 100,
        "attack": 50,
        "defense": 30,
        "strength": 1,
        "dexterity": 1,
        "intelligence": 1,
        "wisdom": 1,
        "willpower": 1,
        "constitution": 1,
        "level": 1,
        "health_per_level": 10,
        "spell_points_per_level": 5,
        "health_per_constitution": 10,
        "damage_per_strength": 2,
        "spell_points_per_intelligence": 3,
        "defense_per_constitution": 1,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "companion",
        "skills": {
            "offensive_melee": ["poison_bite"],
            "passive_offense": ["attack"],
            "general": ["combat_initiative"],
            "restoration_magic": ["cure_light_wounds"]
        },
        "has_traits": {}
    }
}

player_data = {
    "player": {
        "id": "player",
        "name": "Claus",
        "health": 100,
        "spell_points": 100,
        "attack": 50,
        "defense": 30,
        "strength": 100,
        "dexterity": 10,
        "intelligence": 1,
        "wisdom": 1,
        "willpower": 1,
        "constitution": 1,
        "level": 1,
        "health_per_level": 10,
        "spell_points_per_level": 5,
        "health_per_constitution": 10,
        "damage_per_strength": 2,
        "spell_points_per_intelligence": 3,
        "defense_per_constitution": 1,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "player",
        "has_traits": {
            "admin": "Mysterious admin powers"
        },
        "skills": {
            "offensive_melee": ["poison_bite"],
            "passive_offense": ["attack"],
            "general": ["combat_initiative"]
        }
    }
}

creature_data = {
    "dragon": {
        "id": "dragon",
        "name": "Flame Wyvern",
        "health": 1000,
        "spell_points": 100,
        "attack": 4,
        "defense": 0,
        "strength": 2,
        "dexterity": 2,
        "intelligence": 5,
        "wisdom": 5,
        "willpower": 5,
        "constitution": 2,
        "level": 1,
        "health_per_level": 20,
        "spell_points_per_level": 5,
        "health_per_constitution": 15,
        "damage_per_strength": 3,
        "spell_points_per_intelligence": 5,
        "defense_per_constitution": 2,
        "hates_all": True,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "dragon",
        "has_traits": {"fire_breath": True},
        "skills": {
            "offensive_melee": ["fireball"],
            "passive_defense": [],
            "passive_offense": ["attack"],
            "restoration_magic": ["cure_light_wounds"],
            "defensive_magic": ["magic_shield"],
            "general": ["combat_initiative"]
        }
    },
    "goblin": {
        "id": "goblin",
        "name": "Small sneaky goblin",
        "health": 5,
        "spell_points": 50,
        "attack": 2,
        "defense": 2,
        "strength": 1,
        "dexterity": 1,
        "intelligence": 1,
        "wisdom": 1,
        "willpower": 1,
        "constitution": 1,
        "level": 1,
        "health_per_level": 5,
        "spell_points_per_level": 1,
        "health_per_constitution": 10,
        "damage_per_strength": 2,
        "spell_points_per_intelligence": 3,
        "defense_per_constitution": 1,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": ["animal"],
        "monster_type": "goblin",
        "skills": {
            "passive_offense": ["attack"],
            "general": ["combat_initiative"]
        },
        "has_traits": {}
    },
    "wolf": {
        "id": "wolf",
        "name": "Young wolf",
        "health": 10,
        "spell_points": 10,
        "attack": 3,
        "defense": 4,
        "strength": 4,
        "dexterity": 1,
        "intelligence": 1,
        "wisdom": 1,
        "willpower": 1,
        "constitution": 1,
        "level": 1,
        "health_per_level": 10,
        "spell_points_per_level": 1,
        "health_per_constitution": 5,
        "damage_per_strength": 3,
        "spell_points_per_intelligence": 1,
        "defense_per_constitution": 1,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": ["animal"],
        "monster_type": "wolf",
        "has_traits": {},
        "skills": {
            "passive_offense": ["attack"],
            "general": ["combat_initiative"]
        }
    },
    "rabbit": {
        "id": "rabbit",
        "name": "Small rabbit",
        "health": 3,
        "spell_points": 5,
        "attack": 1,
        "defense": 1,
        "strength": 1,
        "dexterity": 10,
        "intelligence": 1,
        "wisdom": 1,
        "willpower": 1,
        "constitution": 1,
        "level": 1,
        "health_per_level": 4,
        "spell_points_per_level": 1,
        "health_per_constitution": 2,
        "damage_per_strength": 1,
        "spell_points_per_intelligence": 1,
        "defense_per_constitution": 1,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],
        "monster_type": "rabbit",
        "has_traits": {},
        "skills": {
            "passive_offense": ["attack"],
            "general": ["combat_initiative"]
        }
    }
}


# Example creature_traits dictionary (optional traits)
creature_traits_data = {
    "flight": True,
    "regeneration": "Moderate",
    "fire_resistance": "High",
    "poison_immunity": True
}

# Example creature_status_data dictionary (default status effects)
creature_status_data = {
    "status_effect": {
        "buffs": {
            "strength_boost": [0, 0]  # Default duration and effect
        },
        "debuffs": {
            "poisoned": [0, 0]  # Default duration and effect
        }
    }
}
