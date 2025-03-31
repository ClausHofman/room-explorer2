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
            "cooldown": 2,
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
        "poison_bite": {
            "base_damage": 5,
            "stat_scaling": "strength",
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "A bite that poisons the target.",
            "effects": ["poison"],  # Apply the poison effect
            "cooldown": 100,
            "current_cooldown": 0
        }
    },
    "passive_defense": {
        "iron_skin": {
            "flat_reduction": 50,
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Reduces incoming damage by a flat amount.",
            "affects": ["take_damage"],
        },
        "tough_hide": {
            "percent_reduction": 0.50,  # 10% damage reduction
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Reduces incoming damage by 10%.",
            "affects": ["take_damage"],
        }
    },
    "passive_offense": {
        "attack": {
            "base_damage": 0,
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "A basic attack.",
            "flat_stat_scaling": "strength",
            "flat_scaling_value": 1,
        },
    },
    "restoration_magic": {
        "cure_light_wounds": {
            "base_heal": 200,
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
    "defensive_magic": {
        "magic_shield": {
            "duration": 10,
            "flat_reduction": 5,
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Creates a temporary magic shield that reduces incoming damage.",
            "effects": ["magic_shield_effect"],
            "cooldown": 5,
            "current_cooldown": 0
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
            "duration": 50,
            "modifier": 20,
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Deals damage over time.",
        },
        "magic_shield_effect": {
            "duration": 3,
            "flat_reduction": 5,
            "level_scaling_factor": 0.002,
            "level": 1,
            "active": True,
            "description": "Reduces incoming damage by a flat amount.",
        }
    }
}
