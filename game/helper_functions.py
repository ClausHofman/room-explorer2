import uuid
import combatant_data
from managers import TurnManager, RoomManager, MovementManager
from shared_resources import stop_event
print("helper_functions.py stop event:", stop_event)
print(f"helper_functions.py stop_event: {id(stop_event)}")
import room

turn_interval = None
turn_manager = None
player = None
movement_manager = None
room_manager = None
start_current_player_room = None

def initialize_game():
    global turn_interval
    global movement_manager
    global player
    global room_manager
    global start_current_player_room
    global turn_manager

    # Example usage
    selected_traits_for_dragon = ["flight", "fire_resistance"]
    dragon1 = create_creature(
        creature_type="dragon",
        creature_data=combatant_data.creature_data,
        creature_traits=combatant_data.creature_traits_data,
        status_data=combatant_data.creature_status_data,
        selected_traits=selected_traits_for_dragon
    )
    player = create_player(
        creature_type="player",
        player_data=combatant_data.player_data,
        creature_traits=combatant_data.creature_traits_data,
        status_data=combatant_data.creature_status_data,
    )
    companion1 = create_companion(
        creature_type="companion",
        companion_data=combatant_data.companion_data,
        creature_traits=combatant_data.creature_traits_data,
        status_data=combatant_data.creature_status_data
    )

    turn_manager = TurnManager(stop_event)
    room_manager = RoomManager()
    movement_manager = MovementManager(room_manager, player)
    turn_manager.room_manager = room_manager

    print(f"---------DEBUG--------MovementManager initialized: {movement_manager is not None}")

    room1 = room.Room()
    room_manager.add_room(room1)
    room2 = room.Room()
    room_manager.add_room(room2)

    room1.connect(room2, "north")
    room2.connect(room1, "south")

    room1.add_combatant(player)
    print(player.current_room)
    # movement_manager.move_entity(player, "north")


    # pprint(dir(room))
    # print("---------------------------------")
    # pprint(vars(room))

    room1.add_combatant(companion1)
    room1.add_combatant(dragon1)

    print(room_manager.room_lookup[f"{dragon1.current_room}"].room_exits)




    room1.spawn_monsters(["dragon", "dragon"])
    room1.detect_hostility(turn_manager)
    dragon1.combatant_manager.add_buff("strength_boost", 5, 10)
    room2.spawn_monsters("dragon")
    # room2.spawn_monsters(["goblin", "wolf", "wolf", "wolf", "wolf", "rabbit"])
    room1.detect_hostility(turn_manager)


    # pprint(dir(player))
    # print("---------------------------------")
    # pprint(vars(player))
    # print(player.stats["health"])

    # SAVE AND LOAD
    # SaveLoadManager.save_to_file("serialization/save_game.json", turn_manager)

    # print(RoomManager)  # Should display <class 'RoomManager'>
    # print(hasattr(RoomManager, "from_dict"))  # Should display True


    # room_manager = None
    # turn_manager = None
    # # # Load the game and optional data
    # turn_manager = SaveLoadManager.load_from_file(
    #     "serialization/save_game.json")

    # print(player.current_room)

    # print((turn_manager))


    # dragon1.combatant_manager.decrement_buff_durations()
    # print(dragon1.describe())
    # print(dragon1.type)

    # selected_traits_for_dragon2 = ["regeneration"]
    # dragon2 = create_creature(
    #     creature_type="dragon",
    #     creature_data=creature_data,
    #     creature_traits=creature_traits_data,
    #     status_data=creature_status_data,
    #     selected_traits=selected_traits_for_dragon2
    # )

    # dragon1.stats["health"] -= 20
    # print(f"Flame Wyvern HP: {dragon1.stats['health']}")
    # print(f"Flame Wyvern HP: {dragon2.stats['health']}")
    # print(dragon1.describe())
    # print(dragon1.hates_all)

    # dragon2.stats["health"] += 20
    # print(f"Flame Wyvern HP: {dragon1.stats['health']}")
    # print(f"Flame Wyvern HP: {dragon2.stats['health']}")
    # dragon2.combatant_manager.add_buff("strength_boost", 5, 5)
    # print(dragon2.describe())

    # print("---------------------")
    # pprint(dir(dragon1))
    # pprint(vars(dragon1.combatant_manager))
    # pprint(help(dragon1))
    # pprint(hasattr(dragon1, 'x'))
    # pprint(getattr(dragon1, 'x', 'Attribute not found'))


    # player.combatant_manager.add_buff("strength_boost", 5, 5)
    # pprint(dir(player))
    # pprint(f"[DEBUG Dragon]{vars(dragon1.combatant_manager)}")
    # pprint(f"[DEBUG Dragon]{vars(dragon2.combatant_manager)}")
    # pprint(vars(player))
    # pprint(vars(companion1))



    # Get information about rooms / a room
    # room_manager.display_map()
    # print(room_manager.get_room_info("room1"))
    # print(room_manager.get_room_info("room2"))
    turn_interval=10
    turn_manager.start_timer(turn_interval)
    print("Turn interval set to:", turn_interval)

    start_current_player_room = room_manager.room_lookup[player.current_room]
    return {"movement_manager": movement_manager, "player": player, "start_current_player_room": start_current_player_room}


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


from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

class CommandCompleter(Completer):
    def __init__(self, commands):
        self.commands = commands  # The commands dictionary

    def get_completions(self, document, complete_event):
        # Only complete the first word (before any whitespace)
        text_before_cursor = document.text_before_cursor

        # Check if there's whitespace, meaning the user is typing beyond the first word
        if " " in text_before_cursor:
            return  # Do nothing if there's already a space
        
        # Suggest commands if the user is typing the first word
        for cmd, details in self.commands.items():
            if cmd.startswith(text_before_cursor):  # Match commands based on current input
                yield Completion(cmd, start_position=-len(text_before_cursor), display=f"{cmd} - {details['description']}")

