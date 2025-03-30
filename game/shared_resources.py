from prompt_toolkit.styles import Style
import threading
import random

# Initialize stop_event
stop_event = threading.Event()

room_type_data = {
    "forest_random": {
        "short_description": [
            "A dense forest.",
            "Towering trees in a lush forest.",
            "A thick forest with overgrown vines."
        ],
        "long_description": [
            "Sunlight filters through the leaves above, and the air is filled with the scent of earth and greenery.",
            "The forest floor is soft and damp, with birds chirping high above.",
            "A cool breeze flows through the trees, carrying the scent of pine and moss."
        ]
    },
    "forest_fixed": {
        "short_description": "A dense forest.",
        "long_description": "Sunlight filters through the leaves above, and the air is filled with the scent of earth and greenery."
    },
    "cave_random": {
        "short_description": [
            "A dark, damp cave.",
            "A shadowy cave with heavy, moist air.",
            "A cold and oppressive cave."
        ],
        "long_description": [
            "Water drips from the ceiling, and the air smells of moisture and decay. The walls are slick with dampness.",
            "The silence is deafening, broken only by the occasional sound of dripping water.",
            "The floor is uneven and wet, and you can hear the faint echo of distant sounds."
        ]
    },
    "cave_fixed": {
        "short_description": "A dark, damp cave.",
        "long_description": "Water drips from the ceiling, and the air smells of moisture and decay. The walls are slick with dampness."
    },
    "town_random": {
        "short_description": [
            "A bustling town square.",
            "A busy town square filled with merchants and townsfolk.",
            "A crowded town square with people going about their business."
        ],
        "long_description": [
            "People are going about their business, walking between stalls selling goods. The air is filled with the hum of conversation and clinking coins.",
            "Vendors are calling out their wares, and children run around, laughing and playing.",
            "A light breeze rustles the leaves of nearby trees, and the sounds of the town fill the air."
        ]
    },
    "town_fixed": {
        "short_description": "A bustling town square.",
        "long_description": "People are going about their business, walking between stalls selling goods. The air is filled with the hum of conversation and clinking coins."
    },
    "dungeon_random": {
        "short_description": [
            "A dark and foreboding dungeon.",
            "A cold and oppressive dungeon with narrow stone passages.",
            "A dimly lit dungeon, thick with dust and age."
        ],
        "long_description": [
            "The air is thick with the smell of decay, and the walls are covered in moss. Strange noises echo through the corridors.",
            "The dungeon is damp and musty, with flickering torchlight casting long shadows across the stone floor.",
            "Chains rattle faintly in the distance, and the stone walls seem to close in around you."
        ]
    },
    "dungeon_fixed": {
        "short_description": "A dark and foreboding dungeon.",
        "long_description": "The air is thick with the smell of decay, and the walls are covered in moss. Strange noises echo through the corridors."
    },
    "generic_random": {
        "short_description": [
            "A nondescript room.",
            "A plain and featureless room.",
            "A small, unremarkable room."
        ],
        "long_description": [
            "The room is plain and unremarkable, with only bare walls and a floor of smooth stone.",
            "There is nothing in this room, except for the cold, unyielding walls around you.",
            "The air feels stale and lifeless, as if no one has entered this room in years."
        ]
    },
    "generic_fixed": {
        "short_description": "A nondescript room.",
        "long_description": "The room is plain and unremarkable, with only bare walls and a floor of smooth stone."
    },
    "starting_area_fixed": {
        "short_description": "A starting area.",
        "long_description": "This is the starting area."
    },
    "starting_area_custom": {
        "short_description": "A custom starting area.",
        "long_description": "This is a custom starting area."
    }
}


# COLOR
# Define custom ANSI escape code variables
game_colors = {
"PLAYER_COLOR": "\033[38;5;165m",
"LIST_COMMANDS": "\033[38;5;39m",
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
