import uuid

class Combatant:
    def __init__(self, combatant_id, name, health, attack, defense, hates_all=False, hates_player_and_companions=False, hates=None, monster_type=None):
        self.id = combatant_id
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.hates_all = hates_all
        self.hates_player_and_companions = hates_player_and_companions
        self.hates = hates or []  # Defaults to an empty list if not provided
        self.monster_type = monster_type
        self.grudge_list = []  # Tracks IDs of entities this combatant is hostile toward

        # Debugging: Validate Initialization
        print(f"[DEBUG] Created Combatant: {self.name} (ID: {self.id}), Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}")

    # Serialization method
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "health": self.health,
            "attack": self.attack,
            "defense": self.defense,
            "hates_all": self.hates_all,
            "hates_player_and_companions": self.hates_player_and_companions,
            "hates": self.hates,
            "monster_type": self.monster_type,
            "grudge_list": self.grudge_list  # Include grudges in the dictionary
        }

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        # Create a new instance of Combatant from a dictionary
        instance = cls(
            combatant_id=data["id"],
            name=data["name"],
            health=data["health"],
            attack=data["attack"],
            defense=data["defense"],
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None)
        )
        instance.grudge_list = data.get("grudge_list", [])  # Restore grudges
        return instance

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"[DEBUG] {self.name} has been defeated!")
            self.grudge_list.clear()  # Clear grudges when defeated
            print(f"[DEBUG] Cleared grudge list for {self.name} (ID: {self.id})")
        return self.health > 0

    def add_to_grudge_list(self, attacker_id):
        if attacker_id not in self.grudge_list:
            self.grudge_list.append(attacker_id)
            print(f"[DEBUG] {self.name} adds {attacker_id} to grudge list")

class Player(Combatant):
    def __init__(self, data):
        super().__init__(
            combatant_id=data["id"],
            name=data["name"],
            health=data["stats"]["health"],
            attack=data["stats"]["attack"],
            defense=data["stats"]["defense"]
        )
        self.inventory = data.get("inventory", [])
        self.equipment = data.get("equipment", {})
        print(f"[DEBUG] Player initialized: {self.name} (ID: {self.id})")

    # Serialization method
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "inventory": self.inventory,
            "equipment": self.equipment
        })
        return base

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        stats = {
            "health": data["health"],
            "attack": data["attack"],
            "defense": data["defense"]
        }
        player_data = {
            "id": data["id"],
            "name": data["name"],
            "stats": stats,
            "inventory": data.get("inventory", []),
            "equipment": data.get("equipment", {})
        }
        return cls(player_data)

class Companion(Combatant):
    def __init__(self, id, data):
        super().__init__(
            combatant_id=id,
            name=data["name"],
            health=data["stats"]["health"],
            attack=data["stats"]["attack"],
            defense=data["stats"]["defense"]
        )
        print(f"[DEBUG] Companion initialized: {self.name} (ID: {self.id})")

    # Serialization method
    def to_dict(self):
        return super().to_dict()

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        companion_data = {
            "name": data["name"],
            "stats": {
                "health": data["health"],
                "attack": data["attack"],
                "defense": data["defense"]
            }
        }
        return cls(data["id"], companion_data)

class Monster(Combatant):
    def __init__(self, id, data):
        super().__init__(
            combatant_id=f"monster_{id}_{uuid.uuid4().hex[:6]}",
            name=data["name"],
            health=data["health"],
            attack=data["attack"],
            defense=data["defense"],
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None)
        )
        print(f"[DEBUG] Monster initialized: {self.name} (ID: {self.id})")

    # Serialization method
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "hates_all": self.hates_all,
            "hates_player_and_companions": self.hates_player_and_companions,
            "hates": self.hates,
            "monster_type": self.monster_type
        })
        return base

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        monster_data = {
            "name": data["name"],
            "health": data["health"],
            "attack": data["attack"],
            "defense": data["defense"],
            "hates_all": data.get("hates_all", False),
            "hates_player_and_companions": data.get("hates_player_and_companions", False),
            "hates": data.get("hates", []),
            "monster_type": data.get("monster_type", None)
        }
        return cls(data["id"], monster_data)
