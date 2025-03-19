import uuid

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

