import game.combatant_data as combatant_data
from game.combatants import Player, Companion, Monster
from game.shared_resources import room_type_data
import random

class Room:
    room_count = 0

    def __init__(self, room_name="Default room name", room_id=None, always_track_turns=False, in_combat=False, combat_rounds=0, room_type="generic_random", combat_start_turn=0):
        Room.room_count += 1  # Increment the count unconditionally
        self.room_name = room_name
        if room_id is None:
            self.room_id = f"room{Room.room_count}"  # Generate a unique room ID
        else:
            self.room_id = room_id  # Use the provided room ID
        self.in_combat = in_combat
        self.always_track_turns = always_track_turns
        self.combat_start_turn = combat_start_turn
        self.combat_rounds = combat_rounds
        self.combatants = []  # Holds Player, Companion, and Monster objects
        self.entities = []  # Not in use, could be used for other objects in the future
        self.room_exits = {}
        self.player_in_room = False
        self.room_type = room_type
        self.in_combat = in_combat
        self.active_room = False
        self.room_manager = None
        

    def to_dict(self):
        # Update all combatant's current_room before serialization
        for combatant in self.combatants:
            combatant.current_room = self.room_id
        room_dict = {
            "room_name": self.room_name,
            "room_id": self.room_id,
            "in_combat": self.in_combat,
            "combat_start_turn": self.combat_start_turn,
            "combat_rounds": self.combat_rounds,
            "always_track_turns": self.always_track_turns,
            "combatants": [
                {"type": type(combatant).__name__, "data": combatant.to_dict()} for combatant in self.combatants
            ],
            "entities": [
                {"type": type(entity).__name__, "data": entity.to_dict()} for entity in self.entities
            ],
            "room_exits": self.room_exits,
            "room_type": self.room_type,
            "active_room": self.active_room
        }
        return room_dict



    @classmethod
    def from_dict(cls, room_data):
        # Validate required fields
        room_id = room_data.get("room_id")
        if not room_id:
            raise ValueError("Missing required 'room_id' in Room deserialization data.")

        # Reconstruct the Room object
        reconstructed_room = cls(
            room_name=room_data.get("room_name", "Default room name"),
            room_id=room_id,
            always_track_turns=room_data.get("always_track_turns", False),
            in_combat=room_data.get("in_combat", False),
            combat_start_turn=room_data.get("combat_start_turn", 0),
            combat_rounds=room_data.get("combat_rounds", 0),
            room_type=room_data.get("room_type", "generic_random")
        )
        
        print(f"[DEBUG FROM_DICT] Reconstructed Room: {reconstructed_room.room_id}, "
            f"always_track_turns={reconstructed_room.always_track_turns}, "
            f"in_combat={reconstructed_room.in_combat}, "
            f"combat_rounds={reconstructed_room.combat_rounds}")

        # Add room_exits after initialization, here because is not in the __init__ constructor
        reconstructed_room.room_exits = room_data.get("room_exits", {})
        # Add active_room after initialization
        reconstructed_room.active_room = room_data.get("active_room", False)
        
        # print(f"[DEBUG ROOM.PY] room_data: {room_data}")
        # Deserialize combatants
        deserialized_combatants = [
            globals()[combatant_data["type"]].from_dict(combatant_data["data"]) for combatant_data in room_data["combatants"]
        ]
        reconstructed_room.combatants = deserialized_combatants

        # Update the current_room of the combatants
        for combatant in reconstructed_room.combatants:
            combatant.current_room = reconstructed_room.room_id

        # Deserialize entities
        deserialized_entities = [
            globals()[entity_data["type"]].from_dict(entity_data["data"]) for entity_data in room_data["entities"]
        ]
        reconstructed_room.entities = deserialized_entities

        return reconstructed_room

    def make_active(self):
        """Marks the room as active and notifies the RoomManager."""
        if not self.active_room:
            self.active_room = True
            if self.room_manager:
                self.room_manager.add_room_active(self)
                print(f"[DEBUG make_active] Room {self.room_id} is now active.")

    def check_and_deactivate(self):
        """Checks if the room should be deactivated and deactivates it if necessary."""
        if self.active_room and not self.combatants:
            self.active_room = False
            if self.room_manager:
                self.room_manager.remove_room_active(self.room_id)
                print(f"[DEBUG check_and_deactivate] Room {self.room_id} is now inactive.")    

    def connect(self, target_room, direction="Unknown", **room_ids):
        """
        Connect this room to another room, optionally using room IDs or extra metadata via room_ids.

        Args:
            target_room (Room): The Room object to connect to.
            direction (str): The direction of the exit (e.g., 'north', 'special_portal').
            **room_ids: Additional room ID or metadata for the connection.
        """
        # Debug statements for troubleshooting
        print(f"[DEBUG] Attempting to connect {self.room_id} to {target_room.room_id} via {direction}")
        print(f"[DEBUG] Available directions: {self.available_directions()}")
        
        opposite_direction = {"north": "south", "south": "north", "east": "west", "west": "east", 
                            "northeast": "southwest", "southeast": "northwest", 
                            "southwest": "northeast", "northwest": "southeast"}.get(direction)
        print(f"[DEBUG] Opposite direction: {direction} -> {opposite_direction}")

        # Handle normal exits
        if direction in self.available_directions()['normal_exits'] and not room_ids and direction != "Unknown":
            self.room_exits[direction] = target_room.room_id
            if opposite_direction:
                target_room.room_exits[opposite_direction] = self.room_id
            print(f"[DEBUG CONNECT] Connected {self.room_id} to {target_room.room_id} via {direction}")
            return

        # Handle special connections via room_ids
        elif room_ids:
            connection_data = {"target_room": target_room}
            connection_data.update(room_ids)  # Add the metadata
            self.room_exits[direction] = connection_data
            print(f"[DEBUG CONNECT] Special connection established for {self.room_id}: {direction} -> {connection_data}")
            return

        raise ValueError("Invalid connection parameters. Check direction or room_ids!")


    @staticmethod
    def available_directions():
        exits = {'normal_exits': ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest'],
                'special_exits': []}
        return exits
    

    def advance_turn(self, current_turn):
        # Logic for rooms that should always track turns
        if self.always_track_turns:
            print(f"Room {self.room_id} processes turn-based events on Turn {current_turn}.")

        # Logic for combat
        if self.in_combat and current_turn > self.combat_start_turn + self.combat_rounds:
            self.combat_rounds += 1
            print(f"Combat Round {self.combat_rounds} begins in Room {self.room_id}!")

    def on_turn_advanced(self, current_turn): # TODO: might need to modify this if going for out of combat stuff that require tracking turns
        if self.in_combat:
            self.advance_combat_round(current_turn)


    def advance_combat_round(self, current_turn):
        print(f"[DEBUG advance_combat_round] Starting advance_combat_round in Room {self.room_id}!") # Added debug statement
        if not self.in_combat:
            return  # Skip if not in combat

        # Only advance if we're on the right turn
        if current_turn > self.combat_start_turn + self.combat_rounds:
            self.combat_rounds += 1  # Increment the round number
            print(f"[DEBUG advance_combat_round] Starting Combat Round {self.combat_rounds} in Room {self.room_id}!")

            # Process active combatants
            active_combatants = [c for c in self.combatants if c.is_alive() and c.grudge_list] # Changed this line
            print(f"[DEBUG advance_combat_round] Active combatants: {[c.name for c in active_combatants]}")

            # Check hostility
            if not self.has_hostility():
                if self.player_in_room:
                    print(f"[DEBUG advance_combat_round] No hostility remains. Combat ends in Room {self.room_id}.")
                self.end_combat()
                return

            # Calculate initiative for each combatant
            initiative_order = []
            for combatant in active_combatants:
                initiative = combatant._calculate_combat_initiative()
                initiative_order.append((combatant, initiative))
                print(f"[DEBUG advance_combat_round] {combatant.name} (ID: {combatant.id}) initiative: {initiative}")

            # Sort combatants by initiative (highest first)
            initiative_order.sort(key=lambda x: x[1], reverse=True)

            # Process each combatant's turn in initiative order
            for combatant, initiative in initiative_order:
                print(f"[DEBUG advance_combat_round] Processing turn for {combatant.name} (ID: {combatant.id})") # Added debug statement
                # Start of turn effects
                combatant.update_effects_start_of_turn()

                # Skill usage decision, handle ai using healing first
                skill_used = False
                if combatant.monster_type != "player":
                    skill_name = combatant.select_ai_skill(None)
                    if skill_name:
                        if skill_name == "cure_light_wounds":
                            target = combatant
                        else:
                            target = self.select_target(combatant)
                            if target is None:
                                skill_used = False
                                print(f"[DEBUG advance_combat_round] No target found for {combatant.name}, using default attack.")
                                if combatant.can_use_skill("attack"):
                                    target = self.select_target(combatant) # Select target for default attack
                                    if target is not None:
                                        combatant.use_skill("attack", target)
                                        skill_used = True
                                    else:
                                        print(f"[DEBUG advance_combat_round] {combatant.name} (ID: {combatant.id}) does not have the attack skill or no target found.")
                                else:
                                    print(f"[DEBUG advance_combat_round] {combatant.name} failed to use default attack!")
                                continue
                        combatant.use_skill(skill_name, target)
                        skill_used = True

                elif combatant.monster_type == "player":
                    target = self.select_target(combatant)
                    if target is not None: # Check if target exists
                        if combatant.can_use_skill("slash"):
                            combatant.use_skill("slash", target)
                            skill_used = True
                        elif combatant.can_use_skill("double_slash"):
                            combatant.use_skill("double_slash", target)
                            skill_used = True
                        elif combatant.can_use_skill("attack"):
                            combatant.use_skill("attack", target)
                            skill_used = True
                    else:
                        print(f"[DEBUG advance_combat_round] No target found for player, skipping skill usage.")

                if not skill_used:
                    print(f"DEBUG A skill was not used, using default attack for {combatant.name}")
                    target = self.select_target(combatant)
                    if target is not None and combatant.can_use_skill("attack"):
                        combatant.use_skill("attack", target)
                    else:
                        print(f"[DEBUG advance_combat_round] {combatant.name} (ID: {combatant.id}) does not have the attack skill or no target found.")

                # End of turn effects
                print(f"[DEBUG advance_combat_round] Updating end of turn effects for {combatant.name} (ID: {combatant.id})")
                combatant.update_effects_end_of_turn()

                # Remove defeated combatants from grudges
                for target in self.combatants:
                    if not target.is_alive():
                        self.remove_defeated_grudges(target.id)

            # Check victory conditions
            if self.check_victory():
                self.end_combat()


    def add_combatant(self, combatant):
        if combatant in self.combatants:
            print(f"[DEBUG] Combatant {combatant.name} (ID: {combatant.id}) is already in the room. Skipping addition.")
            return
        print(f"[DEBUG] Adding combatant: {combatant.name} (ID: {combatant.id})")
        combatant.current_room = self.room_id
        self.combatants.append(combatant)
        self.make_active() # Make room active when a combatant is added

    def remove_combatant_by_id(self, combatant_id):
        """
        Removes a combatant from the room based on their ID.

        Args:
            combatant_id: The ID of the combatant to remove.
        """
        for combatant in self.combatants:
            if combatant.id == combatant_id:
                print(f"[DEBUG] Removing combatant: {combatant.name} (ID: {combatant.id})")
                self.combatants.remove(combatant)
                combatant.current_room = None  # Optionally reset the combatant's current_room
                return  # Exit after removing the combatant
        self.check_and_deactivate() # Check if room should be deactivated
        print(f"[DEBUG] Combatant with ID {combatant_id} is not in the room. Skipping removal.")



    def add_new_combatant(self, combatant):
        print(f"[DEBUG] A new combatant enters the room: {combatant.name} (ID: {combatant.id})")
        self.add_combatant(combatant)
        self.update_grudges(combatant)


    def detect_hostility(self, turn_manager=None):
        # print("[DEBUG] Detecting hostility...")
        for combatant in self.combatants:
            if combatant.is_alive():
                # Hates everyone
                if combatant.hates_all:
                    for other in self.combatants:
                        if other.id != combatant.id and other.is_alive() and other.name != combatant.name:
                            combatant.add_to_grudge_list(other.id)
                            other.add_to_grudge_list(combatant.id)
                # Hates player and companions
                elif combatant.hates_player_and_companions:
                    for other in self.combatants:
                        if (other.id.startswith("player") or other.id.startswith("companion")) and other.is_alive():
                            combatant.add_to_grudge_list(other.id)
                            other.add_to_grudge_list(combatant.id)
                # Hates specific monster types
                elif combatant.hates:
                    for other in self.combatants:
                        if other.id != combatant.id and other.is_alive() and other.monster_type in combatant.hates:
                            combatant.add_to_grudge_list(other.id)
                            other.add_to_grudge_list(combatant.id)

        # print("[DEBUG] Hostility detection complete.")

        # Debugging: Print combatants and their grudges
        temp = []
        for c in self.combatants:
            # TODO: this might need some fixing
            # print(f"[DEBUG detect_hostility] {c.name} grudges: {c.grudge_list}")
            temp += c.grudge_list
            if len(temp) > 0:
                break
        if temp:
            self.start_combat(0)


    def has_hostility(self): # TODO: this might need some looking into
        print("[DEBUG has_hostility] Checking for hostility among combatants...")
        for combatant in self.combatants:
            # Skip dead combatants
            if not combatant.is_alive():
                # print(f"[DEBUG has_hostility] Skipping {combatant.name} (ID: {combatant.id}) because they are not alive.")
                continue

            # Debug: Print combatant details
            print(f"[DEBUG has_hostility] Combatant: {combatant.name} (ID: {combatant.id}), Alive: {combatant.is_alive()}, Grudge List: {combatant.grudge_list}")
            
            if combatant.grudge_list:  # Check if grudge list exists and is non-empty
                for target_id in combatant.grudge_list:
                    # Debug: Print the target ID being checked
                    print(f"[DEBUG has_hostility] {combatant.name} is hostile toward {target_id}. Checking if target is alive...")
                    
                    # Find the target in the room's combatants
                    target = next((c for c in self.combatants if c.id == target_id and c.is_alive()), None)
                    
                    if target:
                        # Debug: Print details of the alive target
                        print(f"[DEBUG has_hostility] Hostility detected! {combatant.name} has a valid target: {target.name} (ID: {target.id}, Health: {target.stats['health']})")
                        return True
                    else:
                        # Debug: The target is either not found or not alive
                        print(f"[DEBUG has_hostility] Target with ID {target_id} is not alive or not found.")

        # Debug: No hostility detected
        print("[DEBUG has_hostility] No hostility detected. All grudges are either resolved or targets are dead.")
        return False

    def update_grudges(self, new_combatant):
        # Add grudges for the new combatant
        if new_combatant.hates_all:
            for other in self.combatants:
                if other.id != new_combatant.id and other.is_alive():
                    new_combatant.add_to_grudge_list(other.id)
                    other.add_to_grudge_list(new_combatant.id)
        elif new_combatant.hates_player_and_companions:
            for other in self.combatants:
                if (other.id.startswith("player") or other.id.startswith("companion")) and other.is_alive():
                    new_combatant.add_to_grudge_list(other.id)
                    other.add_to_grudge_list(new_combatant.id)
        elif new_combatant.hates:
            for other in self.combatants:
                if other.id != new_combatant.id and other.is_alive() and other.monster_type in new_combatant.hates:
                    new_combatant.add_to_grudge_list(other.id)
                    other.add_to_grudge_list(new_combatant.id)

        # Update existing combatants' grudges to reflect the presence of the new combatant
        for combatant in self.combatants:
            if combatant.id != new_combatant.id and combatant.is_alive():
                if combatant.hates_all:
                    combatant.add_to_grudge_list(new_combatant.id)
                elif combatant.hates_player_and_companions and (new_combatant.id.startswith("player") or new_combatant.id.startswith("companion")):
                    combatant.add_to_grudge_list(new_combatant.id)
                elif combatant.hates and new_combatant.monster_type in combatant.hates:
                    combatant.add_to_grudge_list(new_combatant.id)


    def start_combat(self, current_turn):
        self.in_combat = True
        self.combat_start_turn = current_turn
        self.combat_rounds = 0  # Initialize combat rounds
        print(f"Combat begins in Room {self.room_id} on Turn {current_turn}!")


    def end_combat(self):
        self.in_combat = False
        self.combat_start_turn = 0
        self.combat_rounds = 0
        self.check_and_deactivate() # Check if room should be deactivated
        print(f"Combat ends in Room {self.room_id}.")

    def remove_defeated_grudges(self, defeated_id):
        # print(f"[DEBUG] Removing {defeated_id} from all grudge lists")
        for combatant in self.combatants:
            if defeated_id in combatant.grudge_list:
                combatant.grudge_list.remove(defeated_id)

    def select_target(self, attacker):
        # print(f"[DEBUG] Selecting target for {attacker.name} (ID: {attacker.id})")
        # Filter grudge list for alive targets
        valid_targets = [combatant for combatant in self.combatants if combatant.id in attacker.grudge_list and combatant.is_alive()]
        
        # Debugging: Show grudge list and valid targets
        # print(f"[DEBUG] {attacker.name}'s grudge list: {attacker.grudge_list}")
        # print(f"[DEBUG] Valid targets for {attacker.name}: {[t.name for t in valid_targets]}")
        
        return random.choice(valid_targets) if valid_targets else None


    def check_victory(self):
        active_grudges = False
        for combatant in self.combatants:
            if len(combatant.grudge_list) > 0:
                active_grudges = True
                break
        if active_grudges == False:
            print("No active grudges. Combat ends.")
            return True

        # if not any(c.is_alive() for c in self.combatants if c.id.startswith("player")):
        #     print("[DEBUG] The player has been defeated! Game Over.")
        #     return True
        # if not any(c.is_alive() for c in self.combatants if c.id.startswith("player")):
        #     print("[DEBUG] All monsters are defeated! Combat ends.")
        #     return True
        # return False
    
    def trigger_reinforcements(self):
        from game.combatants import Monster
        reinforcement_data = {
            "name": "Reinforcement Goblin",
            "health": 50,
            "attack": 10,
            "defense": 5,
            "hates_player_and_companions": True,
            "hates": ["animal"],
            "monster_type": "goblin"
        }
        new_goblin = Monster("goblin", reinforcement_data)
        print(f"[DEBUG] Reinforcements arrived! {new_goblin.name} joins the battle.")
        self.add_new_combatant(new_goblin)

    def spawn_monsters(self, monster_types):
        from game.helper_functions import create_creature
        """
        Spawns monsters based on the given monster_types.
        :param monster_types: Either a string (single monster type) or a list of strings (multiple monster types).
        """
        # Ensure monster_types is always treated as a list, even if it's a single string
        if isinstance(monster_types, str):
            monster_types = [monster_types]

        # Iterate over the list of monster types and spawn each monster
        for monster_type in monster_types:
            if monster_type not in combatant_data.creature_data.keys():
                raise ValueError(f"Creature type '{monster_type}' does not exist in creature_data.")
            
            # Create and add the monster to combatants
            monster = create_creature(
                creature_type=monster_type,
                creature_data=combatant_data.creature_data,
                creature_traits=combatant_data.creature_traits_data,
                status_data=combatant_data.creature_status_data,
                level=5
                # selected_traits=selected_traits_for_dragon # Would need to use default traits or maybe random ones
            )
            self.add_combatant(monster)