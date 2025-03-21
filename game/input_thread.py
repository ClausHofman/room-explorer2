from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from game.helper_functions import CommandCompleter
import threading
from game.shared_resources import stop_event

DEBUG = True

# stop_event = threading.Event()
print("input_thread.py stop event:", stop_event)
print(f"input_thread.py stop_event: {id(stop_event)}")

def input_thread(player, movement_manager, turn_manager):
    from game.managers import SaveLoadManager
    commands = {
        "list_commands": {
            "description": "List all available commands",
            "handler": lambda: print("Available commands:\n" + "\n".join(f"{cmd}: {details['description']}\n" for cmd, details in commands.items())),
        },
        "quit": {
            "description": "Quit the game",
            "handler": lambda: quit_game(),
        },
            "save": {
            "description": "Save the current game state",
            "handler": lambda: SaveLoadManager.save_to_file("serialization/save_game.json", turn_manager), # ADDED SAVE COMMAND
        },
        "move": {
            "description": "Move in a specified direction (e.g., 'move north')",
            "handler": lambda direction: movement_manager.move_entity_command(direction, player),
            "movement_command": True,
        },
    }

    # Create a WordCompleter with command descriptions
    # command_completer = WordCompleter(
    #     [f"{cmd} - {details['description']}" for cmd, details in commands.items()],
    #     ignore_case=True
    # )

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

            # with threading.Lock():
                if command in commands:
                    try:
                        if commands[command].get("movement_command"):
                            turn_manager.movement_manager.player.current_room = player.current_room
                        commands[command]["handler"](*args)
                        if command == "move":

                            if DEBUG:
                                                        # Add print statements here
                                print(f"Player's current room: {player.current_room}")
                                print(f"Player is in room: {movement_manager.room_manager.room_lookup[player.current_room].room_name}")
                                print(f"Room exits: {movement_manager.room_manager.room_lookup[player.current_room].room_exits}")
                                print(f"Room ID: {movement_manager.room_manager.room_lookup[player.current_room].room_id}")
                                print(f"Room Name: {movement_manager.room_manager.room_lookup[player.current_room].room_name}")
                                print(f"Room Connections: {movement_manager.room_manager.room_lookup[player.current_room].room_exits}")
                                print(f"Room Manager Room Lookup: {movement_manager.room_manager.room_lookup}")
                                print(f"Turn Manager: {turn_manager}")
                                print(f"Turn Manager Current Turn: {turn_manager.current_turn}")
                                print(f"Turn Manager Room Manager: {turn_manager.room_manager}")
                                print(f"Turn Manager Movement Manager: {turn_manager.movement_manager}")
                                print(f"Turn Manager Stop Event: {turn_manager.stop_event}")
                                print(f"Turn Manager Running: {turn_manager.running}")


                    except TypeError:
                        print(f"Invalid usage for command: {command}")
                else:
                    print(f"Unknown command: {command}")
            except (EOFError, KeyboardInterrupt):
                print("Input thread interrupted. Quitting...")
                quit_game()
            except Exception as e:
                print(f"Unexpected error: {e}")

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