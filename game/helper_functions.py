import uuid, os
import game.combatant_data as combatant_data
from game.managers import TurnManager, RoomManager, MovementManager, SaveLoadManager, PlayerActionManager
from game.shared_resources import stop_event, game_style
from game.available_skills import available_skills
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import  FormattedText

print("helper_functions.py stop event:", stop_event)
print(f"helper_functions.py stop_event: {id(stop_event)}")
import game.room as room_object

turn_manager = None
player = None
movement_manager = None
room_manager = None
player_action_manager = None
start_current_player_room = None
TURN_INTERVAL = 5


def initialize_game():
    global turn_interval
    global movement_manager
    global player
    global room_manager
    global start_current_player_room
    global turn_manager
    global player_action_manager
    

    # Example usage
    selected_traits_for_dragon = ["flight", "fire_resistance"]
    dragon1 = create_creature(
        creature_type="dragon",
        creature_data=combatant_data.creature_data,
        creature_traits=combatant_data.creature_traits_data,
        status_data=combatant_data.creature_status_data,
        level=5,
        selected_traits=selected_traits_for_dragon
    )
    
    # dragon1.add_skill("fireball", {"damage": 15, "description": "Hurls a ball of fire at the target."}) # Added fireball skill
    # dragon1.add_skill("fire_breath", {"damage": 10, "description": "Breathes fire at the target."}) # Added fire_breath skill

    player = create_player(
        creature_type="player",
        player_data=combatant_data.player_data,
        creature_traits=combatant_data.creature_traits_data,
        status_data=combatant_data.creature_status_data,
    )

    # player.add_skill("slash", {"damage": 10, "description": "A basic melee attack."})  # Added slash skill
    # player.add_skill("double_slash", {"damage": 15, "description": "A more powerful melee attack."})  # Added double_slash skill

    companion1 = create_companion(
        creature_type="companion",
        companion_data=combatant_data.companion_data,
        creature_traits=combatant_data.creature_traits_data,
        status_data=combatant_data.creature_status_data
    )

    # companion1.add_skill("bite", {"damage": 5, "description": "A basic bite attack."})  # Added bite skill
    # companion1.add_skill("double_bite", {"damage": 10, "description": "A more powerful bite attack."})  # Added double_bite skill

    turn_manager = TurnManager(stop_event)
    room_manager = RoomManager(player=player)
    turn_manager.room_manager = room_manager
    movement_manager = MovementManager(room_manager, player)
    movement_manager.turn_manager = turn_manager
    player_action_manager = PlayerActionManager(room_manager=room_manager, player=player)


    

    ### # Example Usage
    # room_manager = RoomManager()  # Assuming RoomManager is defined elsewhere
    # player = Player()  # Assuming Player is defined elsewhere

    # action_manager = ActionManager(room_manager, player)

    # # Now, ActionManager can use MovementManager's methods
    # action_manager.move_player(player, "north")
    ### action_manager.perform_action("Attack")

    
    room1 = room_object.Room()
    room_manager.add_room(room1)

    room2 = room_object.Room()
    room_manager.add_room(room2)

    room3 = room_object.Room()
    room_manager.add_room(room3)

    room1.connect(room2, "north")
    room2.connect(room1, "south")
    room1.connect(room3, "east")
    room3.connect(room1, "west")

    room1.add_combatant(player)
    room1.player_in_room=True
    

    # print(player_action_manager)
    print("---------------- DEBUG ROOM LOOKUP ------------------")
    for id, exits in room_manager.room_lookup.items():
        print(f"Room id: {id}, exits: {exits.room_exits}")

    # print(player.current_room)
    # movement_manager.move_entity(player, "north")

    # print(f"---------DEBUG-------- get_room_info")
    # print(room_manager.get_room_info(room1.room_id))
    # print(room_manager.get_room_info(room2.room_id))

    # pprint(dir(room))
    # print("---------------------------------")
    # pprint(vars(room))

    room1.add_combatant(companion1)
    room1.add_combatant(dragon1)
    print(dragon1.describe())

    print(room_manager.room_lookup[f"{dragon1.current_room}"].room_exits)

    # Test create_and_connect_rooms
    # room_manager.create_and_connect_rooms(room1)


    room1.spawn_monsters(["dragon"])
    room1.detect_hostility(turn_manager)
    dragon1.combatant_manager.add_buff("strength_boost", 5, 10)
    # room2.spawn_monsters("dragon")
    # room2.spawn_monsters(["goblin", "wolf", "wolf", "wolf", "wolf", "rabbit"])


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
    #     "serialization/save_game.json", player)

    # Check if loading was successful
    # if turn_manager is None:
    #     print("[ERROR] Failed to load the game. Exiting.")
    #     return None  # Or handle the error in another way


    # Retrieve room manager from the turn manager
    room_manager = turn_manager.room_manager


    # Retrieve movement manager from the turn manager
    if turn_manager.movement_manager is None:
        print_formatted_text(FormattedText([
            ('class:debug', f"[DEBUG initialize_game] movement_manager is None. Creating a new one.\n")
        ]), style=game_style)
        movement_manager = MovementManager(room_manager, player)
        turn_manager.movement_manager = movement_manager
    else:
        print("[DEBUG initialize_game] movement_manager found in turn_manager.")
        movement_manager = turn_manager.movement_manager
    print(f"[DEBUG initialize_game] Loaded movement_manager: {movement_manager}")
    # Set room manager attribute of the movement manager to the loaded room manager
    movement_manager.room_manager = room_manager
    # Set the player attribute of the movement manager to the loaded player
    movement_manager.player = player
    print(f"[DEBUG initialize_game] movement_manager.room_manager: {movement_manager.room_manager}")
    print(f"[DEBUG initialize_game] movement_manager.player: {movement_manager.player}")

    # Update the player's current room
    # print(f"[DEBUG initialize_game] Before updating player.current_room: {player.current_room}")
    player.current_room = room_manager.room_lookup[player.current_room].room_id
    # print(f"[DEBUG initialize_game] After updating player.current_room: {player.current_room}")


    turn_interval=TURN_INTERVAL
    turn_manager.start_timer(turn_interval)
    print("Turn interval set to:", turn_interval)

    start_current_player_room = room_manager.room_lookup[player.current_room]

    return {"movement_manager": movement_manager,
            "player": player,
            "start_current_player_room": start_current_player_room,
            "turn_manager": turn_manager,
            "player_action_manager": player_action_manager,
            "room_manager": room_manager}



