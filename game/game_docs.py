#
# === Standalone Functions by Module ===
#
# helper_functions.py
#   initialize_game
#     """
#     Description: Initializes the game world, player, and all starting state. Sets up rooms, combatants, and context.
#     Arguments: None
#     Output: Tuple (player, room_manager, movement_manager, turn_manager, companion, game_context)
#     """
#   create_companion
#     """
#     Description: Creates a new companion character with default or specified attributes.
#     Arguments: name (str), skills (dict, optional)
#     Output: Companion object
#     """
#   create_player
#     """
#     Description: Creates a new player character with default or specified attributes.
#     Arguments: name (str), skills (dict, optional)
#     Output: Player object
#     """
#   create_creature
#     """
#     Description: Creates a new generic creature (monster or NPC) with specified attributes.
#     Arguments: name (str), health (int), skills (dict, optional)
#     Output: Combatant object
#     """
#   remove_creature_by_id
#     """
#     Description: Removes a creature from the game by its unique ID.
#     Arguments: creature_id (str), room_manager (RoomManager)
#     Output: None
#     """
#   generate_internal_connections
#     """
#     Description: Generates internal connections between rooms in a cluster for navigation.
#     Arguments: room_cluster (list of Room)
#     Output: None (modifies room_cluster in place)
#     """
#   create_room_cluster
#     """
#     Description: Creates a group of interconnected rooms as a cluster.
#     Arguments: num_rooms (int), base_name (str)
#     Output: List of Room objects
#     """
#   create_cluster_command
#     """
#     Description: Command function to create a new room cluster via user input or parameters.
#     Arguments: args (list), room_manager (RoomManager)
#     Output: None (modifies room_manager)
#     """
#   create_cluster_command_wrapper
#     """
#     Description: Wraps the cluster creation command for use in command dispatch or UI.
#     Arguments: *args, **kwargs
#     Output: None
#     """
#   clear_screen
#     """
#     Description: Clears the terminal or console screen for better readability.
#     Arguments: None
#     Output: None (side effect: clears screen)
#     """
#   use_skill_command
#     """
#     Description: Handles the use of a skill by a player or combatant, processing input and applying effects.
#     Arguments: skill_name (str), user (Combatant), target (Combatant)
#     Output: None (applies skill effects)
#     """
#   toggle_pause
#     """
#     Description: Toggles the paused state of the game (e.g., for timers or input threads).
#     Arguments: turn_manager
#     Output: Prints pause state to console.
#     """
#
# input_thread.py
#   load_game
#     """
#     Description: Loads a saved game state from disk, restoring the game context and managers.
#     Arguments: filename (str), player (Player)
#     Output: Restored TurnManager instance or None if loading fails.
#     """
#   input_thread
#     """
#     Description: Runs a background thread to handle user input asynchronously during gameplay.
#     Arguments: 
#     Output: None (runs input loop in thread)
#     """
#   quit_game
#     """
#     Description: Handles quitting the game
#     Arguments: 
#     Output:
#     """
#   load_game_with_player_transfer
#     """
#     Description: Loads a saved game and transfers the player object to the new context, preserving player state.
#     Arguments: filename (str), player (Player)
#     Output: Restored TurnManager instance with transferred player, or None if loading fails.
#     """

# === Class and Method Names by Module ===

