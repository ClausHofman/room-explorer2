# In game/available_skills.py

available_skills = {
    "offensive_melee": {
        "slash": {
            "base_damage": 20,
            "stat_scaling": "strength",
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "A basic melee attack.",
            "effects": [],
            "cooldown": 1,
            "current_cooldown": 1
        },
        "fireball": {
            "base_damage": 10,
            "stat_scaling": "intelligence",
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Hurls a ball of fire at the target.",
            "effects": [],
            "cooldown": 3,
            "current_cooldown": 0
        },
        "fire_breath": {
            "base_damage": 10,
            "stat_scaling": "intelligence",
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Breathes fire at the target.",
            "effects": [],
            "cooldown": 3,
            "current_cooldown": 0
        },
    },
    "restoration_magic": {
        "cure_light_wounds": {
            "base_heal": 20,
            "stat_scaling": "wisdom",
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Heals a small amount of health.",
            "effects": [],
            "cooldown": 1,
            "current_cooldown": 0
        }
    },
    "passive_defense": {
        "iron_skin": {
            "reduction": 2,
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Reduces incoming damage.",
            "affects": ["take_damage"],
        }
    },
    "passive_offense": {
        "attack": {
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "A basic attack.",
            "flat_stat_scaling": "strength",
            "flat_scaling_value": 1,
        }
    },
    "general": {
        "combat_initiative": {
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Determines the combatant's initiative in combat.",
        }
    },
    "effects": {
        "poison": {
            "duration": 5,
            "modifier": 2,
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Deals damage over time.",
        }
    }
}