def create_companion(creature_type, companion_data, creature_traits, status_data, selected_traits=None):
    from game.combatants import Companion
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
    base_stats = {
        "health": companion_info["health"],
        "attack": companion_info["attack"],
        "defense": companion_info["defense"],
        "strength": companion_info["strength"],
        "intelligence": companion_info["intelligence"]
    }
    
    # Generate a unique combatant ID
    combatant_id = f"{creature_type}_{uuid.uuid4().hex[:6]}"
    
    # Return a Companion object
    companion = Companion(
        combatant_id=combatant_id,
        name=companion_info["name"],
        base_stats=base_stats,
        level=companion_info.get("level", 1),
        hates_all=companion_info.get("hates_all", False),
        hates_player_and_companions=companion_info.get("hates_player_and_companions", False),
        hates=companion_info.get("hates", []),
        monster_type=companion_info.get("monster_type", None),
        has_traits=companion_info["has_traits"],
        all_creature_traits_data=creature_traits,
        status_data=status_data,
        selected_traits=selected_traits
    )
    # companion.add_skill("offensive_melee", "bite", available_skills["offensive_melee"]["bite"])
    # companion.add_skill("offensive_melee", "double_bite", available_skills["offensive_melee"]["double_bite"])
    companion.add_skill("offensive_melee", "poison_bite", available_skills["offensive_melee"]["poison_bite"])
    return companion
    
def create_player(creature_type, player_data, creature_traits, status_data, selected_traits=None):
    from game.combatants import Player
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
    base_stats = {
        "health": player_info["health"],
        "attack": player_info["attack"],
        "defense": player_info["defense"],
        "strength": player_info["strength"],
        "intelligence": player_info["intelligence"]
    }

    
    # Generate a unique combatant ID
    combatant_id = f"{creature_type}_{uuid.uuid4().hex[:6]}"
    
    # Return a Player object
    player = Player(
        combatant_id=combatant_id,
        name=player_info["name"],
        base_stats=base_stats,
        level=player_info.get("level", 1),
        hates_all=player_info.get("hates_all", False),
        hates_player_and_companions=player_info.get("hates_player_and_companions", False),
        hates=player_info.get("hates", []),
        monster_type=player_info.get("monster_type", None),
        has_traits=player_info["has_traits"],
        all_creature_traits_data=creature_traits,
        status_data=status_data,
        selected_traits=selected_traits
    )
    player.add_skill("offensive_melee", "slash", available_skills["offensive_melee"]["slash"])
    player.add_skill("offensive_melee", "double_slash", available_skills["offensive_melee"]["double_slash"])
    return player

