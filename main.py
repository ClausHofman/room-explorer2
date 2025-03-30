import sys
from game.helper_functions import initialize_game
from game.input_thread import input_thread
from game.shared_resources import game_colors
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import ANSI
import threading, time

def main():
    from game.input_thread import stop_event

    start_game = initialize_game()

    # print("Test game initialization:", start_game)
    # print("movement_manager type:", type(start_game["movement_manager"]))
    # print("movement_manager object:", start_game["movement_manager"])

    # Check that argument order is correct!
    user_input_thread = threading.Thread(target=input_thread, args=(
        start_game["player"],
        start_game["movement_manager"],
        start_game["turn_manager"],
        start_game["player_action_manager"]
        ), daemon=True)
    
    user_input_thread.start()

    turn_manager = start_game["turn_manager"]
    room_manager = start_game["room_manager"]
    room_manager = turn_manager.room_manager

    room_manager.generate_map(size=7, search_depth=40)
    
    print_formatted_text(ANSI(f"{game_colors['LIST_COMMANDS']} Type 'list_commands' for available commands. {game_colors['COLOR_RESET']}"))

    if not user_input_thread.is_alive():
        print("Input thread has unexpectedly stopped.")

    # print(f"[DEBUG] stop_event in main(): {id(stop_event)}")

    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Stopping the program...")
        stop_event.set()
    finally:
        print("All threads have stopped. Exiting program.")
        sys.exit()

if __name__ == "__main__":
    main()
