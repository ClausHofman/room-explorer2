import uuid, json, random, threading, time, copy
import room as room_module
from managers import *


def create_companion(creature_type, companion_data, creature_traits, status_data, selected_traits=None):
    from combatants import Companion
    """
    Creates a Player object by extracting the data for the given creature type.

    :param creature_type: The type of the creature (e.g., "dragon").
    :param creature_data: A dictionary containing data for all creatures.
    :param creature_traits: A dictionary containing optional traits.
    :param status_data: A dictionary containing buffs and debuffs.
    :param selected_traits: A list of selected traits.
    :return: A fully initialized Monster object.
    """
    if creature_type not in companion_data:
        raise ValueError(f"Creature type '{creature_type}' does not exist in companion_data.")
    
    # Extract specific companion's data
    companion_info = companion_data[creature_type]
    
    # Construct combatant stats
    stats = {
        "health": companion_info["health"],
        "attack": companion_info["attack"],
        "defense": companion_info["defense"]
    }
    
    # Generate a unique combatant ID
    combatant_id = f"{creature_type}_{uuid.uuid4().hex[:6]}"
    
    # Return a Companion object
    return Companion(
        combatant_id=combatant_id,
        name=companion_info["name"],
        stats=stats,
        hates_all=companion_info.get("hates_all", False),
        hates_player_and_companions=companion_info.get("hates_player_and_companions", False),
        hates=companion_info.get("hates", []),
        monster_type=companion_info.get("monster_type", None),
        has_traits=companion_info["has_traits"],
        all_creature_traits_data=creature_traits,
        status_data=status_data,
        selected_traits=selected_traits
    )

def create_player(creature_type, player_data, creature_traits, status_data, selected_traits=None):
    from combatants import Player
    """
    Creates a Player object by extracting the data for the given creature type.

    :param creature_type: The type of the creature (e.g., "dragon").
    :param creature_data: A dictionary containing data for all creatures.
    :param creature_traits: A dictionary containing optional traits.
    :param status_data: A dictionary containing buffs and debuffs.
    :param selected_traits: A list of selected traits.
    :return: A fully initialized Monster object.
    """
    if creature_type not in player_data:
        raise ValueError(f"Creature type '{creature_type}' does not exist in player_data.")
    
    # Extract specific creature's data
    player_info = player_data[creature_type]
    
    # Construct combatant stats
    stats = {
        "health": player_info["health"],
        "attack": player_info["attack"],
        "defense": player_info["defense"]
    }
    
    # Generate a unique combatant ID
    combatant_id = f"{creature_type}_{uuid.uuid4().hex[:6]}"
    
    # Return a Player object
    return Player(
        combatant_id=combatant_id,
        name=player_info["name"],
        stats=stats,
        hates_all=player_info.get("hates_all", False),
        hates_player_and_companions=player_info.get("hates_player_and_companions", False),
        hates=player_info.get("hates", []),
        monster_type=player_info.get("monster_type", None),
        has_traits=player_info["has_traits"],
        all_creature_traits_data=creature_traits,
        status_data=status_data,
        selected_traits=selected_traits
    )

def create_creature(creature_type, creature_data, creature_traits, status_data, selected_traits=None):
    from combatants import Monster
    """
    Creates a Monster object by extracting the data for the given creature type.

    :param creature_type: The type of the creature (e.g., "dragon").
    :param creature_data: A dictionary containing data for all creatures.
    :param creature_traits: A dictionary containing optional traits.
    :param status_data: A dictionary containing buffs and debuffs.
    :param selected_traits: A list of selected traits.
    :return: A fully initialized Monster object.
    """
    if creature_type not in creature_data:
        raise ValueError(f"Creature type '{creature_type}' does not exist in creature_data.")
    
    # Extract specific creature's data
    creature_info = creature_data[creature_type]
    
    # Construct combatant stats
    stats = {
        "health": creature_info["health"],
        "attack": creature_info["attack"],
        "defense": creature_info["defense"]
    }
    
    # Generate a unique combatant ID
    combatant_id = f"{creature_type}_{uuid.uuid4().hex[:6]}"
    
    # Return a Monster object
    return Monster(
        combatant_id=combatant_id,
        name=creature_info["name"],
        stats=stats,
        hates_all=creature_info.get("hates_all", False),
        hates_player_and_companions=creature_info.get("hates_player_and_companions", False),
        hates=creature_info.get("hates", []),
        monster_type=creature_info.get("monster_type", None),
        has_traits=creature_info["has_traits"],
        all_creature_traits_data=creature_traits,
        status_data=status_data,
        selected_traits=selected_traits
    )