def create_creature(creature_type, creature_data, creature_traits, status_data, level, selected_traits=None):
    from game.combatants import Monster

    if creature_type not in creature_data:
        raise ValueError(f"Creature type '{creature_type}' does not exist in creature_data.")
    
    creature_info = creature_data[creature_type]
    
    # Use base stats from creature_info
    base_stats = {
        "health": creature_info["health"],
        "attack": creature_info["attack"],
        "defense": creature_info["defense"],
        "strength": creature_info["strength"],
        "intelligence": creature_info["intelligence"],
        "health_per_level": creature_info.get("health_per_level", 0),
        "attack_per_level": creature_info.get("attack_per_level", 0),
        "defense_per_level": creature_info.get("defense_per_level", 0)
    }
    
    combatant_id = f"{creature_type}_{uuid.uuid4().hex[:6]}"
    

    monster = Monster(
        combatant_id=combatant_id,
        name=creature_info["name"],
        base_stats=base_stats,
        level=level,
        hates_all=creature_info.get("hates_all", False),
        hates_player_and_companions=creature_info.get("hates_player_and_companions", False),
        hates=creature_info.get("hates", []),
        monster_type=creature_info.get("monster_type", None),
        has_traits=creature_info["has_traits"],
        all_creature_traits_data=creature_traits,
        status_data=status_data,
        selected_traits=selected_traits
    )

    if creature_type == "dragon":
        monster.add_skill("offensive_melee", "fireball", available_skills["offensive_melee"]["fireball"])
        monster.add_skill("offensive_melee", "fire_breath", available_skills["offensive_melee"]["fire_breath"])
        monster.add_passive_skill("passive_defense", "iron_skin", available_skills["passive_defense"]["iron_skin"])

    return monster  # Level is now stored in the monster itself


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


    # Create a WordCompleter with command descriptions
    # command_completer = WordCompleter(
    #     [f"{cmd} - {details['description']}" for cmd, details in commands.items()],
    #     ignore_case=True
    # )


def remove_creature_by_id(room_manager, player):
    current_room = room_manager.room_lookup[player.current_room]
    for combatant in current_room.combatants:
                if combatant.id != player.id:
                    print(combatant.id)
    while True:
            try:
                creature_id = str(input("Type id of creature to remove (Enter to abort):\n"))
                if creature_id == "":
                    print("Aborting.")
                    return
                for combatant in current_room.combatants:
                    if combatant.id == creature_id and combatant.id != player.id:
                        creature_to_remove = combatant
                    else:
                        print("Unable to remove yourself or invalid combatant_id")
                        continue
                current_room.combatants.remove(creature_to_remove)
                print(f"{combatant.name} blinks out from existence.")
                break
            except ValueError:
                ("Enter a valid combatant_id string or press Enter to abort.")


def remove_creature_by_id(room_manager, player):
    """
    Removes a creature from the player's current room by ID, except the player themselves.

    Args:
        room_manager: The RoomManager instance containing room and combatant data.
        player: The player object (the one performing the removal).
    """
    current_room = room_manager.room_lookup[player.current_room]

    # List all combatants in the current room (excluding the player)
    has_other_creatures = False
    for combatant in current_room.combatants:
        if combatant.id != player.id:
            print(f"- {combatant.id}: {combatant.name}")
            has_other_creatures = True

    if not has_other_creatures:
        print("No other creatures to remove in this room.")
        return

    while True:
        creature_id = str(input("Type the ID of the creature to remove (or press Enter to abort):\n")).strip().lower()
        if creature_id == "":
            print("Aborting.")
            return

        # Search for the combatant by ID in the current room
        creature_to_remove = next(
            (combatant for combatant in current_room.combatants if combatant.id == creature_id), 
            None
        )

        # Check if the combatant exists and is not the player
        if creature_to_remove is None:
            print("Invalid combatant ID. Please try again.")
        elif creature_to_remove.id == player.id:
            print("Unable to remove yourself or invalid combatant_id.")
        else:
            # Remove the combatant and update the room
            current_room.combatants.remove(creature_to_remove)
            print(f"{creature_to_remove.name} snaps out from existence.")
            break