# combatants.py
#   Combatant
#     to_dict
#       """
#       Description: Serializes the Combatant's state to a dictionary for saving.
#       Arguments: None (uses instance attributes)
#       Output: dict representing the Combatant state.
#       """
#     from_dict
#       """
#       Description: Deserializes a Combatant from a dictionary, restoring all attributes.
#       Arguments: data (dict)
#       Output: Combatant instance.
#       """
#     _update_cached_stats
#       """
#       Description: Updates cached/computed stats (e.g., health, initiative) based on current state and effects.
#       Arguments: None (uses instance attributes)
#       Output: None (updates internal state)
#       """
#     select_ai_skill
#       """
#       Description: Selects a skill for AI-controlled combatants to use during their turn.
#       Arguments: target (Combatant)
#       Output: skill_name (str)
#       """
#     level_up_skill
#       """
#       Description: Increases the level of a specified skill for the combatant.
#       Arguments: skill_name (str)
#       Output: None (modifies skills)
#       """
#     _calculate_stats
#       """
#       Description: Calculates and updates the combatant's stats (e.g., attack, defense) from base values and effects.
#       Arguments: None (uses instance attributes)
#       Output: None (updates internal state)
#       """
#     describe_stats
#       """
#       Description: Returns a string describing the combatant's current stats and status.
#       Arguments: None
#       Output: str summary of stats.
#       """
#     is_alive
#       """
#       Description: Checks if the combatant is alive (health > 0).
#       Arguments: None
#       Output: bool (True if alive, False otherwise)
#       """
#     add_to_grudge_list
#       """
#       Description: Adds another combatant to this combatant's grudge list (for targeting/AI).
#       Arguments: other (Combatant)
#       Output: None (modifies grudge list)
#       """
#     add_skill
#       """
#       Description: Adds a new skill to the combatant's skill set.
#       Arguments: skill_name (str), level (int)
#       Output: None (modifies skills)
#       """
#     add_passive_skill
#       """
#       Description: Adds a passive skill to the combatant, granting ongoing effects.
#       Arguments: skill_name (str), effect (Effect)
#       Output: None (modifies passive skills)
#       """
#     can_use_skill
#       """
#       Description: Checks if the combatant can use a specified skill (e.g., has enough resources, not silenced).
#       Arguments: skill_name (str)
#       Output: bool (True if usable, False otherwise)
#       """
#     use_skill
#       """
#       Description: Uses a skill against a target, applying effects and calculating results.
#       Arguments: skill_name (str), target (Combatant)
#       Output: None (applies skill effects)
#       """
#     _calculate_damage
#       """
#       Description: Calculates the damage dealt by this combatant to a target, factoring in skills and effects.
#       Arguments: target (Combatant), skill_name (str)
#       Output: int (damage amount)
#       """
#     heal
#       """
#       Description: Restores health to the combatant, up to max health.
#       Arguments: amount (int)
#       Output: None (modifies health)
#       """
#     _calculate_combat_initiative
#       """
#       Description: Calculates the combatant's initiative for turn order in combat.
#       Arguments: None
#       Output: int (initiative value)
#       """
#     _apply_effect
#       """
#       Description: Applies an effect (buff/debuff) to the combatant.
#       Arguments: effect (Effect)
#       Output: None (modifies effects)
#       """
#     take_damage
#       """
#       Description: Reduces the combatant's health by a specified amount, applying any relevant effects.
#       Arguments: amount (int), source (Combatant, optional)
#       Output: None (modifies health)
#       """
#     update_effects_start_of_turn
#       """
#       Description: Updates all effects on the combatant at the start of their turn (e.g., poison ticks).
#       Arguments: None
#       Output: None (modifies effects)
#       """
#     update_effects_end_of_turn
#       """
#       Description: Updates all effects on the combatant at the end of their turn (e.g., duration reduction).
#       Arguments: None
#       Output: None (modifies effects)
#       """

#   Player(Combatant)
#     to_dict
#       """
#       Description: Serializes the Player's state to a dictionary for saving, including player-specific attributes.
#       Arguments: None (uses instance attributes)
#       Output: dict representing the Player state.
#       """
#     from_dict
#       """
#       Description: Deserializes a Player from a dictionary, restoring all player-specific attributes.
#       Arguments: data (dict)
#       Output: Player instance.
#       """

#   Companion(Combatant)
#     to_dict
#       """
#       Description: Serializes the Companion's state to a dictionary for saving, including companion-specific attributes.
#       Arguments: None (uses instance attributes)
#       Output: dict representing the Companion state.
#       """
#     from_dict
#       """
#       Description: Deserializes a Companion from a dictionary, restoring all companion-specific attributes.
#       Arguments: data (dict)
#       Output: Companion instance.
#       """

