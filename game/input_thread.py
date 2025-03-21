from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from helper_functions import CommandCompleter
import threading
from shared_resources import stop_event

DEBUG = True

# stop_event = threading.Event()
print("input_thread.py stop event:", stop_event)
print(f"input_thread.py stop_event: {id(stop_event)}")

def input_thread(player, movement_manager):
    commands = {
        "list_commands": {
            "description": "List all available commands",
            "handler": lambda: print("Available commands:\n" + "\n".join(f"{cmd}: {details['description']}\n" for cmd, details in commands.items())),
        },
        "quit": {
            "description": "Quit the game",
            "handler": lambda: quit_game(),
        },
        "move": {
            "description": "Move in a specified direction (e.g., 'move north')",
            "handler": lambda direction: movement_manager.move_entity_command(direction, player),
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

                with threading.Lock():
                    if command in commands:
                        try:
                            commands[command]["handler"](*args)
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