def generate_internal_connections(width, length):
    """
    Generates the internal_connections list for a grid of the given width and length.

    Args:
        width: The width of the grid (number of columns).
        length: The length of the grid (number of rows).

    Returns:
        A list of tuples representing the internal connections.
    """

    internal_connections = []
    room_count = 0

    # Helper function to get the room number from row and column
    def get_room_number(row, col):
        return row * width + col + 1

    # Iterate through each room in the grid
    for row in range(length):
        for col in range(width):
            room_num1 = get_room_number(row, col)

            # Check for adjacent rooms in all directions
            # North
            if row > 0:
                room_num2 = get_room_number(row - 1, col)
                internal_connections.append((room_num1, room_num2, "north"))
                internal_connections.append((room_num2, room_num1, "south"))

            # South
            if row < length - 1:
                room_num2 = get_room_number(row + 1, col)
                internal_connections.append((room_num1, room_num2, "south"))
                internal_connections.append((room_num2, room_num1, "north"))

            # East
            if col < width - 1:
                room_num2 = get_room_number(row, col + 1)
                internal_connections.append((room_num1, room_num2, "east"))
                internal_connections.append((room_num2, room_num1, "west"))

            # West
            if col > 0:
                room_num2 = get_room_number(row, col - 1)
                internal_connections.append((room_num1, room_num2, "west"))
                internal_connections.append((room_num2, room_num1, "east"))

            # Northeast
            if row > 0 and col < width - 1:
                room_num2 = get_room_number(row - 1, col + 1)
                internal_connections.append((room_num1, room_num2, "northeast"))
                internal_connections.append((room_num2, room_num1, "southwest"))

            # Northwest
            if row > 0 and col > 0:
                room_num2 = get_room_number(row - 1, col - 1)
                internal_connections.append((room_num1, room_num2, "northwest"))
                internal_connections.append((room_num2, room_num1, "southeast"))

            # Southeast
            if row < length - 1 and col < width - 1:
                room_num2 = get_room_number(row + 1, col + 1)
                internal_connections.append((room_num1, room_num2, "southeast"))
                internal_connections.append((room_num2, room_num1, "northwest"))

            # Southwest
            if row < length - 1 and col > 0:
                room_num2 = get_room_number(row + 1, col - 1)
                internal_connections.append((room_num1, room_num2, "southwest"))
                internal_connections.append((room_num2, room_num1, "northeast"))
    print(f"[DEBUG generate_internal_connections] Generated internal connections: {internal_connections}")
    return internal_connections