#   Monster(Combatant)
#     _apply_selected_traits
#       """
#       Description: Applies selected traits to the Monster, modifying stats and abilities accordingly.
#       Arguments: None (uses selected_traits)
#       Output: None (modifies internal state)
#       """
#     describe
#       """
#       Description: Returns a string describing the Monster, including traits and status.
#       Arguments: None
#       Output: str summary of monster traits and status.
#       """
#     to_dict
#       """
#       Description: Serializes the Monster's state to a dictionary for saving, including monster-specific attributes.
#       Arguments: None (uses instance attributes)
#       Output: dict representing the Monster state.
#       """
#     from_dict
#       """
#       Description: Deserializes a Monster from a dictionary, restoring all monster-specific attributes.
#       Arguments: data (dict)
#       Output: Monster instance.
#       """

# room.py
#   Room
#     to_dict
#       """
#       Description: Serializes the Room's state to a dictionary for saving, including connections and combatants.
#       Arguments: None (uses instance attributes)
#       Output: dict representing the Room state.
#       """
#     from_dict
#       """
#       Description: Deserializes a Room from a dictionary, restoring all room attributes and connections.
#       Arguments: data (dict), room_lookup (dict)
#       Output: Room instance.
#       """
#     make_active
#       """
#       Description: Marks the room as active for turn processing or combat.
#       Arguments: None
#       Output: None (modifies room state)
#       """
#     check_and_deactivate
#       """
#       Description: Checks if the room should be deactivated (e.g., no combatants remain) and deactivates if needed.
#       Arguments: None
#       Output: None (modifies room state)
#       """
#     connect
#       """
#       Description: Connects this room to another room in a specified direction.
#       Arguments: direction (str), other_room (Room)
#       Output: None (modifies connections)
#       """
#     available_directions
#       """
#       Description: Returns a list of available directions (exits) from this room.
#       Arguments: None
#       Output: list of str (directions)
#       """
#     advance_turn
#       """
#       Description: Advances the room's state by one turn, updating effects and combat.
#       Arguments: current_turn (int)
#       Output: None (modifies room state)
#       """
#     on_turn_advanced
#       """
#       Description: Called when the global turn advances; updates room-specific state.
#       Arguments: current_turn (int)
#       Output: None (modifies room state)
#       """
#     advance_combat_round
#       """
#       Description: Advances the combat round for all combatants in the room.
#       Arguments: None
#       Output: None (modifies combat state)
#       """
#     add_combatant
#       """
#       Description: Adds a combatant to the room.
#       Arguments: combatant (Combatant)
#       Output: None (modifies room state)
#       """
#     remove_combatant_by_id
#       """
#       Description: Removes a combatant from the room by their unique ID.
#       Arguments: combatant_id (str)
#       Output: None (modifies room state)
#       """
#     add_new_combatant
#       """
#       Description: Adds a new combatant to the room, initializing any necessary state.
#       Arguments: combatant (Combatant)
#       Output: None (modifies room state)
#       """
#     detect_hostility
#       """
#       Description: Detects if there is hostility between any combatants in the room.
#       Arguments: None
#       Output: bool (True if hostility detected, False otherwise)
#       """
#     has_hostility
#       """
#       Description: Checks if the room currently has any hostile combatants.
#       Arguments: None
#       Output: bool (True if hostility present, False otherwise)
#       """
#     update_grudges
#       """
#       Description: Updates grudge lists for all combatants in the room.
#       Arguments: None
#       Output: None (modifies combatant state)
#       """
#     start_combat
#       """
#       Description: Initiates combat between hostile combatants in the room.
#       Arguments: None
#       Output: None (modifies combat state)
#       """
#     end_combat
#       """
#       Description: Ends combat in the room, resetting combatant states as needed.
#       Arguments: None
#       Output: None (modifies combat state)
#       """
#     remove_defeated_grudges
#       """
#       Description: Removes defeated combatants from all grudge lists in the room.
#       Arguments: None
#       Output: None (modifies grudge lists)
#       """
#     select_target
#       """
#       Description: Selects a target for a combatant in the room, based on hostility and AI.
#       Arguments: combatant (Combatant)
#       Output: target (Combatant)
#       """
#     check_victory
#       """
#       Description: Checks if a victory condition has been met in the room (e.g., all enemies defeated).
#       Arguments: None
#       Output: bool (True if victory, False otherwise)
#       """
#     trigger_reinforcements
#       """
#       Description: Triggers reinforcements to enter the room, adding new combatants.
#       Arguments: None
#       Output: None (modifies room state)
#       """
#     spawn_monsters
#       """
#       Description: Spawns new monsters in the room, initializing their state and adding them to combat.
#       Arguments: num_monsters (int)
#       Output: None (modifies room state)
#       """

