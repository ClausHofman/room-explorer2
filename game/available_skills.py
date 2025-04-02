# In game/available_skills.py
# In game/available_skills.py

available_skills = {
    "offensive_melee": {
        "slash": {
            "base_damage": 20,
            "level": 1,
            "active": True,
            "description": "A basic melee attack.",
            "effects": [],
            "cooldown": 2,
            "current_cooldown": 1,
            "damage_types": ["physical"],
            "scaling_rules": {
                "stat_scaling": "strength",
                "level_scaling_factor": 0.002,
            }
        },
        "fireball": {
            "base_damage": 10,
            "level": 1,
            "active": True,
            "description": "Hurls a ball of fire at the target.",
            "effects": [],
            "cooldown": 3,
            "current_cooldown": 0,
            "damage_types": ["fire"],
            "scaling_rules": {
                "stat_scaling": "intelligence",
                "level_scaling_factor": 0.002,
            }
        },
        "fire_breath": {
            "base_damage": 10,
            "level": 1,
            "active": True,
            "description": "Breathes fire at the target.",
            "effects": [],
            "cooldown": 3,
            "current_cooldown": 0,
            "scaling_rules": {
                "stat_scaling": "intelligence",
                "level_scaling_factor": 0.002,
            }
        },
        "poison_bite": {
            "base_damage": 5,
            "level": 1,
            "active": True,
            "description": "A bite that poisons the target.",
            "effects": ["poison"],  # Apply the poison effect
            "cooldown": 100,
            "current_cooldown": 0,
            "scaling_rules": {
                "stat_scaling": "strength",
                "level_scaling_factor": 0.002,
            }
        }
    },
    "passive_defense": {
        "iron_skin": {
            "flat_reduction": 50,
            "level": 1,
            "active": True,
            "description": "Reduces incoming damage by a flat amount.",
            "affects": ["take_damage"],
            "scaling_rules": {
                "level_scaling_factor": 0.002,
            }
        },
        "tough_hide": {
            "percent_reduction": 0.50,  # 10% damage reduction
            "level": 1,
            "active": True,
            "description": "Reduces incoming damage by 10%.",
            "affects": ["take_damage"],
            "scaling_rules": {
                "level_scaling_factor": 0.002,
            }
        }
    },
    "passive_offense": {
        "attack": {
            "base_damage": 0,
            "level": 100,
            "active": True,
            "description": "A basic attack.",
            "damage_types": ["physical"],
            "scaling_rules": {
                "level_scaling_factor": 0.002,
                "flat_stat_scaling": "strength",
                "flat_scaling_value": 0.25,
            }
        },
    },
    "restoration_magic": {
        "cure_light_wounds": {
            "base_heal": 200,
            "level": 1,
            "active": True,
            "description": "Heals a small amount of health.",
            "effects": [],
            "cooldown": 1,
            "current_cooldown": 0,
            "scaling_rules": {
                "stat_scaling": "wisdom",
                "level_scaling_factor": 0.002,
            }
        }
    },
    "defensive_magic": {
        "magic_shield": {
            "description": "Creates a magic shield that reduces incoming damage.",
            "cooldown": 5,
            "current_cooldown": 0,
            "base_flat_reduction": 50,
            "base_duration": 3,
            "level": 10,
            "active": True,
            "scaling_rules": {
                "stat_scaling": {
                    "intelligence": 0.2,
                    "willpower": 0.2,
                },
                "level_scaling_factor": 0.1,
                "flat_reduction_per_level": 1,
                "duration_per_level": 1,
                "description": "A magic shield that reduces incoming damage.",
                "on_damage_taken": {
                    "healing_on_damage_taken": {
                        "level_unlocks": {
                            10: 5,
                            20: 10,
                        }
                    }
                }
            }
        },
    },
    "general": {
        "combat_initiative": {
            "level": 1,
            "active": True,
            "description": "Determines the combatant's initiative in combat.",
            "scaling_rules": {
                "level_scaling_factor": 0.002,
            }
        }
    },
    "effects": {
        "poison": {
            "duration": 50,
            "modifier": 20,
            "level": 1,
            "active": True,
            "description": "Deals damage over time.",
            "scaling_rules": {
                "level_scaling_factor": 0.002,
            }
        },
    },
    "effects_skills": ["magic_shield"]
}
