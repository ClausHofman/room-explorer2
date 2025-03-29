import sys
from prompt_toolkit import PromptSession, print_formatted_text, ANSI
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from game.helper_functions import CommandCompleter
from game.managers import RoomManager
from game.shared_resources import stop_event, game_style
from game.helper_functions import remove_creature_by_id, create_cluster_command_wrapper, clear_screen, use_skill_command
import threading

DEBUG = False
turn_manager = None
room_manager = None
player = None

# stop_event = threading.Event()
print("input_thread.py stop event:", stop_event)
print(f"input_thread.py stop_event: {id(stop_event)}")


def load_game(player, turn_manager, movement_manager, player_action_manager):
    from game.managers import SaveLoadManager
    print("[DEBUG load_game] Starting to load the game.")

    print(f"[DEBUG load_game] Before loading: player.current_room = {player.current_room}")

    # Attempt to load the game state from a file using SaveLoadManager
    loaded_turn_manager = SaveLoadManager.load_from_file(player)
    
    # Check if the loading was successful
    if loaded_turn_manager:
        print("[DEBUG load_game] Successfully loaded TurnManager from file.")
        
        # --- Update the global turn_manager with the loaded data ---
        print("[DEBUG load_game] Updating turn_manager with loaded data.")
        # Replace the current room_manager with the loaded one
        turn_manager.room_manager = loaded_turn_manager.room_manager
        # Restore the active_room_lookup from the loaded data
        turn_manager.room_manager.active_room_lookup = loaded_turn_manager.room_manager.active_room_lookup
        # Restore the current turn from the loaded data
        turn_manager.current_turn = loaded_turn_manager.current_turn
        # Restore the movement_manager from the loaded data
        turn_manager.movement_manager = loaded_turn_manager.movement_manager

        # --- Update the movement_manager with the loaded data ---
        print("[DEBUG load_game] Updating movement_manager with the loaded TurnManager's room_manager.")
        # Set the movement_manager's room_manager to the loaded room_manager
        movement_manager.room_manager = turn_manager.room_manager
        # Set the movement_manager's player to the current player
        movement_manager.player = player

        # --- Retrieve the room manager ---
        # Get a reference to the room_manager from the turn_manager
        room_manager = turn_manager.room_manager
        # Update the room_manager attribute of all rooms
        for room in room_manager.game_rooms:
            # Set the room_manager attribute of each room to the current room_manager
            room.room_manager = room_manager
        # Update the room_manager attribute of all active rooms
        for room in room_manager.active_room_lookup.values():
            # Set the room_manager attribute of each active room to the current room_manager
            room.room_manager = room_manager
        print(f"[DEBUG load_game] Room manager retrieved. Total game rooms: {len(room_manager.game_rooms)}.")

        # --- Find the player in the loaded data ---
        player_data = None
        # Iterate through all rooms in the loaded room_manager
        for room in room_manager.game_rooms:
            print(f"[DEBUG load_game] Checking room: {room.room_id} for player.")
            # Iterate through all combatants in the current room
            for combatant in room.combatants:
                # Check if the current combatant is the player
                if combatant.id == player.id:
                    print(f"[DEBUG load_game] Player with ID {player.id} found in room {room.room_id}.")
                    # Store a reference to the player's data
                    player_data = combatant
                    print(f"Player data: {player_data}")
                    break
            # If the player was found, exit the outer loop
            if player_data:
                break

        # --- Update the player's data with the loaded data ---
        if player_data:
            # Get the player's current_room from the loaded data
            player.current_room = player_data.current_room
            
            # Set the room_manager's player to the current player
            room_manager.player = player
        
            # --- Update the player_action_manager with the loaded data ---
            print("[DEBUG load_game] Updating player_action_manager with loaded data.")
            # Set the player_action_manager's room_manager to the loaded room_manager
            player_action_manager.room_manager = room_manager
            # Set the player_action_manager's player to the current player
            player_action_manager.player = player

            # Update player skills and stats from loaded data
            player.skills = player_data.skills
            player.stats = player_data.stats

        else:
            print(f"[ERROR load_game] Player with ID {player.id} not found in loaded data!")

        print("[DEBUG load_game] Game loaded successfully!")
    else:
        print("[ERROR load_game] Failed to load game.")



