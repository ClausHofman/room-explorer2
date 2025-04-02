class Equipment:
    def __init__(self, name, equipment_type, damage_types=None, base_damage=0, effects=None, required_stats=None, description=None):
        self.name = name
        self.equipment_type = equipment_type  # e.g., "main_hand", "off_hand", "armor", "ring"
        self.damage_types = damage_types or []  # e.g., ["physical"], ["fire", "physical"]
        self.base_damage = base_damage
        self.effects = effects or []  # List of Effect objects (or similar)
        self.required_stats = required_stats or {} # e.g. {"strength": 10}
        self.description = description or ""

    def to_dict(self):
        return {
            "name": self.name,
            "equipment_type": self.equipment_type,
            "damage_types": self.damage_types,
            "base_damage": self.base_damage,
            "effects": [effect.to_dict() for effect in self.effects],
            "required_stats": self.required_stats,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        from game.effects import Effect
        return cls(
            name=data["name"],
            equipment_type=data["equipment_type"],
            damage_types=data.get("damage_types", []),
            base_damage=data.get("base_damage", 0),
            effects=[Effect.from_dict(effect_data) for effect_data in data.get("effects", [])],
            required_stats=data.get("required_stats", {}),
            description=data.get("description", "")
        )