def create_room_cluster(room_manager, start_room, direction, width, length, internal_connections):
    """
    Creates a grid of rooms starting from a specified direction relative to a central room.
    Connects the rooms internally and with adjacent rooms if they exist.
    
    Parameters:
        room_manager: Manages and tracks all rooms in the game.
        start_room: The central room to start the cluster from.
        direction: Direction to build the cluster (north, south, east, or west).
        width: The width of the grid (number of columns).
        length: The length of the grid (number of rows).
        internal_connections: The list of tuples defining the internal connections.
    
    Returns:
        A dictionary of rooms in the grid, keyed by their grid positions (1 to width*length).
    """
    from game.room import Room

    # Ensure the direction is valid
    valid_directions = ["north", "south", "east", "west"]
    if direction not in valid_directions:
        raise ValueError(f"Invalid direction: {direction}. Must be one of {valid_directions}")

    # Initialize placeholders for adjacent rooms
    north_room, south_room, east_room, west_room = None, None, None, None

    # Identify and assign adjacent rooms if they exist
    for room in room_manager.room_lookup.values():
        if start_room.room_id in room.room_exits.values():
            for exit_dir, connected_room_id in room.room_exits.items():
                if connected_room_id == start_room.room_id:
                    if exit_dir == "north":
                        south_room = room
                    elif exit_dir == "south":
                        north_room = room
                    elif exit_dir == "east":
                        west_room = room
                    elif exit_dir == "west":
                        east_room = room

    # Create a dictionary to store the new rooms
    rooms = {}

    # Create all rooms
    for room_number in range(1, width * length + 1):
        new_room = Room()
        room_manager.add_room(new_room)
        rooms[room_number] = new_room
        print(f"[DEBUG CLUSTER] Created room: {room_number}")

    # Connect the first three rooms to the start room and adjacent rooms
    if direction == "north":
        start_room.connect(rooms[length*width-width+2], "north") # 3x3: 8, 4x4: 14
        start_room.connect(rooms[length*width-width+3], "northeast") # 3x3: 9, 4x4: 15
        start_room.connect(rooms[length*width-width+1], "northwest") # 3x3: 7, 4x4: 13
        print(f"[DEBUG CLUSTER] Connected start_room to {length*width-width+2} (north), {length*width-width+3} (northeast), {length*width-width+1} (northwest)")
        if east_room:
            east_room.connect(rooms[length*width-width+3], "north") # 3x3: 9, 4x4: 15
            east_room.connect(rooms[length*width-width+2], "northwest") # 3x3: 8, 4x4: 14
            print(f"[DEBUG CLUSTER] Connected east_room to {length*width-width+3} (north), {length*width-width+2} (northwest)")
        if west_room:
            west_room.connect(rooms[length*width-width+1], "north") # 3x3: 7, 4x4: 13
            west_room.connect(rooms[length*width-width+2], "northeast") # 3x3: 8, 4x4: 14
            print(f"[DEBUG CLUSTER] Connected west_room to {length*width-width+1} (north), {length*width-width+2} (northeast)")
    elif direction == "south":
        start_room.connect(rooms[2], "south") # 3x3: 2, 4x4: 2
        start_room.connect(rooms[3], "southeast") # 3x3: 3, 4x4: 3
        start_room.connect(rooms[1], "southwest") # 3x3: 1, 4x4: 1
        print(f"[DEBUG CLUSTER] Connected start_room to 2 (south), 3 (southeast), 1 (southwest)")
        if east_room:
            east_room.connect(rooms[2], "southwest") # 3x3: 2, 4x4: 2
            east_room.connect(rooms[3], "south") # 3x3: 3, 4x4: 3
            print(f"[DEBUG CLUSTER] Connected east_room to 2 (southwest), 3 (south)")
        if west_room:
            west_room.connect(rooms[2], "southeast") # 3x3: 2, 4x4: 2
            west_room.connect(rooms[1], "south") # 3x3: 1, 4x4: 1
            print(f"[DEBUG CLUSTER] Connected west_room to 2 (southeast), 1 (south)")
    elif direction == "east":
        start_room.connect(rooms[1], "northeast") # 3x3: 1, 4x4: 1
        start_room.connect(rooms[1+width], "east") # 3x3: 4, 4x4: 5
        start_room.connect(rooms[1+width*(length-1)], "southeast") # 3x3: 7, 4x4: 9
        print(f"[DEBUG CLUSTER] Connected start_room to 1 (northeast), {1+width} (east), {1+width*(length-1)} (southeast)")
        if north_room:
            north_room.connect(rooms[1], "east") # 3x3: 1, 4x4: 1
            north_room.connect(rooms[1+width], "southeast") # 3x3: 4, 4x4: 5
            print(f"[DEBUG CLUSTER] Connected north_room to 1 (east), {1+width} (southeast)")
        if south_room:
            south_room.connect(rooms[1+width*(length-1)], "east") # 3x3: 7, 4x4: 9
            south_room.connect(rooms[1+width], "northeast") # 3x3: 4, 4x4: 5
            print(f"[DEBUG CLUSTER] Connected south_room to {1+width*(length-1)} (east), {1+width} (northeast)")
    elif direction == "west":
        start_room.connect(rooms[width], "northwest") # 3x3: 3, 4x4: 4
        start_room.connect(rooms[width*2], "west") # 3x3: 6, 4x4: 8
        start_room.connect(rooms[width*length], "southwest") # 3x3: 9, 4x4: 12
        print(f"[DEBUG CLUSTER] Connected start_room to {width} (northwest), {width*2} (west), {width*length} (southwest)")
        if north_room:
            north_room.connect(rooms[width], "west") # 3x3: 3, 4x4: 4
            north_room.connect(rooms[width*2], "southwest") # 3x3: 6, 4x4: 8
            print(f"[DEBUG CLUSTER] Connected north_room to {width} (west), {width*2} (southwest)")
        if south_room:
            south_room.connect(rooms[width*length], "west") # 3x3: 9, 4x4: 12
            south_room.connect(rooms[width*2], "northwest") # 3x3: 6, 4x4: 8
            print(f"[DEBUG CLUSTER] Connected south_room to {width*length} (west), {width*2} (northwest)")

    # Connect the rooms internally
    for room_num1, room_num2, conn_direction in internal_connections: # tuple numbers are the rooms in rooms dictionary
        if room_num1 in rooms and room_num2 in rooms: # rooms dictionary, keys are numbers
            rooms[room_num1].connect(rooms[room_num2], conn_direction)
            print(f"[DEBUG CLUSTER] Connecting room {room_num1} to {room_num2} in direction {conn_direction}")
            print(f"[DEBUG CLUSTER] Room {room_num1} connections: {rooms[room_num1].room_exits}")
            print(f"[DEBUG CLUSTER] Room {room_num2} connections: {rooms[room_num2].room_exits}")

    return rooms