# helper_functions.py
#   CommandCompleter
#     get_completions
#       # Description: Yields possible command completions for the prompt_toolkit UI based on user input.
#       # Arguments: document (Document), complete_event (CompleteEvent)
#       # Output: Yields Completion objects for matching commands.

# managers.py
#   PlayerActionManager
#     look
#       # Description: Displays the current room's long description, available exits, and any combatants present.
#       # Arguments: None (uses self.player and self.room_manager)
#       # Output: Prints styled room info to the console.
#     exits
#       # Description: Lists all exits (directions) from the player's current room.
#       # Arguments: None (uses self.player and self.room_manager)
#       # Output: Prints a comma-separated list of exits.

#   RoomManager
#     to_dict
#       # Description: Serializes all rooms and active room IDs to a dictionary for saving.
#       # Arguments: None (uses self.game_rooms and self.active_room_lookup)
#       # Output: Returns a dictionary representing the RoomManager state.
#     from_dict
#       # Description: Deserializes a RoomManager from saved data, reconstructing rooms and lookups.
#       # Arguments: data (dict) - the saved RoomManager data
#       # Output: Returns a RoomManager instance.
#     add_room
#       # Description: Registers a new Room object and adds it to the manager's lookups.
#       # Arguments: room (Room) - the room to add
#       # Output: None
#     add_room_active
#       # Description: Marks a room as active (e.g., for turn processing or combat).
#       # Arguments: room (Room) - the room to mark as active
#       # Output: None
#     remove_room_active
#       # Description: Removes a room from the active rooms dictionary.
#       # Arguments: room_id (str) - the ID of the room to remove
#       # Output: None
#     create_and_connect_rooms
#       # Description: Handles user input or test mode to create and connect multiple rooms dynamically.
#       # Arguments: starting_room (Room), test_mode (bool), num_rooms_to_create (int)
#       # Output: None
#     get_room_info
#       # Description: Prints detailed information about a room, including name, ID, and exits.
#       # Arguments: None (uses self.player and self.room_lookup)
#       # Output: Prints room info to the console.
#     on_turn_advanced
#       # Description: Calls on_turn_advanced for all rooms, advancing their state each turn.
#       # Arguments: current_turn (int)
#       # Output: None
#     generate_map
#       # Description: Generates and prints a visual map of the current room layout.
#       # Arguments: size (int), search_depth (int)
#       # Output: Prints the map to the console.
#     remove_room_by_id
#       # Description: Removes a room and cleans up all references to it in the game.
#       # Arguments: room_id_to_remove (str)
#       # Output: None

#   MovementManager
#     move_player
#       # Description: Moves the player to another room in the specified direction, updating state and triggering events.
#       # Arguments: player (Player), direction (str)
#       # Output: Returns True if movement succeeded, False otherwise. Prints results and updates state.
#     move_player_command
#       # Description: Handles the move command, calling move_player and printing results/errors.
#       # Arguments: direction (str), player (Player)
#       # Output: None
#     to_dict
#       # Description: Serializes movement manager state (room and player IDs) for saving.
#       # Arguments: None (uses self.room_manager and self.player)
#       # Output: Returns a dictionary representing the MovementManager state.
#     from_dict
#       # Description: Deserializes a MovementManager from saved data, linking to room and player.
#       # Arguments: data (dict), room_manager (RoomManager), player (Player)
#       # Output: Returns a MovementManager instance.

