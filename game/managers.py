import json, threading, copy, time


class PlayerActionManager():

    # Called when the player moves with MovementManager
    def exits(self):
        adjacent_rooms = self.room_manager.room_lookup[self.player.current_room].room_exits
        
        for direction, room_id in adjacent_rooms.items():
            print(f"{direction}: {self.room_manager.room_lookup[room_id].room_short_desc}")

    def look(self):
        """Displays the exits and combatants in the current room."""
        current_room = self.room_manager.room_lookup[self.player.current_room]

        # Display exits
        exits_str = ", ".join(current_room.room_exits.keys())
        print(f"Exits: {exits_str}")

        # Display combatants
        if current_room.combatants:
            for combatant in current_room.combatants:
                if combatant.id != self.player.id:
                    print(f"  - {combatant.name} (ID: {combatant.id})")
        else:
            print("There are no combatants in the room.")

class RoomManager:
    def __init__(self):
        self.game_rooms = []  # List of Room objects
        self.room_lookup = {}  # Maps room_id to Room objects

    def add_room(self, room):
        """Registers a new room in the RoomManager."""
        room.room_manager = self
        self.game_rooms.append(room)
        self.room_lookup[room.room_id] = room
        print(f"[DEBUG ADD ROOM] Room added: {room.room_name} ({room.room_id})")

    def create_and_connect_rooms(self, starting_room):
        from game.room import Room
        """Handles user input to create and connect multiple rooms dynamically."""
        valid_directions = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest', 'up', 'down']
        cardinal_directions = ['north', 'east', 'south', 'west']
        diagonal_directions = ['northeast', 'southeast', 'southwest', 'northwest']
        opposite_directions = {'north': 'south', 'east': 'west', 'south': 'north', 'west': 'east', 'up': 'down', 'down': 'up', 'northeast': 'southwest', 'southeast': 'northwest', 'southwest': 'northeast', 'northwest': 'southeast'}

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

        while True:
            user_input = input(f"How do you want to proceed with connecting rooms to {starting_room.room_id}?\n"
                               f"  - Press Enter to specify the number of rooms manually.\n"
                               f"  - Type 'all' to connect to all available directions.\n"
                               f"  - Type 'cardinal' to connect to available cardinal directions (north, east, south, west).\n"
                               f"  - Type 'diagonal' to connect to available diagonal directions (northeast, southeast, southwest, northwest).\n"
                               f"  - Type 'abort' to abort room creation.\n"
                               f"Your choice: ").lower()

            if user_input == "":
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




    def get_room_info(self, room_id):
        """Retrieve detailed information about a room."""
        room = self.room_lookup.get(room_id)
        if not room:
            return f"[ERROR] Room with ID '{room_id}' not found."

        room_info = [
            f"Room Name: {room.room_name}",
            f"Room ID: {room.room_id}",
            "Exits:"
        ]
        if room.room_exits:
            for direction, target_id in room.room_exits.items():
                target_room = self.room_lookup.get(target_id)
                room_info.append(f"  {direction} -> {target_room.room_name if target_room else target_id}")
        else:
            room_info.append("  No exits")

        room_info.append("Status: In combat" if room.in_combat else "Status: Peaceful")

        return "\n".join(room_info)


    def on_turn_advanced(self, current_turn):
        for room in self.game_rooms:
            room.on_turn_advanced(current_turn)

    def display_map(self):
        map_output = []
        for room_id, room in self.room_lookup.items():
            connections = []
            for direction, target_room_id in room.room_exits.items():
                # Use room_lookup to resolve the room ID into an actual Room object
                target_room = self.room_lookup.get(target_room_id)
                if target_room:
                    connections.append(f"{direction} -> {target_room.room_id}")
                else:
                    connections.append(f"{direction} -> (unknown room)")  # Handle missing rooms gracefully
            if connections:
                map_output.append(f"{room.room_name} ({room_id}):\n    " + "\n    ".join(connections))
            else:
                map_output.append(f"{room.room_name} ({room_id}):\n    No connections")
        print("\n".join(map_output))


    def to_dict(self):
        # Update all combatant's current_room before serialization
        for room in self.game_rooms:
            for combatant in room.combatants:
                combatant.current_room = room.room_id
        return {
            "game_rooms": [room.to_dict() for room in self.game_rooms],  # Serialize all rooms
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
        else:
            print("[WARNING] 'game_rooms' key missing in RoomManager data!")
        return room_manager


class MovementManager(PlayerActionManager, RoomManager):
    def __init__(self, room_manager=None, player=None, companion=None, creature=None):
        self.room_manager = room_manager
        self.player = player
        self.companion = companion
        self.creature = creature
        

    def move_player(self, player, direction):
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
        print(f"[DEBUG Player is in room] Player left room {current_room.room_id}, player is in room {current_room.room_id}: {current_room.player_in_room}")
        current_room.remove_combatant_by_id(player.id)

        # Add player to target room and reset grudge list
        player.grudge_list = []
        target_room.add_combatant(player)
        player.current_room = target_room.room_id
        # Inherited from PlayerActionManager
        self.exits()

        # Check hostility after moving
        target_room.player_in_room = True
        print(f"[DEBUG Player is in room] Player moved to {target_room.room_id} and is now in room {target_room.room_id}: {target_room.player_in_room}")
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

        # Restore the player's current_room if possible
        if data.get("room_manager_id") and room_manager and player:
            if data["room_manager_id"] in room_manager.room_lookup:
                # Remove the player from the old room
                old_room = next((room for room in room_manager.game_rooms if player in room.combatants), None)
                if old_room:
                    old_room.remove_combatant_by_id(player.id)
                # Update the player's current room
                player.current_room = data["room_manager_id"]
                # Add the player to the new room
                room_manager.room_lookup[player.current_room].add_combatant(player)
                # Update the movement_manager
                movement_manager.room_manager = room_manager
                movement_manager.player = player
            else:
                print(f"[WARNING] Room with ID '{data['room_manager_id']}' not found in RoomManager. Player's current_room not restored.")

        return movement_manager



class TurnManager:
    def __init__(self, stop_event=False):
        from game.input_thread import stop_event
        self.current_turn = 0
        self.room_manager = RoomManager()
        self.running = False
        self.stop_event = stop_event
        self.movement_manager = None

    def advance_turn(self):
        self.current_turn += 1
        print(f"[DEBUG TurnManager advance_turn] Global Turn {self.current_turn} begins!")

        # Notify rooms in combat
        for room in self.room_manager.game_rooms:
            if room.in_combat:
                room.advance_combat_round(self.current_turn)

    def start_timer(self, interval_seconds):
        def timer_task():
            while not self.stop_event.is_set():
                # print(f"Timer running. stop_event.is_set(): {self.stop_event.is_set()}")
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

    def remove_buff(self, buff_key):
        if buff_key in self.buffs:
            strength_to_remove = self.buffs[buff_key][1]
            self.current_power = max(0, self.current_power - strength_to_remove)
            del self.buffs[buff_key]
            print(f"Buff '{buff_key}' removed. Current power: {self.current_power}.")
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

    def remove_debuff(self, debuff_key):
        if debuff_key in self.debuffs:
            del self.debuffs[debuff_key]
            print(f"Debuff '{debuff_key}' removed.")
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
                    # Set room manager attribute of the movement manager to the loaded room manager
                    movement_manager.room_manager = room_manager
                    # Set the player attribute of the movement manager to the loaded player
                    movement_manager.player = player
                    print(f"[DEBUG load_from_file] movement_manager.room_manager: {movement_manager.room_manager}")
                    print(f"[DEBUG load_from_file] movement_manager.player: {movement_manager.player}")

                    # Update the player's current room
                    print(f"[DEBUG load_from_file] Before updating player.current_room: {player.current_room}")
                    player.current_room = room_manager.room_lookup[player.current_room].room_id
                    print(f"[DEBUG load_from_file] After updating player.current_room: {player.current_room}")
                    # Add the player to the correct room
                    room_manager.room_lookup[player.current_room].add_combatant(player)

                    # Update the combatants' current room
                    for room in room_manager.game_rooms:
                        for combatant in room.combatants:
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