def create_cluster_command(room_manager, player):
    """Handles the 'create_cluster' command."""
    valid_directions = ["north", "south", "east", "west"]  # Only cardinal directions
    while True:
        direction = input(f"Enter the direction to expand the cluster ({', '.join(valid_directions)} or press Enter to abort):\n").strip().lower()
        if direction == "":
            abort_message = "Aborting cluster creation."
            print(abort_message)
            return abort_message  # Return the abort message for logging purposes
        if direction not in valid_directions:
            print(f"Invalid direction '{direction}'. Please choose from: {', '.join(valid_directions)}.")
            continue
        while True:
            try:
                width = int(input("Enter the width of the cluster (horizontal axis):\n"))
                length = int(input("Enter the length of the cluster (vertical axis):\n"))

                if width < 1 or length < 1:
                    print("Width and length must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter integers for width and length.")

        start_room = room_manager.room_lookup[player.current_room]
        internal_connections = generate_internal_connections(width, length)
        create_room_cluster(room_manager, start_room, direction, width, length, internal_connections)
        success_message = f"{width}x{length} room cluster created to the {direction} of room '{start_room.room_id}'."
        print(success_message)
        return success_message  # Return the success message for logging purposes


def create_cluster_command_wrapper():
    """Wrapper for create_cluster_command to handle user input."""
    valid_directions = ["north", "south", "east", "west"]
    while True:
        direction = input(f"Enter the direction to expand the cluster ({', '.join(valid_directions)} or press Enter to abort):\n").strip().lower()
        if direction == "":
            print("Aborting cluster creation.")
            return
        if direction not in valid_directions:
            print(f"Invalid direction '{direction}'. Please choose from: {', '.join(valid_directions)}.")
            continue
        while True:
            try:
                width = int(input("Enter the width of the cluster:\n"))
                length = int(input("Enter the length of the cluster:\n"))
                if width < 1 or length < 1:
                    print("Width and length must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter integers for width and length.")

        start_room = turn_manager.room_manager.room_lookup[player.current_room]
        internal_connections = generate_internal_connections(width, length)
        create_room_cluster(turn_manager.room_manager, start_room, direction, width, length, internal_connections)
        print(f"{width}x{length} room cluster created to the {direction} of room '{start_room.room_id}'.")
        return


def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac and Linux
    else:
        os.system('clear')


# In game/helper_functions.py

def use_skill_command(player, room_manager):
    """Allows the player to select and use a skill."""
    current_room = room_manager.room_lookup[player.current_room]
    target = current_room.select_target(player)

    if not target:
        print("No valid target to use skills on.")
        return

    available_skills = [skill_name for skill_category in player.skills for skill_name in player.skills[skill_category]]

    if not available_skills:
        print("You have no available skills to use.")
        return

    print("Available skills:")
    for i, skill_name in enumerate(available_skills):
        print(f"{i + 1}. {skill_name}")

    while True:
        try:
            choice = int(input("Choose a skill to use (or 0 to cancel): "))
            if choice == 0:
                print("Skill usage cancelled.")
                return
            if 1 <= choice <= len(available_skills):
                selected_skill = available_skills[choice - 1]
                if player.can_use_skill(selected_skill):
                    player.use_skill(selected_skill, target)
                    return
                else:
                    print(f"You can't use {selected_skill} right now.")
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")
