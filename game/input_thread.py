from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from game.helper_functions import CommandCompleter
from game.managers import RoomManager
import threading, time
from game.shared_resources import stop_event
from game.helper_functions import remove_creature_by_id

DEBUG = False
turn_manager = None
room_manager = None
player = None

# stop_event = threading.Event()
print("input_thread.py stop event:", stop_event)
print(f"input_thread.py stop_event: {id(stop_event)}")


def load_game(player, turn_manager, movement_manager):
    from game.managers import SaveLoadManager
    print("[DEBUG load_game] Starting to load the game.")

    print(f"[DEBUG load_game] Before loading: player.current_room = {player.current_room}")

    loaded_turn_manager = SaveLoadManager.load_from_file(player)
    if loaded_turn_manager:
        print("[DEBUG load_game] Successfully loaded TurnManager from file.")
        
        # Update the global turn_manager with the loaded one
        print("[DEBUG load_game] Updating turn_manager with loaded data.")
        turn_manager.room_manager = loaded_turn_manager.room_manager
        turn_manager.current_turn = loaded_turn_manager.current_turn
        turn_manager.movement_manager = loaded_turn_manager.movement_manager

        # Update the movement_manager
        print("[DEBUG load_game] Updating movement_manager with the loaded TurnManager's room_manager.")
        movement_manager.room_manager = turn_manager.room_manager
        movement_manager.player = player

        # Retrieve the room manager
        room_manager = turn_manager.room_manager
        print(f"[DEBUG load_game] Room manager retrieved. Total game rooms: {len(room_manager.game_rooms)}.")

        # Find the player in the loaded data
        player_data = None
        for room in room_manager.game_rooms:
            print(f"[DEBUG load_game] Checking room: {room.room_id} for player.")
            for combatant in room.combatants:
                if combatant.id == player.id:
                    print(f"[DEBUG load_game] Player with ID {player.id} found in room {room.room_id}.")
                    player_data = combatant
                    print(f"Player data: {player_data}")
                    break
            if player_data:
                break

        if player_data:
            # Get the player's current_room from the loaded data
            player.current_room = player_data.current_room
            
            room_manager.player = player

        else:
            print(f"[ERROR load_game] Player with ID {player.id} not found in loaded data!")

        print("[DEBUG load_game] Game loaded successfully!")
    else:
        print("[ERROR load_game] Failed to load game.")



def input_thread(player, movement_manager, turn_manager):
    from game.managers import SaveLoadManager

    commands = {
        "remove_creature": {
            "description": "Provide a combatant_id to remove a creature",
            "handler": lambda: remove_creature_by_id(turn_manager.room_manager, player)
        },
        "list_commands": {
            "description": "List all available commands",
            "handler": lambda: print("Available commands:\n" + "\n".join(f"{cmd}: {details['description']}\n" for cmd, details in commands.items())),
        },
        "exits": {
            "description": "Show available exits",
            "handler": lambda: movement_manager.exits(),
        },
        "look": {
            "description": "Look around the current room (shortcut: 'l')",
            "handler": lambda: movement_manager.look(),
            "shortcuts": {
                "l": "look"
            }
        },
        "map": {
            "description": "Display a map with nearby paths",
            "handler": lambda: turn_manager.room_manager.generate_map(size=9, search_depth=8)
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
            "handler": lambda: load_game(player, turn_manager, movement_manager),
        },
    }


    command_completer = WordCompleter(
        [f"{cmd} " for cmd in commands.keys()],
        ignore_case=True
    )

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