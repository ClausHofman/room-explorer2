
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout
import threading

# Shared flag to manage thread lifecycle
running = True

# Command storage
commands = {
    "list_commands": {
        "description": "List all available commands",
        "handler": lambda: print("Available commands:\n" + "\n".join(commands.keys()))
    },
    "quit": {
        "description": "Quit the game",
        "handler": lambda: quit_game()
    },
    # Add more commands as needed
}

def quit_game():
    global running
    print("Quitting the game. Goodbye!")
    running = False  # Signal the input thread to stop

# Input thread with command history
def input_thread():
    # Create a history object for input storage
    history = InMemoryHistory()

    # Use PromptSession with history
    session = PromptSession(history=history)

    with patch_stdout():
        while running:
            try:
                # Use prompt_toolkit to get input, with history enabled
                user_input = session.prompt(">> ").strip()

                # Split input into command and arguments
                parts = user_input.split()
                if not parts:
                    continue
                command = parts[0]
                args = parts[1:]

                # Execute the command if valid
                if command in commands:
                    try:
                        commands[command]["handler"](*args)
                    except TypeError:
                        print(f"Invalid usage for command: {command}")
                else:
                    print(f"Unknown command: {command}")
            except (EOFError, KeyboardInterrupt):
                # Handle Ctrl+D or Ctrl+C gracefully
                quit_game()

# Main game logic
def main_game_loop():
    try:
        # Game initialization or setup can go here
        while running:
            print("Game logic is running...")

            # Simulate world updates or actions
            threading.Event().wait(2)  # Simulate some delay
    except KeyboardInterrupt:
        quit_game()

# Launching the input thread
if __name__ == "__main__":
    # Start the input thread
    input_thread_instance = threading.Thread(target=input_thread, daemon=True)
    input_thread_instance.start()

    # Run the main game loop
    main_game_loop()

    # Join the thread when exiting
    input_thread_instance.join()



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