class Combatant:
    def __init__(self, combatant_id, name, stats, hates_all=False, hates_player_and_companions=False, hates=None, monster_type=None):
        """
        :param combatant_id: Unique ID for the combatant.
        :param name: Name of the combatant.
        :param stats: A dictionary containing combatant stats (health, attack, defense, etc.).
        :param hates_all: Whether the combatant hates all entities.
        :param hates_player_and_companions: Whether the combatant hates the player and companions.
        :param hates: Specific entities the combatant hates.
        :param monster_type: Type of the combatant, if applicable (e.g., "dragon").
        """
        self.id = combatant_id
        self.name = name
        self.stats = stats
        self.hates_all = hates_all
        self.hates_player_and_companions = hates_player_and_companions
        self.hates = hates or []  # Defaults to an empty list if not provided
        self.monster_type = monster_type
        self.grudge_list = []  # Tracks IDs of entities this combatant is hostile toward

    def is_alive(self):
            return self.stats["health"] > 0

    def take_damage(self, damage):
        self.stats["health"] -= damage
        if self.stats["health"] <= 0:
            print(f"[DEBUG] {self.name} has been defeated!")
            self.grudge_list.clear()  # Clear grudges when defeated
            print(f"[DEBUG] Cleared grudge list for {self.name} (ID: {self.id})")
        return self.stats["health"] > 0

    def add_to_grudge_list(self, attacker_id):
        if attacker_id not in self.grudge_list:
            self.grudge_list.append(attacker_id)
            print(f"[DEBUG] {self.name} adds {attacker_id} to grudge list")

    # Serialization method
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "health": self.stats["health"],
            "attack": self.stats["attack"],
            "defense": self.stats["defense"],
            "hates_all": self.hates_all,
            "hates_player_and_companions": self.hates_player_and_companions,
            "hates": self.hates,
            "monster_type": self.monster_type,
            "grudge_list": self.grudge_list,
            "status_effect": {
                "buffs": self.combatant_manager.buffs if self.combatant_manager and isinstance(self.combatant_manager.buffs, dict) else {},
                "debuffs": self.combatant_manager.debuffs if self.combatant_manager and isinstance(self.combatant_manager.debuffs, dict) else {}
            }            
        }

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        # Create a new instance of Combatant from a dictionary
        stats = {
                    "health": data["stats"]["health"],
                    "attack": data["stats"]["attack"],
                    "defense": data["stats"]["defense"]}
        status_effects = data.get("status_effect", {"buffs": {}, "debuffs": {}})

        instance = cls(
            combatant_id=data["id"],
            name=data["name"],
            stats = stats,
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None),
            has_traits=data.get("has_traits", {}),
            all_creature_traits_data=data.get("all_creature_traits_data", {}),
            status_effects=status_effects,  # Rebuild status data
            selected_traits=data.get("selected_traits", None)            
        )
        instance.grudge_list = data.get("grudge_list", [])  # Restore grudges
        return instance


class Player(Combatant):
    def __init__(self, combatant_id, name, stats, hates_all, hates_player_and_companions, hates, monster_type, has_traits, all_creature_traits_data, status_data, selected_traits=None):
        super().__init__(combatant_id, name, stats, hates_all, hates_player_and_companions, hates, monster_type)
        self.has_traits = has_traits
        self.combatant_manager = CombatantManager(
            traits_dict=all_creature_traits_data,
            status_effects=status_data["status_effect"],
            selected_traits=selected_traits)
        self.inventory = ("inventory", [])
        self.equipment = ("equipment", {})

    # Serialization method
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "inventory": self.inventory,
            "equipment": self.equipment,
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

        # Extract and organize status effects properly
        status_data = {
            "status_effect": data.get("status_effect", {"buffs": {}, "debuffs": {}})
        }

        # Rebuild the Player object
        return cls(
            combatant_id=data["id"],
            name=data["name"],
            stats=stats,
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None),
            has_traits=data.get("has_traits", {}),
            all_creature_traits_data=data.get("all_creature_traits_data", {}),
            status_data=status_data,  # Pass status_effect
            selected_traits=data.get("selected_traits", None)
        )



