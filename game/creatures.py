class Creature:
    def __init__(self, name, description, health):
        self.name = name
        self.description = description
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} takes {damage} damage!")
        if self.health <= 0:
            print(f"{self.name} has been defeated.")
            self.health = 0  # Ensure health doesn't go negative

    def heal(self, amount):
        self.health += amount
        print(f"{self.name} heals for {amount}. Health is now {self.health}.")

    def describe(self):
        print(f"{self.name}: {self.description} (Health: {self.health})")

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "health": self.health
        }

    @staticmethod
    def from_dict(data):
        return Creature(data["name"], data["description"], data["health"])
