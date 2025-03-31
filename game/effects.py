# In game/effects.py

class Effect:
    def __init__(self, name, duration, modifier, description, flat_reduction=0, on_apply=None, on_remove=None, on_turn_start=None, on_damage_taken=None, on_damage_dealt=None, absorb_amount=None, damage_type_effectiveness=None, skill_level=None):
        self.name = name
        self.duration = duration
        self.modifier = modifier
        self.description = description
        self.on_apply = on_apply
        self.on_remove = on_remove
        self.on_turn_start = on_turn_start
        self.on_damage_taken = on_damage_taken
        self.on_damage_dealt = on_damage_dealt
        self.flat_reduction = flat_reduction
        self.absorb_amount = absorb_amount
        self.damage_type_effectiveness = damage_type_effectiveness
        self.skill_level = skill_level

    def apply(self, target):
        """Applies the effect to the target."""
        if self.on_apply:
            self.on_apply(self, target)
        # target._update_cached_stats()

    def remove(self, target):
        """Removes the effect from the target."""
        if self.on_remove:
            self.on_remove(self, target)
        # target._update_cached_stats()

    def turn_start(self, target):
        """Called at the start of the target's turn."""
        if self.on_turn_start:
            self.on_turn_start(self, target)

    def damage_taken(self, target, damage):
        """Called when the target takes damage."""
        if self.on_damage_taken:
            if isinstance(self.on_damage_taken, dict):
                for trigger_name, trigger_data in self.on_damage_taken.items():
                    if trigger_name == "healing_on_damage_taken":
                        heal_amount = trigger_data["level_unlocks"].get(self.skill_level, 0)  # Default to 0 if level not found
                        if heal_amount:
                            target.heal(heal_amount)
                            print(f"[DEBUG healing_on_damage_trigger] {target.name} heals for {heal_amount} health due to healing_on_damage effect!")
            elif callable(self.on_damage_taken):
                self.on_damage_taken(self, target, damage)

    def damage_dealt(self, target, damage):
        """Called when the target deals damage."""
        if self.on_damage_dealt:
            self.on_damage_dealt(self, target, damage)

    def turn_start(self, target):
        """Called at the start of the target's turn."""
        if self.name == "poison":
            print(f"{target.name} takes {self.modifier} poison damage!")
            target.take_damage(self.modifier, "poison")
        if self.on_turn_start:
            self.on_turn_start(self, target)

    def to_dict(self):
        """Converts the effect object to a dictionary for serialization."""
        return {
            "name": self.name,
            "duration": self.duration,
            "modifier": self.modifier,
            "description": self.description,
            "flat_reduction": self.flat_reduction,
            "absorb_amount": self.absorb_amount,
            "damage_type_effectiveness": self.damage_type_effectiveness,
            "on_damage_taken": self.on_damage_taken,
            "skill_level": self.skill_level
        }

    @classmethod
    def from_dict(cls, data):
        """Creates an effect object from a dictionary (deserialization)."""
        return cls(
            name=data["name"],
            duration=data["duration"],
            modifier=data["modifier"],
            description=data["description"],
            flat_reduction=data.get("flat_reduction", 0),
            absorb_amount=data.get("absorb_amount", None),
            damage_type_effectiveness=data.get("damage_type_effectiveness", None),
            on_damage_taken=data.get("on_damage_taken", None),
            skill_level=data.get("skill_level", None)
        )
