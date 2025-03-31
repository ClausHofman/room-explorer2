import json, threading, copy, time, random
from prompt_toolkit import print_formatted_text, ANSI
from prompt_toolkit.formatted_text import FormattedText
from game.shared_resources import room_type_data, game_style
import random

class PlayerActionManager(): # Changed
    def __init__(self, room_manager=None, player=None):
        self.room_manager = room_manager
        self.player = player
    
    def look(self):
        """Displays information about the current room."""
        current_room = self.room_manager.room_lookup[self.player.current_room]

        # Get the room type's data
        room_data = room_type_data[current_room.room_type]

        # Handle both list and single string for long_description
        if isinstance(room_data['long_description'], list):
            room_description = random.choice(room_data['long_description'])
        else:
            room_description = room_data['long_description']

        # Print the room description using prompt_toolkit's styling
        print_formatted_text(FormattedText([
            ('class:room-desc', f"{room_description}\n"),
            ('class:room-desc', "Exits:")
        ]), style=game_style)

        adjacent_rooms = self.room_manager.room_lookup[self.player.current_room].room_exits

        for direction, room_id in adjacent_rooms.items():
            # print(f"{direction}: {self.room_manager.room_lookup[room_id]}") # Room object
            # Query room type using room_lookup and room_id
            nearby_room_type = self.room_manager.room_lookup[room_id].room_type
            # Query key that matches room type and display description
            # print(f"{direction}: {random.choice(room_type_data[nearby_room_type]['short_description'])}")
            
            # Handle both list and single string for short_description
            nearby_room_data = room_type_data[nearby_room_type]
            if isinstance(nearby_room_data['short_description'], list):
                nearby_room_description = random.choice(nearby_room_data['short_description'])
            else:
                nearby_room_description = nearby_room_data['short_description']

            print_formatted_text(FormattedText([
                ('class:room-exit', f"{direction}: "),  # Direction (e.g., "North: ")
                ('class:room-nearby', f"{nearby_room_description}")  # Room description
            ]), style=game_style)


        # Display combatants
        if current_room.combatants:
            for combatant in current_room.combatants:
                # if combatant.id != self.player.id:
                    print(f"  - {combatant.name} (ID: {combatant.id})")
                    # print(f"    {combatant.describe_stats()}")
        else:
            print("There are no combatants in the room.")


    # Called when the player moves with MovementManager
    def exits(self):
        # Display exits
        current_room = self.room_manager.room_lookup[self.player.current_room]
        exits_str = ", ".join(current_room.room_exits.keys())
        print(f"Exits: {exits_str}")




