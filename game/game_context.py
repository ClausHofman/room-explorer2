class GameContext:
    def __init__(self):
        self.start_game = None

    def initialize(self):
        from helper_functions import initialize_game
        self.start_game = initialize_game()

# Create a global instance of GameContext
game_context = GameContext()

# Can be used in main.py for example
# game_context.initialize()
# print("GAME CONTEXT:", game_context.start_game["movement_manager"])

# Examples

### main.py

# from game_context import game_context

# # Initialize the game state
# game_context.initialize()

# # Pass context or objects to the input thread
# from input_commands import input_thread
# import threading

# user_input_thread = threading.Thread(target=input_thread, args=(game_context.start_game,))
# user_input_thread.start()

### input_commands.py

# from game_context import game_context

# def input_thread(start_game):
#     movement_manager = start_game["movement_manager"]
#     player = start_game["player"]

#     # Use the game context
#     print("Movement Manager:", game_context.start_game["movement_manager"])
#     print("Player:", game_context.start_game["player"])
