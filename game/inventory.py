
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"{item.name} added to your inventory.")

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                print(f"{item_name} removed from your inventory.")
                return item
        print(f"No item named '{item_name}' found in your inventory.")
        return None

    def display(self):
        if self.items:
            print("Your inventory:")
            for item in self.items:
                print(f"- {item.name}: {item.description}")
        else:
            print("Your inventory is empty.")

    def to_dict(self):
        """Convert the Inventory to a dictionary for serialization."""
        return {
            "items": [item.to_dict() for item in self.items]  # Serialize each item
        }

    @staticmethod
    def from_dict(data):
        """Rebuild the Inventory from a dictionary."""
        inventory = Inventory()
        inventory.items = [Item.from_dict(item_data) for item_data in data.get("items", [])]
        return inventory

class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def to_dict(self):
        return {"name": self.name, "description": self.description, "value": self.value}

    @staticmethod
    def from_dict(data):
        return Item(data["name"], data["description"], data["value"])