class Companion(Combatant):
    def __init__(self, combatant_id, name, stats, hates_all, hates_player_and_companions, hates, monster_type, has_traits, all_creature_traits_data, status_data, selected_traits=None):
        super().__init__(combatant_id, name, stats, hates_all, hates_player_and_companions, hates, monster_type)
        self.has_traits = has_traits
        self.combatant_manager = CombatantManager(
            traits_dict=all_creature_traits_data,
            status_effects=status_data["status_effect"],
            selected_traits=selected_traits)
        self.inventory =("inventory", [])
        self.equipment =("equipment", {})

    # Serialization method
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "inventory": self.inventory,
            "equipment": self.equipment,
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

        # Extract and organize status effects properly
        status_data = {
            "status_effect": data.get("status_effect", {"buffs": {}, "debuffs": {}})
        }

        return cls(
            combatant_id=data["id"],
            name=data["name"],
            stats=stats,
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None),
            has_traits=data.get("has_traits", {}),
            all_creature_traits_data=data.get("all_creature_traits_data", {}),
            status_data=status_data,
            selected_traits=data.get("selected_traits", None)
        )


class Monster(Combatant):
    def __init__(self, combatant_id, name, stats, hates_all, hates_player_and_companions, hates, monster_type, has_traits, all_creature_traits_data, status_data, selected_traits=None):
        """
        :param combatant_id: Unique ID for the combatant.
        :param name: Name of the monster.
        :param stats: A dictionary containing stats (health, attack, defense, etc.).
        :param hates_all: Whether the monster hates all entities.
        :param hates_player_and_companions: Whether the monster hates the player and companions.
        :param hates: Specific entities the monster hates.
        :param monster_type: Type of the monster.
        :param has_traits: The monster's default traits.
        :param all_creature_traits_data: A dictionary of all optional traits.
        :param status_data: A dictionary containing buffs and debuffs.
        :param selected_traits: A list of selected traits.
        """
        super().__init__(combatant_id, name, stats, hates_all, hates_player_and_companions, hates, monster_type)
        self.has_traits = has_traits
        self.combatant_manager = CombatantManager(
            traits_dict=all_creature_traits_data,
            status_effects=status_data,
            selected_traits=selected_traits
        )
        self._apply_selected_traits()

    def _apply_selected_traits(self):
        # Append selected traits to the monster's default traits
        self.has_traits.update(self.combatant_manager.selected_traits)

    def describe(self):
        """
        Provides a summary of the monster's attributes.
        """
        stats_description = ", ".join([f"{key}: {value}" for key, value in self.stats.items()])
        hates_description = (
            f"Hates All: {self.hates_all}, "
            f"Hates Player/Companions: {self.hates_player_and_companions}, "
            f"Hates Specific: {', '.join(self.hates) if self.hates else 'None'}"
        )
        return (
            f"{self.name} ({self.monster_type})\n"
            f"Stats: {stats_description}\nTraits: {self.has_traits}\n{hates_description}"
        )

    def _apply_selected_traits(self):
        self.has_traits.update(self.combatant_manager.selected_traits)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name,
            "stats": self.stats,
            "has_traits": {key: value for key, value in self.has_traits.items()},
        })
        return base

    @classmethod
    def from_dict(cls, data):
        stats = {
            "health": data["stats"]["health"],
            "attack": data["stats"]["attack"],
            "defense": data["stats"]["defense"]}
        
        # Extract and organize status effects properly
        status_data = {
            "status_effect": data.get("status_effect", {"buffs": {}, "debuffs": {}})
        }

        return cls(
            combatant_id=data["id"],
            name=data["name"],
            stats=stats,
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None),
            has_traits=data.get("has_traits", {}),
            all_creature_traits_data=data.get("all_creature_traits_data", {}),
            status_data=status_data,
            selected_traits=data.get("selected_traits", None)
        )


    def _apply_selected_traits(self):
        self.has_traits.update(self.combatant_manager.selected_traits)
