# In game/effects.py

class Effect:
    def __init__(self, name, duration, modifier, description, on_apply=None, on_remove=None, on_turn_start=None, on_damage_taken=None, on_damage_dealt=None):
        self.name = name
        self.duration = duration
        self.modifier = modifier
        self.description = description
        self.on_apply = on_apply
        self.on_remove = on_remove
        self.on_turn_start = on_turn_start
        self.on_damage_taken = on_damage_taken
        self.on_damage_dealt = on_damage_dealt

    def apply(self, target):
        """Applies the effect to the target."""
        if self.on_apply:
            self.on_apply(self, target)

    def remove(self, target):
        """Removes the effect from the target."""
        if self.on_remove:
            self.on_remove(self, target)

    def turn_start(self, target):
        """Called at the start of the target's turn."""
        if self.on_turn_start:
            self.on_turn_start(self, target)

    def damage_taken(self, target, damage):
        """Called when the target takes damage."""
        if self.on_damage_taken:
            self.on_damage_taken(self, target, damage)

    def damage_dealt(self, target, damage):
        """Called when the target deals damage."""
        if self.on_damage_dealt:
            self.on_damage_dealt(self, target, damage)

    def to_dict(self):
        """Converts the effect object to a dictionary for serialization."""
        return {
            "name": self.name,
            "duration": self.duration,
            "modifier": self.modifier,
            "description": self.description,
            # We don't serialize the methods (on_apply, on_remove, etc.) for now
        }

    @classmethod
    def from_dict(cls, data):
        """Creates an effect object from a dictionary (deserialization)."""
        return cls(
            name=data["name"],
            duration=data["duration"],
            modifier=data["modifier"],
            description=data["description"],
            # We don't deserialize the methods (on_apply, on_remove, etc.) for now
        )