#   TurnManager
#     advance_turn
#       # Description: Advances the global turn counter and notifies all active rooms to update their state.
#       # Arguments: None (uses self.current_turn and self.room_manager)
#       # Output: Increments turn, prints debug info, and updates rooms.
#     start_timer
#       # Description: Starts a background timer thread to auto-advance turns at intervals, respecting pause/stop events.
#       # Arguments: interval_seconds (float)
#       # Output: None (spawns a thread)
#     to_dict
#       # Description: Serializes the turn manager, including current turn, room manager, and movement manager.
#       # Arguments: None (uses self.current_turn, self.room_manager, self.movement_manager)
#       # Output: Returns a dictionary representing the TurnManager state.
#     from_dict
#       # Description: Deserializes a TurnManager from saved data, restoring all state.
#       # Arguments: data (dict)
#       # Output: Returns a TurnManager instance.

#   CombatantManager
#     get_active_effects
#       # Description: Returns a string listing all currently active effects (buffs/debuffs) with durations and strengths.
#       # Arguments: effects (dict) - the effects to summarize
#       # Output: String summary of active effects.
#     describe_traits
#       # Description: Returns a string describing all selected traits for the combatant.
#       # Arguments: None (uses self.selected_traits)
#       # Output: String summary of traits.
#     add_buff
#       # Description: Adds or updates a buff, increasing its duration/strength and updating power.
#       # Arguments: buff_key (str), duration (int), strength (int)
#       # Output: None (updates state and prints debug info)
#     remove_buff
#       # Description: Removes a buff and updates power.
#       # Arguments: buff_key (str)
#       # Output: None (updates state and prints debug info)
#     decrement_buff_durations
#       # Description: Decreases the duration of all buffs, removing any that expire.
#       # Arguments: None (operates on self.buffs)
#       # Output: None
#     add_debuff
#       # Description: Adds or updates a debuff, increasing its duration/strength.
#       # Arguments: debuff_key (str), duration (int), strength (int)
#       # Output: None (updates state and prints debug info)
#     remove_debuff
#       # Description: Removes a debuff.
#       # Arguments: debuff_key (str)
#       # Output: None (updates state and prints debug info)
#     decrement_debuff_durations
#       # Description: Decreases the duration of all debuffs, removing any that expire.
#       # Arguments: None (operates on self.debuffs)
#       # Output: None
#     describe_status
#       # Description: Returns a string summary of all current buffs and debuffs.
#       # Arguments: None (uses self.buffs and self.debuffs)
#       # Output: String summary of buffs and debuffs.

#   SaveLoadManager
#     save_to_file
#       # Description: Prompts the user for a filename and saves the current game state to disk as JSON.
#       # Arguments: turn_manager (TurnManager)
#       # Output: None (writes to disk, prints debug info)
#     load_from_file
#       # Description: Prompts the user to select a save file and loads the game state from disk.
#       # Arguments: player (Player)
#       # Output: Returns a TurnManager instance loaded from file, or None if cancelled.

# game_context.py
#   GameContext
#     initialize
#       # Description: Calls the game initialization routine and stores the result in the context.
#       # Arguments: None (uses helper_functions.initialize_game)
#       # Output: Sets self.start_game to the initialized game state.

# effects.py
#   Effect
#     apply
#       # Description: Applies the effect to a target, calling any on_apply callback if present.
#       # Arguments: target (Combatant)
#       # Output: None (may modify target state)
#     remove
#       # Description: Removes the effect from a target, calling any on_remove callback if present.
#       # Arguments: target (Combatant)
#       # Output: None (may modify target state)
#     turn_start
#       # Description: Called at the start of the target's turn; can apply periodic effects (e.g., poison).
#       # Arguments: target (Combatant)
#       # Output: None (may modify target state)
#     damage_taken
#       # Description: Called when the target takes damage, for effect-triggered logic.
#       # Arguments: target (Combatant), damage (int)
#       # Output: None (may modify target state)
#     damage_dealt
#       # Description: Called when the target deals damage, for effect-triggered logic.
#       # Arguments: target (Combatant), damage (int)
#       # Output: None (may modify target state)
#     to_dict
#       # Description: Serializes the effect for saving.
#       # Arguments: None (uses effect attributes)
#       # Output: Returns a dictionary representing the Effect state.
#     from_dict
#       # Description: Deserializes an effect from saved data.
#       # Arguments: data (dict)
#       # Output: Returns an Effect instance.