class RoomManager:
    def __init__(self, player=None):
        self.game_rooms = []  # List of Room objects
        self.room_lookup = {}  # Maps room_id to Room objects
        self.active_room_lookup = {}
        self.player = player


    def to_dict(self):
        # Update all combatant's current_room before serialization
        for room in self.game_rooms:
            for combatant in room.combatants:
                combatant.current_room = room.room_id
        # Serialize active rooms
        active_rooms_data = {room_id: room.to_dict() for room_id, room in self.active_room_lookup.items()}
        return {
            "game_rooms": [room.to_dict() for room in self.game_rooms],
            "active_room_ids": list(self.active_room_lookup.keys()),  # Save only room IDs
        }

    @classmethod
    def from_dict(cls, data):
        from game.room import Room
        room_manager = cls()
        if "game_rooms" in data:
            room_manager.game_rooms = [Room.from_dict(room_data) for room_data in data["game_rooms"]]

            # Recreate the room_lookup dictionary
            for room in room_manager.game_rooms:
                room_manager.room_lookup[room.room_id] = room

            # Recreate the active_room_lookup dictionary from the saved IDs
            if "active_room_ids" in data:
                for room_id in data["active_room_ids"]:
                    if room_id in room_manager.room_lookup:
                        room_manager.active_room_lookup[room_id] = room_manager.room_lookup[room_id]
                    else:
                        print(f"[WARNING] Room with ID '{room_id}' not found during deserialization of active_room_lookup.")
        else:
            print("[WARNING] 'game_rooms' key missing in RoomManager data!")
        return room_manager

    def add_room(self, room):
        """Registers a new room in the RoomManager."""
        room.room_manager = self
        self.game_rooms.append(room)
        self.room_lookup[room.room_id] = room
        # print(f"[DEBUG ADD ROOM] Room added: {room.room_name} ({room.room_id})")
    
    def add_room_active(self, room):
        """Add a room to the active rooms dictionary"""
        room.room_manager = self
        self.active_room_lookup[room.room_id] = room
        print(f"[DEBUG ADD ACTIVE ROOM] Room marked as active: {room.room_id}")

    def remove_room_active(self, room_id):
        """Remove a room from the active rooms dictionary"""
        if room_id in self.active_room_lookup:
            del self.active_room_lookup[room_id]
            print(f"[DEBUG REMOVE ACTIVE ROOM] Room removed: {room_id}")
        else:
            print(f"[DEBUG REMOVE ACTIVE ROOM] Room ID {room_id} not found.")


    def create_and_connect_rooms(self, starting_room, test_mode=False, num_rooms_to_create=0):
        from game.room import Room
        import random
        """Handles user input to create and connect multiple rooms dynamically."""
        valid_directions = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest']
        # valid_directions = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest', 'up', 'down']
        cardinal_directions = ['north', 'east', 'south', 'west']
        diagonal_directions = ['northeast', 'southeast', 'southwest', 'northwest']
        opposite_directions = {'north': 'south', 'east': 'west', 'south': 'north', 'west': 'east', 'northeast': 'southwest', 'southeast': 'northwest', 'southwest': 'northeast', 'northwest': 'southeast'}
        # opposite_directions = {'north': 'south', 'east': 'west', 'south': 'north', 'west': 'east', 'up': 'down', 'down': 'up', 'northeast': 'southwest', 'southeast': 'northwest', 'southwest': 'northeast', 'northwest': 'southeast'}

        def get_available_directions(room):
            """Returns available directions where no rooms exist."""
            return [direction for direction in valid_directions if direction not in room.room_exits]

        available_directions = get_available_directions(starting_room)

        if not available_directions:
            print(f"No available directions for {starting_room.room_name} ({starting_room.room_id})!")
            return

        print(f"Available directions for {starting_room.room_name}: {available_directions}")

        directions_to_connect = []  # Initialize here
        user_choice = ""

        if test_mode:
            print(f"[DEBUG] Test mode enabled. Creating {num_rooms_to_create} rooms.")
            current_room = starting_room
            for _ in range(num_rooms_to_create):
                available_directions = get_available_directions(current_room)
                if not available_directions:
                    print(f"[DEBUG] No available directions for {current_room.room_name}. Stopping room creation.")
                    break
                direction = random.choice(available_directions)  # Choose a random direction
                opposite_direction = opposite_directions[direction]

                # Create a new room and register it
                new_room = Room()
                self.add_room(new_room)

                # Establish bidirectional connection
                current_room.room_exits[direction] = new_room.room_id
                new_room.room_exits[opposite_direction] = current_room.room_id

                print(f"[DEBUG] Connected {current_room.room_name} to {new_room.room_name} ({new_room.room_id}) via {direction}")
                current_room = new_room  # Move to the new room for the next iteration
            return

        while True:
            user_input = input(f"How do you want to proceed with connecting rooms to {starting_room.room_id}?\n"
                               f"  - Press Enter to specify the number of rooms manually.\n"
                               f"  - Type 'all' to connect to all available directions.\n"
                               f"  - Type 'cardinal' to connect to available cardinal directions (north, east, south, west).\n"
                               f"  - Type 'diagonal' to connect to available diagonal directions (northeast, southeast, southwest, northwest).\n"
                               f"  - Type 'connect' to connect current room to a specific room id.\n"
                               f"  - Type 'abort' to abort room creation.\n"
                               f"Your choice: ").lower()

            if user_input == "connect":
                while True:
                    try:
                        room_id_to_connect = str(input(f"Please type the room_id of an existing room that is not this room ({starting_room.room_id}). (Enter to abort)\n")).lower()
                        if room_id_to_connect == "":
                            print("Cancelling operation.")
                            return
                        if room_id_to_connect not in self.room_lookup:
                            print(f"Room with ID '{room_id_to_connect}' not found. Please try again.")
                            continue
                        if room_id_to_connect == starting_room.room_id:
                            print("You cannot connect to the current room. Please try again.")
                            continue

                        connection_type = str(input(f"Special or normal connection? (s/n) (Enter to abort)\n")).lower()
                        if connection_type == "":
                            print("Cancelling operation.")
                            return
                        if connection_type == "n":
                            available_directions = get_available_directions(starting_room)
                            if not available_directions:
                                print(f"No available directions for {starting_room.room_name}.")
                                break
                            direction_for_connection = str(input(f"Pick an available direction: {available_directions}. (Enter to abort)\n")).lower()
                            if direction_for_connection == "":
                                print("Cancelling operation.")
                                return
                            if direction_for_connection not in available_directions:
                                print(f"Invalid direction. Please choose one from: {available_directions}")
                                continue
                            if room_id_to_connect in self.room_lookup:
                                starting_room.connect(self.room_lookup[room_id_to_connect], direction_for_connection)
                                print(f"Successfully connected {starting_room.room_id} to {self.room_lookup[room_id_to_connect].room_id}")
                                self.room_lookup[room_id_to_connect].connect(starting_room, opposite_directions[direction_for_connection])
                                print(f"Successfully connected {self.room_lookup[room_id_to_connect].room_id} to {starting_room.room_id}")
                                break
                        elif connection_type == "s":
                            if room_id_to_connect in self.room_lookup:
                                starting_room.connect(self.room_lookup[room_id_to_connect], "special", room_id_to_connect=room_id_to_connect)
                                print(f"Successfully made a special connection from {starting_room.room_id} to {self.room_lookup[room_id_to_connect].room_id}")
                                self.room_lookup[room_id_to_connect].connect(starting_room, "special", starting_room_id=starting_room.room_id)
                                print(f"Successfully made a special connection from {self.room_lookup[room_id_to_connect].room_id} to {starting_room.room_id}")
                                break
                        else:
                            print("Invalid connection type. Please enter 's' or 'n'.")
                    except ValueError:
                        print("Invalid input. Please enter a valid room_id or press Enter to abort.")
                break
            

            # TODO: what if a room is removed, would need to update rooms' connections that were connected to it I think


            elif user_input == "":
                # Proceed with manual room number input
                user_choice = "manual"
                while True:
                    try:
                        num_rooms = int(input(f"How many rooms do you want to connect to {starting_room.room_id}? (0 to abort) Max: {len(available_directions)} "))
                        if num_rooms == 0:
                            print("Aborting room creation.")
                            return
                        if 1 <= num_rooms <= len(available_directions):
                            break
                        print(f"Invalid input. Please input a number between 0 and {len(available_directions)}.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                for _ in range(num_rooms):
                    available_directions = get_available_directions(starting_room)  # Refresh available directions

                    if not available_directions:
                        print(f"No more available directions for {starting_room.room_name}.")
                        break

                    while True:
                        direction = input(f"Pick an available direction: {available_directions} ").lower()
                        if direction in available_directions:
                            directions_to_connect.append(direction)
                            break
                        print(f"Invalid direction. Please choose one from: {available_directions}")
                break

            elif user_input == "all":
                # Connect to all available directions
                user_choice = "all"
                directions_to_connect = available_directions
                break

            elif user_input == "cardinal":
                # Connect to available cardinal directions
                user_choice = "cardinal"
                directions_to_connect = [d for d in available_directions if d in cardinal_directions]
                break

            elif user_input == "diagonal":
                # Connect to available diagonal directions
                user_choice = "diagonal"
                directions_to_connect = [d for d in available_directions if d in diagonal_directions]
                break

            elif user_input == "abort":
                print("Aborting room creation.")
                return

            else:
                print("Invalid choice. Please press Enter, type 'all', 'cardinal', 'diagonal' or 'abort'.")
                continue
            break

        # Exclusion logic (moved outside the inner loop)
        if directions_to_connect and user_choice != "manual":
            if user_choice == "all":
                while True:
                    exclude_input = input(f"Available directions to connect: {directions_to_connect}\n"
                                        f"Enter directions to exclude (comma-separated, e.g., 'north,east') or press Enter to connect to all: ").lower()
                    if exclude_input == "":
                        break  # Skip exclusion
                    exclude_directions = [d.strip() for d in exclude_input.split(',')]
                    invalid_directions = [d for d in exclude_directions if d not in directions_to_connect]
                    if invalid_directions:
                        print(f"Invalid directions: {', '.join(invalid_directions)}. Please use valid directions.")
                    else:
                        directions_to_connect = [d for d in directions_to_connect if d not in exclude_directions]
                        break
            else:
                while True:
                    exclude_input = input(f"Available directions to connect: {directions_to_connect}\n"
                                        f"Enter directions to exclude (comma-separated, e.g., 'north,east') or press Enter to skip: ").lower()
                    if exclude_input == "":
                        break  # Skip exclusion
                    exclude_directions = [d.strip() for d in exclude_input.split(',')]
                    invalid_directions = [d for d in exclude_directions if d not in directions_to_connect]
                    if invalid_directions:
                        print(f"Invalid directions: {', '.join(invalid_directions)}. Please use valid directions.")
                    else:
                        directions_to_connect = [d for d in directions_to_connect if d not in exclude_directions]
                        break

            if not directions_to_connect:
                print("All directions have been excluded. Aborting room creation.")
                return

        for direction in directions_to_connect:
            opposite_direction = opposite_directions[direction]
            print(f"Creating new room in {direction} direction...")

            # Create a new room and register it
            new_room = Room()
            self.add_room(new_room)

            # Establish bidirectional connection
            starting_room.room_exits[direction] = new_room.room_id
            new_room.room_exits[opposite_direction] = starting_room.room_id

            print(f"Connected {starting_room.room_name} to {new_room.room_name} ({new_room.room_id}) via {direction}")


    def get_room_info(self):
        """Retrieve detailed information about a room."""
        room = self.player.current_room
        room_object = self.room_lookup.get(room)

        room_info = [
            f"Room Name: {room_object.room_name}",
            f"Room ID: {room_object.room_id}",
        ]

        print("\n".join(room_info))
        exits_str = ", ".join(room_object.room_exits.keys())
        print(f"Exits: {exits_str}")


    def on_turn_advanced(self, current_turn):
        for room in self.game_rooms:
            room.on_turn_advanced(current_turn)



    def generate_map(self, size=7, search_depth=8):
        DEBUG = False
        MAX_GRID_SIZE = 100  # Set a reasonable maximum size
        if size > MAX_GRID_SIZE:
            raise ValueError(f"Grid size too large! Maximum allowed size is {MAX_GRID_SIZE}.")

        # Initialize grid
        grid = [["#" for _ in range(size * 2 - 1)] for _ in range(size * 2 - 1)]
        middle = size // 2 * 2

        # Hardcode colors for symbols
        symbol_colors = {
            "#": "\033[92m",  # Green for "#"
            "o": "\033[38;5;250m",
            "-": "\033[97m",  # White for "-"
            "X": "\033[38;5;165m",
            "/": "\033[97m",  # White for "/"
            "\\": "\033[97m",  # White for "\"
            "|": "\033[97m",  # White for "|"
        }

        map_symbols = {
            "map_player": "X",
            "map_unoccupied_room": "o"
        }

        map_direction_offsets = {
            "north": (-1, 0),
            "south": (1, 0),
            "east": (0, 1),
            "west": (0, -1),
            "northeast": (-1, 1),
            "northwest": (-1, -1),
            "southeast": (1, 1),
            "southwest": (1, -1)
        }
        map_direction_representations = {
            "north": "|",
            "south": "|",
            "east": "-",
            "west": "-",
            "northeast": "/",
            "southeast": "\\",
            "southwest": "/",
            "northwest": "\\"
        }

        middle_cell = f"row{size // 2 + 1}col{size // 2 + 1}"  # Calculate the middle cell, needed for first new_rooms key
        if DEBUG:
            print(f"[DEBUG] Calculated middle_cell: {middle_cell}")

        # Get the player's room object
        current_room = self.room_lookup[self.player.current_room]
        if DEBUG:
            print(f"[DEBUG] Current room: {self.player.current_room}, Exits: {current_room.room_exits}")

        # Store the player room's ID for later use
        player_room = self.room_lookup[self.player.current_room].room_id
        
        # Step 1: Initialize new_rooms with the middle_cell and its exits
        new_rooms = {middle_cell: current_room.room_exits or {}}
        # Track found rooms
        found_room_ids = [self.player.current_room]
        # Place the player symbol in the middle of the grid (for odd number size grids)
        grid[middle][middle] = map_symbols["map_player"]
        room_process_count = {}  # Track how many times each room has been processed
        current_depth = 1

        if DEBUG:
            print(f"[DEBUG] Starting search with depth: {search_depth}")

        # Step 2: Iterate through rooms up to the search depth
        while current_depth <= search_depth:
            if DEBUG:
                print(f"[DEBUG] Current search depth: {current_depth}, Rooms to process: {list(new_rooms.keys())}")

            rooms_to_add = {}  # Dictionary to store rooms to add
            rooms_to_remove = []  # List to store rooms to remove

            # Start processing keys in new_rooms
            for cell_key in list(new_rooms.keys()):
                if DEBUG:
                    print(f"[DEBUG] Processing cell_key: {cell_key}")
                    
                # Extract room row/col positions using slice
                row, col = map(int, [cell_key[3:cell_key.index("col")], cell_key[cell_key.index("col") + 3:]])
                room_row, room_col = (row - 1) * 2, (col - 1) * 2  # Adjust for grid with paths
                if DEBUG:
                    print(f"[DEBUG] Processing cell_key: {cell_key} (Room coordinates: {room_row}, {room_col})")

                # Process each direction and the connected room
                for direction, new_rooms_room_id in new_rooms[cell_key].items():
                    if DEBUG:
                        print(f"[DEBUG] Checking direction: {direction}, Connection data: {new_rooms_room_id}")
                        
                    # Ignore up and down directions
                    if direction == "up" or direction == "down":
                        continue

                    # Ignore special connections
                    if isinstance(new_rooms_room_id, dict):
                        if DEBUG:
                            print(f"[DEBUG] Ignoring special connection: {direction}")
                        continue  # Skip to the next direction

                    room_id = new_rooms_room_id  # Normal connection, room_id is a string
                    if DEBUG:
                        print(f"[DEBUG] Checking direction: {direction}, Target room_id: {room_id}")

                    # Increment processing count for the room
                    if room_id not in room_process_count:
                        room_process_count[room_id] = 0
                    room_process_count[room_id] += 1

                    # Increase room_process_count if map is behaving funnily, it might not show rooms in some scenarios and more processing is needed
                    if room_process_count[room_id] > 5:
                        if DEBUG:
                            print(f"[DEBUG] Room {room_id} processed {room_process_count[room_id]} times, skipping.")
                        continue

                    # Track the room in found_room_ids
                    if room_id not in found_room_ids:
                        found_room_ids.append(room_id)
                        if DEBUG:
                            print(f"[DEBUG] Added room_id to found_room_ids: {found_room_ids}")

                    # Determine offsets depending on direction
                    row_offset, col_offset = map_direction_offsets[direction]
                    path_row, path_col = room_row + row_offset, room_col + col_offset
                    next_room_row, next_room_col = room_row + row_offset * 2, room_col + col_offset * 2
                    if DEBUG:
                        print(f"[DEBUG] Path position: ({path_row}, {path_col}), Next room position: ({next_room_row}, {next_room_col})")

                    # Update the path in the grid
                    if 0 <= path_row < len(grid) and 0 <= path_col < len(grid):
                        grid[path_row][path_col] = map_direction_representations[direction]
                        if DEBUG:
                            print(f"[DEBUG] Updated path: {grid[path_row][path_col]} at ({path_row}, {path_col})")
                        
                    # Skip placing anything over the player's position because player symbol is already set
                    if room_id == player_room:
                        continue

                    # Otherwise, update the room as usual
                    if 0 <= next_room_row < len(grid) and 0 <= next_room_col < len(grid):
                        grid[next_room_row][next_room_col] = map_symbols["map_unoccupied_room"]
                        if DEBUG:
                            print(f"[DEBUG] Updated room: 'o' at ({next_room_row}, {next_room_col})")

                    # Perform a lookup for the connected room's exits
                    if room_id in self.room_lookup:
                        room_exits = self.room_lookup[room_id].room_exits or {}
                        new_cell_key = f"row{next_room_row // 2 + 1}col{next_room_col // 2 + 1}"
                        if new_cell_key not in new_rooms:
                            rooms_to_add[new_cell_key] = room_exits  # Add to the dictionary instead of directly to new_rooms
                            if DEBUG:
                                print(f"[DEBUG] Added new cell_key: {new_cell_key} with exits: {room_exits}")

                rooms_to_remove.append(cell_key)

            # Remove the processed rooms from new_rooms AFTER the loop
            for cell_key in rooms_to_remove:
                if cell_key in new_rooms:
                    new_rooms.pop(cell_key)
                    if DEBUG:
                        print(f"[DEBUG] Removed processed cell_key: {cell_key}")

            # Add the new rooms to new_rooms AFTER the loop
            new_rooms.update(rooms_to_add)

            current_depth += 1
            if DEBUG:
                print(f"[DEBUG] Moving to next depth level.")

        # Print the final grid
        if DEBUG:
            print(f"[DEBUG] Final grid:")
        for row in grid:
            row_string = ""
            for cell in row:
                if isinstance(cell, str):  # Regular symbol
                    color_code = symbol_colors.get(cell, "\033[97m")  # Default to white if no color
                    row_string += color_code + cell + "\033[0m"  # Reset color after each symbol
                else:
                    row_string += str(cell)  # In case it is already an ANSI object like "X"
            print_formatted_text(ANSI(row_string))

    def remove_room_by_id(self, room_id_to_remove):
        """
        Removes a room from the game, ensuring all references are cleaned up.
        Prompts the user for a room ID to remove.

        Args:
            room_manager (RoomManager): The RoomManager instance.
        """
        while True:
            if room_id_to_remove is None:
                room_id_to_remove = input("Enter the ID of the room to remove (or press Enter to abort): ").strip()
            if not room_id_to_remove:
                print("Aborting room removal.")
                return

            if room_id_to_remove in self.room_lookup:
                break
            else:
                print(f"Room with ID '{room_id_to_remove}' not found. Please try again.")
                room_id_to_remove = None
                continue

        room_to_remove = self.room_lookup[room_id_to_remove]

        print(f"[DEBUG] Removing room: {room_to_remove.room_id} ({room_to_remove.room_name})")

        # 1. Remove the room from room_lookup
        del self.room_lookup[room_id_to_remove]
        print(f"[DEBUG] Removed room '{room_id_to_remove}' from room_lookup.")

        # 2. Remove the room from game_rooms
        self.game_rooms.remove(room_to_remove)
        print(f"[DEBUG] Removed room '{room_id_to_remove}' from game_rooms.")

        # 3. Remove the room from active_room_lookup if it's there
        if room_id_to_remove in self.active_room_lookup:
            del self.active_room_lookup[room_id_to_remove]
            print(f"[DEBUG] Removed room '{room_id_to_remove}' from active_room_lookup.")

        # 4. Clean up references in other rooms' room_exits
        for room in self.game_rooms:
            exits_to_remove = []
            for direction, connected_room_id in room.room_exits.items():
                if isinstance(connected_room_id, dict):
                    if connected_room_id.get("target_room") == room_to_remove:
                        exits_to_remove.append(direction)
                elif connected_room_id == room_id_to_remove:
                    exits_to_remove.append(direction)

            for direction in exits_to_remove:
                del room.room_exits[direction]
                print(f"[DEBUG] Removed exit '{direction}' from room '{room.room_id}' that pointed to '{room_id_to_remove}'.")

        # 5. Clean up combatants' current_room if they were in the removed room
        for combatant in room_to_remove.combatants:
            combatant.current_room = None
            print(f"[DEBUG] Removed current_room reference for combatant '{combatant.id}' that was in room '{room_id_to_remove}'.")

        print(f"[DEBUG] Successfully removed room '{room_id_to_remove}' and cleaned up all references.")


class MovementManager(PlayerActionManager, RoomManager):
    def __init__(self, room_manager=None, player=None, companion=None, creature=None):
        self.room_manager = room_manager
        self.player = player
        self.companion = companion
        self.creature = creature
        

    def move_player(self, player, direction):
        from time import perf_counter
        """Handles moving the player to another room."""

        current_room = self.room_manager.room_lookup[player.current_room]

        if direction not in current_room.room_exits:
            print(f"You can't move to the {direction}. There's no path.")
            return False

        # Update player's current room
        target_room_id = current_room.room_exits[direction]
        target_room = self.room_manager.room_lookup[target_room_id]

        # Remove player from current room
        current_room.player_in_room = False
        # print(f"[DEBUG Player is in room] Player left room {current_room.room_id}, player is in room {current_room.room_id}: {current_room.player_in_room}")
        current_room.remove_combatant_by_id(player.id)

        # Add player to target room and reset grudge list
        player.grudge_list = []
        target_room.add_combatant(player)
        # Check if the room is active and make it active if it is not
        if not target_room.active_room:
            target_room.make_active()
        # Check if the room is active and make it inactive if it is not
        if current_room.active_room:
            current_room.check_and_deactivate()
        player.current_room = target_room.room_id

        # Display map when moving
        self.room_manager.generate_map(size=13, search_depth=40)

        # Show map
        # start_time = perf_counter()
        # map_size = 10
        # map_search_depth = 40
        # self.room_manager.generate_map(size=map_size, search_depth=map_search_depth)
        # end_time = perf_counter()
        # elapsed_time = end_time - start_time
        # print(f"[PERF] Map generation with size {map_size}, search depth {map_search_depth} took {elapsed_time:.6f} seconds.")

        
        # Inherited from PlayerActionManager
        self.exits()

        # Check hostility after moving
        target_room.player_in_room = True
        # print(f"[DEBUG Player is in room] Player moved to {target_room.room_id} and is now in room {target_room.room_id}: {target_room.player_in_room}")
        target_room.detect_hostility(0)

        print(f"You move from {current_room.room_name} to {target_room.room_name} in the {direction}.")

        # Iterate and print combatants in the new room
        other_combatants = [combatant for combatant in target_room.combatants if combatant.id != player.id]
        if other_combatants:
            combatant_strings = [f"{combatant.name}" for combatant in other_combatants]
            print(", ".join(combatant_strings))
        
        return True


    def move_player_command(self, direction, player):
        """Handle the move command for the player."""
        if self is None:
            print("Movement system is not initialized.")
            return

        if direction:
            success = self.move_player(player, direction)
            if not success:
                print(f"Unable to move {direction}.")
        else:
            print("You must specify a direction to move (e.g., 'move north').")

    def to_dict(self):
        """Convert MovementManager to a dictionary."""
        room_manager_id = None
        if self.room_manager and self.player and self.player.current_room in self.room_manager.room_lookup:
            room_manager_id = self.room_manager.room_lookup[self.player.current_room].room_id
        return {
            "room_manager_id": room_manager_id,
            "player_id": self.player.id if self.player else None,
        }

    @classmethod
    def from_dict(cls, data, room_manager, player):
        """Create a MovementManager from a dictionary."""
        movement_manager = cls(room_manager=room_manager, player=player)

        # Update the movement_manager
        movement_manager.room_manager = room_manager
        movement_manager.player = player

        return movement_manager



class TurnManager:
    def __init__(self, stop_event=False):
        from game.input_thread import stop_event
        self.current_turn = 0
        self.room_manager = RoomManager()
        self.stop_event = stop_event
        self.movement_manager = None

    def advance_turn(self):
        self.current_turn += 1
        print(f"[DEBUG TurnManager advance_turn] Global Turn {self.current_turn} begins!")

        # Notify active rooms
        for room in self.room_manager.active_room_lookup.values():
            room.on_turn_advanced(self.current_turn)

    def start_timer(self, interval_seconds):
        def timer_task():
            while not self.stop_event.is_set():
                time.sleep(interval_seconds)
                self.advance_turn()

                # Passively check all game rooms for hostility on regular intervals
                # if self.current_turn % 5 == 0 and self.current_turn != 0:
                #     for room in self.room_manager.game_rooms:
                #         room.detect_hostility()
                #         print("Testing passive hostility check for all game rooms:", room.in_combat, room.combatants)

            print("[DEBUG TurnManager] Timer thread exiting...")

        thread = threading.Thread(target=timer_task, daemon=True)
        thread.start()

    def to_dict(self):
        from game.room import Room
        # Update all combatant's current_room before serialization
        for room in self.room_manager.game_rooms:
            for combatant in room.combatants:
                combatant.current_room = room.room_id
        return {
            "current_turn": self.current_turn,
            "room_manager": self.room_manager.to_dict(),  # Serialize the RoomManager
            "room_count": Room.room_count,  # Include the current room_count value
            "movement_manager": self.movement_manager.to_dict() if self.movement_manager else None
        }

    @classmethod
    def from_dict(cls, data):
        from game.room import Room
        Room.room_count = 0 # Reset room_count when loading
        turn_manager = cls()
        if "room_manager" in data:
            turn_manager.room_manager = RoomManager.from_dict(data["room_manager"])  # Deserialize RoomManager
        if "current_turn" in data:
            turn_manager.current_turn = data["current_turn"]  # Restore current turn
        else:
            print("[WARNING] 'current_turn' key missing in save file data!")
        if "movement_manager" in data and data["movement_manager"]:
            turn_manager.movement_manager = MovementManager.from_dict(data["movement_manager"], turn_manager.room_manager, None)
        else:
            turn_manager.movement_manager = None
        return turn_manager


class CombatantManager:
    def __init__(self, traits_dict, status_effects, selected_traits=None):
        """
        :param traits_dict: A dictionary of all possible traits.
        :param status_effects: A dictionary of all status effects.
        :param selected_traits: A list of keys to select specific traits from traits_dict.
        """
        self.all_traits = traits_dict
        self.selected_traits = {key: traits_dict[key] for key in (selected_traits or [])}
        self.buffs = copy.deepcopy(status_effects.get("buffs", {}))
        self.debuffs = copy.deepcopy(status_effects.get("debuffs", {}))
        self.current_power = 0  # Example power tracking

    # Resolves active effects based on non-zero durations
    def get_active_effects(self, effects):
        active_effects = [
            f"{key} (Duration: {value[0]}, Strength: {value[1]})"
            for key, value in effects.items()
            if value[0] > 0  # Only include active effects with duration > 0
        ]
        return ", ".join(active_effects) if active_effects else "None"

    # Trait-related methods
    def describe_traits(self):
        if not self.selected_traits:
            return "No special traits."
        return ", ".join([f"{key}: {value}" for key, value in self.selected_traits.items()])

    # Buff-related methods
    def add_buff(self, buff_key, duration, strength):
        if buff_key in self.buffs:
            self.buffs[buff_key][0] += duration
            self.buffs[buff_key][1] += strength
        else:
            self.buffs[buff_key] = [duration, strength]
        self.current_power += strength
        print(f"Buff '{buff_key}' added (Duration: {duration}, Strength: {strength}). Current power: {self.current_power}.")
        self._update_cached_stats()

    def remove_buff(self, buff_key):
        if buff_key in self.buffs:
            strength_to_remove = self.buffs[buff_key][1]
            self.current_power = max(0, self.current_power - strength_to_remove)
            del self.buffs[buff_key]
            print(f"Buff '{buff_key}' removed. Current power: {self.current_power}.")
            self._update_cached_stats()
        else:
            print(f"Buff '{buff_key}' does not exist.")

    def decrement_buff_durations(self):
        for buff_key in list(self.buffs.keys()):
            if self.buffs[buff_key][0] > 0:
                self.buffs[buff_key][0] -= 1
                if self.buffs[buff_key][0] <= 0:
                    self.remove_buff(buff_key)

    # Debuff-related methods
    def add_debuff(self, debuff_key, duration, strength):
        if debuff_key in self.debuffs:
            self.debuffs[debuff_key][0] += duration
            self.debuffs[debuff_key][1] += strength
        else:
            self.debuffs[debuff_key] = [duration, strength]
        print(f"Debuff '{debuff_key}' added (Duration: {duration}, Strength: {strength}).")
        self._update_cached_stats()

    def remove_debuff(self, debuff_key):
        if debuff_key in self.debuffs:
            del self.debuffs[debuff_key]
            print(f"Debuff '{debuff_key}' removed.")
            self._update_cached_stats()
        else:
            print(f"Debuff '{debuff_key}' does not exist.")

    def decrement_debuff_durations(self):
        for debuff_key in list(self.debuffs.keys()):
            if self.debuffs[debuff_key][0] > 0:
                self.debuffs[debuff_key][0] -= 1
                if self.debuffs[debuff_key][0] <= 0:
                    self.remove_debuff(debuff_key)

    # Describe active buffs and debuffs
    def describe_status(self):
        buffs_desc = self.get_active_effects(self.buffs)
        debuffs_desc = self.get_active_effects(self.debuffs)
        return f"Buffs: {buffs_desc}\nDebuffs: {debuffs_desc}"



import json
import os

class SaveLoadManager:
    @staticmethod
    def save_to_file(turn_manager):
        """Saves the game state to a user-specified file."""
        while True:
            filename = input("Enter a filename to save the game (or type 'cancel' to abort): ").strip()
            if filename.lower() == "cancel":
                print("Save operation cancelled.")
                return
            if not filename:
                print("Filename cannot be empty.")
                continue
            if not filename.isalnum() and "_" not in filename:
                print("Filename can only contain alphanumeric characters and underscores.")
                continue
            
            filepath = os.path.join("serialization", f"{filename}.json")
            try:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Ensure directory exists
                with open(filepath, "w") as file:
                    json.dump(turn_manager.to_dict(), file, indent=4)
                print(f"[DEBUG] Successfully saved TurnManager to {filepath}")
                break  # Exit the loop on successful save
            except Exception as e:
                print(f"[ERROR] Failed to save game: {e}")


    @staticmethod
    def load_from_file(player):
        """Loads the game state from a user-specified file."""
        serialization_dir = "serialization"
        available_files = [f for f in os.listdir(serialization_dir) if f.endswith(".json")]

        if not available_files:
            print("No save files found in the 'serialization/' directory.")
            return None

        print("Available save files:")
        for i, filename in enumerate(available_files):
            print(f"{i + 1}. {filename}")

        while True:
            user_input = input("Enter the number of the file to load (or type 'cancel' to abort): ").strip()
            if user_input.lower() == "cancel":
                print("Load operation cancelled.")
                return None
            try:
                choice = int(user_input) - 1
                if 0 <= choice < len(available_files):
                    filename = available_files[choice]
                    filepath = os.path.join(serialization_dir, filename)
                    with open(filepath, "r") as file:
                        data = json.load(file)
                    print(f"[DEBUG] Successfully loaded TurnManager from {filepath}")

                    # Deserialize the TurnManager and retrieve the room manager
                    turn_manager = TurnManager.from_dict(data)

                    # Retrieve room manager from the turn manager
                    room_manager = turn_manager.room_manager
                    print(f"[DEBUG load_from_file] Loaded room_manager: {room_manager}")
                    print(f"[DEBUG load_from_file] room_manager.room_lookup: {room_manager.room_lookup}")

                    # Retrieve movement manager from the turn manager
                    if turn_manager.movement_manager is None:
                        print("[DEBUG load_from_file] movement_manager is None. Creating a new one.")
                        movement_manager = MovementManager(room_manager, player)
                        turn_manager.movement_manager = movement_manager
                    else:
                        print("[DEBUG load_from_file] movement_manager found in turn_manager.")
                        movement_manager = turn_manager.movement_manager
                    print(f"[DEBUG load_from_file] Loaded movement_manager: {movement_manager}")

                    # Set the room manager and player attributes of the movement manager
                    movement_manager.room_manager = room_manager
                    movement_manager.player = player
                    print(f"[DEBUG load_from_file] movement_manager.room_manager: {movement_manager.room_manager}")
                    print(f"[DEBUG load_from_file] movement_manager.player: {movement_manager.player}")

                    # Before updating the player's data
                    print(f"[DEBUG load_from_file] Before updating player.current_room: {player.current_room}")

                    # Look through all rooms to find the corresponding player combatant
                    updated_player_data = None  # Placeholder for updated player combatant data
                    for room in room_manager.game_rooms:
                        for combatant in room.combatants:
                            print("Searching combatants during loading:", combatant.id, combatant.name)
                            if combatant.id.startswith("player"):  # Assuming the player is identified this way
                                print(f"[DEBUG load_from_file] Found player combatant with ID: {combatant.id} in room {room.room_id}")
                                # Update the player's attributes with the combatant's data
                                for attr, value in vars(combatant).items():
                                    setattr(player, attr, value)  # Dynamically update player attributes
                                print(f"[DEBUG load_from_file] Updated player data with combatant data: {vars(player)}")
                                updated_player_data = combatant
                                break
                        if updated_player_data:
                            break

                    # Ensure the player's current room is set correctly
                    if updated_player_data:
                        player.current_room = updated_player_data.current_room
                        print(f"[DEBUG load_from_file] Player's current room set to: {player.current_room}")
                    else:
                        print("[ERROR load_from_file] Player combatant not found during loading!")

                    # Remove any duplicates and ensure proper room transition
                    if player.current_room in room_manager.room_lookup:
                        print(f"[DEBUG load_from_file] Transitioning player to room: {player.current_room}")
                        # Remove any existing player combatants in the player's current room
                        current_room = room_manager.room_lookup[player.current_room]
                        current_room.remove_combatant_by_id(player.id)
                        # Add the up-to-date player to the current room
                        current_room.add_combatant(player)
                    else:
                        print(f"[ERROR load_from_file] Room with ID '{player.current_room}' not found in room lookup!")


                    # Update the combatants' current room
                    for room in room_manager.game_rooms:
                        for combatant in room.combatants:
                            if not combatant.id.startswith("player"):
                                combatant.current_room = room.room_id

                    # Debug update the grudges
                    for room in room_manager.game_rooms:
                        room.detect_hostility(turn_manager)

                    return turn_manager
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number or 'cancel'.")
            except FileNotFoundError:
                print(f"[ERROR] Save file not found: {filename}")
                return None
            except json.JSONDecodeError:
                print(f"[ERROR] Invalid JSON data in save file: {filename}")
                return None
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred during loading: {e}")
                raise  # Re-raise the exception to be handled elsewhere