def input_thread(player, movement_manager, turn_manager, player_action_manager):
    from game.managers import SaveLoadManager
    
    def test_colors_handler():
        """Prints various colored text to test the output."""
        print_formatted_text(FormattedText([
            ('class:player', "This is player text.\n"),
            ('class:list-commands', "This is list-commands text.\n"),
            ('class:warning', "This is warning text.\n"),
            ('class:success', "This is success text.\n"),
            ('class:info', "This is info text.\n"),
            ('class:error', "This is error text.\n"),
            ('class:debug', "This is debug text.\n"),
        ]), style=game_style)


    commands = {
        "use_skill": {
            "description": "Use a skill",
            "handler": lambda: use_skill_command(player, turn_manager.room_manager),
        },
        "create_cluster": {
            "description": "Create a room cluster in a specified direction.",
            "handler": create_cluster_command_wrapper,  # Use the wrapper here
        },
        "create_test_rooms": {
            "description": "Create a large number of rooms for testing.",
            "handler": lambda: turn_manager.room_manager.create_and_connect_rooms(
                turn_manager.room_manager.room_lookup[player.current_room],
                test_mode=True,
                num_rooms_to_create=2000
            ),
        },
        "remove_creature": {
            "description": "Provide a combatant_id to remove a creature",
            "handler": lambda: remove_creature_by_id(turn_manager.room_manager, player)
        },
        "list_commands": {
            "description": "List all available commands",
            "handler": lambda: print("Available commands:\n" + "\n".join(f"{cmd}: {details['description']}\n" for cmd, details in commands.items())),
        },
        "test_colors": {
            "description": "Test the color output",
            "handler": lambda: test_colors_handler(),  # Call the handler function
        },
        "exits": {
            "description": "Show available exits",
            "handler": lambda: movement_manager.exits(),
        },
        "look": {
            "description": "Look around the current room (shortcut: 'l')",
            "handler": lambda: player_action_manager.look(),
            "shortcuts": {
                "l": "look"
            }
        },
        "map": {
            "description": "Display a map with nearby paths",
            "handler": lambda: turn_manager.room_manager.generate_map(size=13,search_depth=40)
        },
        "move": {
            "description": "Move in a specified direction (e.g., 'move north' or use shortcuts 'n', 's', 'e', 'w', 'ne', 'se', 'nw', 'sw', 'd', 'u')",
            "handler": lambda direction: movement_manager.move_player_command(direction, player),
            "movement_command": True,
            "shortcuts": {
                "n": "north",
                "e": "east",
                "s": "south",
                "w": "west",
                "ne": "northeast",
                "se": "southeast",
                "nw": "northwest",
                "sw": "southwest",
                "d": "down",
                "u": "up",
            }
        },
        "create_rooms": {
            "description": "Create and connect rooms to available directions",
            "handler": lambda: turn_manager.room_manager.create_and_connect_rooms(turn_manager.room_manager.room_lookup[player.current_room]),
        },
        "room_info": {
            "description": "Display information about the current room",
            "handler": lambda: turn_manager.room_manager.get_room_info()
        },
        "clear": {
            "description": "Clear the screen",
            "handler": lambda: clear_screen(),
        },          
        "quit": {
            "description": "Quit the game",
            "handler": lambda: quit_game(),
        },
            "save": {
            "description": "Save the current game state",
            "handler": lambda: SaveLoadManager.save_to_file(turn_manager),
        },
            "load": {
            "description": "Load a saved game state",
            "handler": lambda: load_game(player, turn_manager, movement_manager, player_action_manager),
        },
    }


    command_completer = WordCompleter([f"{cmd} " for cmd in commands.keys()], ignore_case=True)
    history = InMemoryHistory()
    command_completer = CommandCompleter(commands)
    
    session = PromptSession(history=history, completer=command_completer)

    with patch_stdout():
        while not stop_event.is_set():
            try:
                user_input = session.prompt(">> ").strip()

                parts = user_input.split()
                if not parts:
                    continue
                command = parts[0]
                args = parts[1:]


                # **Check for shortcuts first**
                shortcut_used = False
                for cmd_name, cmd_details in commands.items():
                    if "shortcuts" in cmd_details and command in cmd_details["shortcuts"] and not cmd_details.get("movement_command", False):
                        # Execute the command associated with the shortcut
                        commands[cmd_name]["handler"](*args)
                        shortcut_used = True
                        break  # Exit the loop after finding a shortcut

                if shortcut_used:
                    continue  # Skip normal command processing

                # **Check if the command is a movement command**
                if command == "move" or command in commands["move"].get("shortcuts", {}):
                    if command in commands["move"]["shortcuts"]:  
                        # Convert shortcut to full movement direction
                        direction = commands["move"]["shortcuts"][command]
                    elif args:  
                        # Use normal move command with its argument
                        direction = args[0]
                    else:
                        print("Usage: move <direction> (e.g., 'move north')")
                        continue

                    # Call move command with the resolved direction
                    commands["move"]["handler"](direction)
                    continue  # Skip normal command processing since movement is handled

                # **Handle other non-movement commands normally**
                if command in commands:
                    commands[command]["handler"](*args)
                else:
                    print(f"Unknown command: {command}")

            except ValueError:
                print("Invalid input. Please try again.")

                if DEBUG:
                    print(f"Player's current room: {player.current_room}")
                    print(f"Player is in room: {movement_manager.room_manager.room_lookup[player.current_room].room_name}")
                    print(f"Room exits: {movement_manager.room_manager.room_lookup[player.current_room].room_exits}")
                    print(f"Room ID: {movement_manager.room_manager.room_lookup[player.current_room].room_id}")
                    print(f"Room Name: {movement_manager.room_manager.room_lookup[player.current_room].room_name}")
                    print(f"Room Connections: {movement_manager.room_manager.room_lookup[player.current_room].room_exits}")
                    print(f"Room Manager Room Lookup: {movement_manager.room_manager.room_lookup}")
                    # print(f"Turn Manager: {turn_manager}")
                    # print(f"Turn Manager Current Turn: {turn_manager.current_turn}")
                    # print(f"Turn Manager Room Manager: {turn_manager.room_manager}")
                    # print(f"Turn Manager Movement Manager: {turn_manager.movement_manager}")
                    # print(f"Turn Manager Stop Event: {turn_manager.stop_event}")
                    # print(f"Turn Manager Running: {turn_manager.running}")

                else:
                    print(f"Unknown command: {command}")
            except (EOFError, KeyboardInterrupt):
                print("Input thread interrupted. Quitting...")
                quit_game()
            except Exception as e:
                print(f"Unexpected error: {e}")
                quit_game()


def quit_game():
    # print("Active threads:", threading.enumerate())
    print("Quitting the game. Setting stop_event...")
    stop_event.set()
    print("Active threads:", threading.enumerate())
    print("stop_event has been set.")

# Color testing
# from colorama import Fore, Style, init

# def found_secret_room():
#     print(Fore.MAGENTA + Style.BRIGHT + "You have discovered a secret room!" + Style.RESET_ALL)

# def picked_up_item(item_name):
#     print(Fore.YELLOW + f"You picked up: {item_name}" + Style.RESET_ALL)

# def critical_warning(message):
#     print(Fore.RED + Style.BRIGHT + "WARNING: " + message + Style.RESET_ALL)

# # Initialize colorama
#     init()
#     found_secret_room()
#     picked_up_item("A peculiar item")
#     critical_warning("WARNING")

###

# Example of defining a style (not necessary for simple colors):
# from prompt_toolkit.styles import Style
# my_style = Style.from_dict({
#     'green-text': '#00aa00',  # Green
#     'red-text': '#ff0000 bold',  # Red and bold
# })
# print_formatted_text(HTML('<green-text>This is green text.</green-text>'), style=my_style)
