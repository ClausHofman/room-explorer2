import json, threading, copy, time


class SaveLoadManager:
    @staticmethod
    def save_to_file(filename, turn_manager):
        try:
            with open(filename, "w") as file:
                json.dump(turn_manager.to_dict(), file, indent=4)
            print(f"[DEBUG] Successfully saved TurnManager to {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to save game: {e}")

    @staticmethod
    def load_from_file(filename, **kwargs):
        try:
            # Load the primary save file
            with open(f"{filename}", "r") as file:
                data = json.load(file)
            print(f"[DEBUG] Successfully loaded TurnManager from {filename}")
            
            # Inject optional dictionaries from **kwargs into the game memory
           
            optional_data = {}
            if optional_data:
                for key, filepath in kwargs.items():
                    try:
                        with open(filepath, "r") as optional_file:
                            loaded_data = json.load(optional_file)
                            # Assign the entire content of the file or its specific key to optional_data
                            optional_data[key] = loaded_data.get(key, loaded_data)
                        print(f"[DEBUG] Successfully loaded additional data: {key} from {filepath}")
                    except Exception as e:
                        print(f"[WARNING] Failed to load optional file {key}: {e}")

            return TurnManager.from_dict(data), optional_data
        except Exception as e:
            print(f"[ERROR] Failed to load game: {e}")
            return None, None


class RoomManager:
    def __init__(self):
        self.game_rooms = []  # List of Room objects
        self.room_lookup = {}  # Maps room_id to Room objects

    def add_room(self, room):
        room.room_manager = self
        self.game_rooms.append(room)
        self.room_lookup[room.room_id] = room  # Add to lookup
        print(f"[DEBUG ADD ROOM] Room added: {room.room_name} ({room.room_id})")

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

    def get_room_info(self, room_id):
        """
        Retrieve and display detailed information about a room based on its room_id.
        
        Args:
            room_id (str): The ID of the room to query.
        
        Returns:
            str: A string representation of the room's details.
        """
        # Look up the room in room_lookup
        room = self.room_lookup.get(room_id)
        if not room:
            return f"[ERROR] Room with ID '{room_id}' not found."

        # Compile room details
        room_info = [
            f"Room Name: {room.room_name}",
            f"Room ID: {room.room_id}",
            "Exits:"
        ]
        if room.room_exits:
            for direction, target_id in room.room_exits.items():
                room_info.append(f"  {direction} -> {target_id}")
        else:
            room_info.append("  No exits")

        # Add additional details if applicable
        if room.in_combat:
            room_info.append("Status: In combat")
        else:
            room_info.append("Status: Peaceful")

        return "\n".join(room_info)

    def to_dict(self):
        return {
            "game_rooms": [room.to_dict() for room in self.game_rooms],  # Serialize all rooms
        }

    @classmethod
    def from_dict(cls, data):
        from room import Room
        room_manager = cls()
        if "game_rooms" in data:
            room_manager.game_rooms = [Room.from_dict(room_data) for room_data in data["game_rooms"]]

            # Recreate the room_lookup dictionary
            for room in room_manager.game_rooms:
                room_manager.room_lookup[room.room_id] = room
        else:
            print("[WARNING] 'game_rooms' key missing in RoomManager data!")
        return room_manager


class TurnManager:
    def __init__(self):
        self.current_turn = 0
        self.room_manager = RoomManager()  # Manages all game rooms
        self.running = False  # Ensure running is initialized

    def advance_turn(self):
        self.current_turn += 1
        print(f"[DEBUG TurnManager advance_turn] Global Turn {self.current_turn} begins!")

        # Notify rooms in combat
        for room in self.room_manager.game_rooms:
            if room.in_combat:
                room.advance_combat_round(self.current_turn)

    def start_timer(self, interval_seconds):
        def timer_task():
            while self.running:  # Use a flag to control the loop
                time.sleep(interval_seconds)
                self.advance_turn()

        self.running = True
        thread = threading.Thread(target=timer_task, daemon=True)
        thread.start()

    def stop_timer(self):
        self.running = False  # Stop the timer thread gracefully

    def to_dict(self):
        from room import Room
        return {
            "current_turn": self.current_turn,
            "room_manager": self.room_manager.to_dict(),  # Serialize the RoomManager
            "room_count": Room.room_count  # Include the current room_count value
        }

    @classmethod
    def from_dict(cls, data):
        from room import Room
        Room.room_count = 0 # Reset room_count when loading
        turn_manager = cls()
        if "room_manager" in data:
            turn_manager.room_manager = RoomManager.from_dict(data["room_manager"])  # Deserialize RoomManager
        if "current_turn" in data:
            turn_manager.current_turn = data["current_turn"]  # Restore current turn
        else:
            print("[WARNING] 'current_turn' key missing in save file data!")
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
            self.current_power -= strength_to_remove
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


class SaveLoadManager:
    @staticmethod
    def save_to_file(filename, turn_manager):
        try:
            with open(filename, "w") as file:
                json.dump(turn_manager.to_dict(), file, indent=4)
            print(f"[DEBUG] Successfully saved TurnManager to {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to save game: {e}")

class SaveLoadManager:
    @staticmethod
    def save_to_file(filename, turn_manager):
        try:
            with open(filename, "w") as file:
                json.dump(turn_manager.to_dict(), file, indent=4)
            print(f"[DEBUG] Successfully saved TurnManager to {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to save game: {e}")

    @staticmethod
    def load_from_file(filename, **kwargs):
        try:
            # Load the primary save file
            with open(f"{filename}", "r") as file:
                data = json.load(file)
            print(f"[DEBUG] Successfully loaded TurnManager from {filename}")
            
            # Inject optional dictionaries from **kwargs into the game memory
           
            optional_data = {}
            if optional_data:
                for key, filepath in kwargs.items():
                    try:
                        with open(filepath, "r") as optional_file:
                            loaded_data = json.load(optional_file)
                            # Assign the entire content of the file or its specific key to optional_data
                            optional_data[key] = loaded_data.get(key, loaded_data)
                        print(f"[DEBUG] Successfully loaded additional data: {key} from {filepath}")
                    except Exception as e:
                        print(f"[WARNING] Failed to load optional file {key}: {e}")

            return TurnManager.from_dict(data)
        except Exception as e:
            print(f"[ERROR] Failed to load game: {e}")
            return None, None

