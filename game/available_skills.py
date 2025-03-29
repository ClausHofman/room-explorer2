# In game/available_skills.py

available_skills = {
    "offensive_melee": {
        "slash": {
            "base_damage": 5,
            "scaling": "strength",
            "description": "A basic melee attack.",
            "effects": []
        },
        "double_slash": {
            "base_damage": 8,
            "scaling": "strength",
            "description": "A more powerful melee attack.",
            "effects": []
        },
        "fireball": {
            "base_damage": 10,
            "scaling": "intelligence",
            "description": "Hurls a ball of fire at the target.",
            "effects": []
        },
        "fire_breath": {
            "base_damage": 7,
            "scaling": "intelligence",
            "description": "Breathes fire at the target.",
            "effects": []
        },
        "bite": {
            "base_damage": 3,
            "scaling": "strength",
            "description": "A basic bite attack.",
            "effects": []
        },
        "double_bite": {
            "base_damage": 6,
            "scaling": "strength",
            "description": "A more powerful bite attack.",
            "effects": []
        },
        "poison_bite": {  # Added poison_bite skill
            "base_damage": 2,
            "scaling": "strength",
            "description": "A bite that poisons the target.",
            "effects": ["poison"]  # Apply the "poison" effect
        }
    },
    "passive_defense": {
        "iron_skin": {
            "reduction": 2,
            "description": "Reduces incoming damage.",
            "affects": ["take_damage"],
            "active": True
        }
    },
    "passive_offense": {
        # ... (add passive offense skills here later) ...
    },
    "effects": {
        "poison": {
            "duration": 5,
            "modifier": 2,
            "description": "Deals damage over time.",
            # Add other effect attributes here
        }
    }
}
