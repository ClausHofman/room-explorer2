from prompt_toolkit.styles import Style
import threading

# Initialize stop_event
stop_event = threading.Event()


room_type_data = {
    "forest": "You are in a dense forest. Sunlight filters through the leaves above.",
    "cave": "You are in a dark, damp cave. Water drips from the ceiling.",
    "town": "You are in a bustling town square. People are going about their business.",
    "dungeon": "You are in a dark and foreboding dungeon. The air is thick with the smell of decay.",
    "generic": "You are in a nondescript room.",
    # Add more room types and descriptions here
}


# COLOR
# Define custom ANSI escape code variables
game_colors = {
"PLAYER_COLOR": "\033[38;5;165m",
"LIST_COMMANDS": "\033[38;5;76m",
"COLOR_RESET": "\033[0m"
}

# Define styles using prompt_toolkit's Style
game_style = Style.from_dict({
    'player': '#a55000',  # Orange
    'list-commands': '#00aa00',  # Green
    'warning': '#ff0000 bold', # Red and bold
    'success': '#00ff00', # Green
    'info': '#0000ff', # Blue
    'error': '#ff0000', # Red
    'debug': '#808080', # Gray
    'room-name': '#00ffff bold', # Cyan and bold
    'room-desc': '#ffffff', # White
    'room-exits': '#ffff00', # Yellow
    'combatant-name': '#ff00ff', # Magenta
    'combatant-stats': '#ffffff', # White
    'combatant-status': '#ffffff', # White
    'combat-action': '#ff0000', # Red
    'combat-damage': '#ff0000', # Red
    'combat-heal': '#00ff00', # Green
    'combat-miss': '#808080', # Gray
    'combat-buff': '#00ff00', # Green
    'combat-debuff': '#ff0000', # Red
    'map-player': '#ff0000 bold', # Red and bold
    'map-room': '#ffffff', # White
    'map-path': '#ffffff', # White
    'map-placeholder': '#808080', # Gray
})

# COLOR_GREEN = "\033[38;5;76m"  # Green
# COLOR_BLUE = "\033[38;5;39m"  # Blue
# COLOR_RED = "\033[38;5;196m"  # Red
# COLOR_ORANGE = "\033[38;5;208m"  # Orange
# COLOR_YELLOW = "\033[38;5;226m"  # Yellow
# COLOR_PURPLE = "\033[38;5;129m"  # Purple
# COLOR_CYAN = "\033[38;5;51m"  # Cyan
# COLOR_WHITE = "\033[38;5;255m"  # White
# COLOR_DARK_GRAY = "\033[38;5;235m"  # Dark Gray
# COLOR_LIGHT_GRAY = "\033[38;5;245m"  # Light Gray


# # Define custom formatting variables
# FORMAT_BOLD = "\033[1m"  # Bold
# FORMAT_ITALIC = "\033[3m"  # Italic
# FORMAT_UNDERLINE = "\033[4m"  # Underline
# FORMAT_RESET = "\033[0m"  # Reset to default



# Notes on a singleton approach
# import threading

# class SharedResources:
#     _stop_event = None

#     @staticmethod
#     def get_stop_event():
#         if SharedResources._stop_event is None:
#             SharedResources._stop_event = threading.Event()
#         return SharedResources._stop_event

# from shared import SharedResources

# stop_event = SharedResources.get_stop_event()

# from shared import SharedResources

# stop_event = SharedResources.get_stop_event()
