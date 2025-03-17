# Global Player, Companions, and Monsters Data
player_data = {
    "id": "player",
    "name": "Claus",
    "inventory": ["Potion", "Sword"],
    "equipment": {"weapon": "Basic Sword", "armor": "Cloth Armor"},
    "stats": {"health": 100, "attack": 20, "defense": 10}
}

companions_data = {
    "companion1": {
        "name": "Companion A",
        "stats": {"health": 80, "attack": 15, "defense": 8}
    }
}

monsters_data = {
    "goblin": {
        "name": "Goblin",
        "health": 50,
        "attack": 12,
        "defense": 5,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": ["animal"],  # Goblins hate animals
        "monster_type": "goblin"
    },
    "wolf": {
        "name": "Wolf",
        "health": 60,
        "attack": 15,
        "defense": 7,
        "hates_all": True,  # Hates everyone
        "hates_player_and_companions": False,
        "monster_type": "animal"  # Wolves are animals
    },
    "rabbit": {
        "name": "Rabbit",
        "health": 30,
        "attack": 5,
        "defense": 2,
        "hates_all": False,
        "hates_player_and_companions": False,
        "hates": [],  # Rabbits are peaceful
        "monster_type": "animal"
    }
}