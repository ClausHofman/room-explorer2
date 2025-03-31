from game.effects import Effect

class Combatant:
    def __init__(self, combatant_id, name, base_stats, level, hates_all=False, hates_player_and_companions=False, hates=None, monster_type=None):
        self.id = combatant_id
        self.name = name
        self.base_stats = base_stats
        self.level = level
        self.hates_all = hates_all
        self.hates_player_and_companions = hates_player_and_companions
        self.hates = hates or []
        self.monster_type = monster_type
        self.grudge_list = []
        self.current_room = None
        self.skills = {
            "offensive_melee": {},
            "passive_defense": {},
            "passive_offense": {},
            "general": {},
            "restoration_magic": {},
            "defensive_magic": {},
            "effects": {}
        }
        self.effects = []
        self.stats = self._calculate_stats()
        self._max_health = self._calculate_stats()["health"]
        self._cached_stats = self._calculate_stats()
        


    # Serialization method
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "stats": self.stats,
            "level": self.level,
            "hates_all": self.hates_all,
            "hates_player_and_companions": self.hates_player_and_companions,
            "hates": self.hates,
            "monster_type": self.monster_type,
            "grudge_list": self.grudge_list,
            "current_room": self.current_room,
            "skills": self.skills,
            "grudge_list": self.grudge_list,
            "status_effect": {
                "buffs": self.combatant_manager.buffs if self.combatant_manager and isinstance(self.combatant_manager.buffs, dict) else {},
                "debuffs": self.combatant_manager.debuffs if self.combatant_manager and isinstance(self.combatant_manager.debuffs, dict) else {}
            }            
        }

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        # print(f"[DEBUG COMBATANT.PY] data in from_dict: {data}")

        base_stats = {
                    "health": data["stats"]["health"],
                    "spell_points": data["stats"]["spell_points"],
                    "attack": data["stats"]["attack"],
                    "defense": data["stats"]["defense"],
                    "strength": data["stats"]["strength"],
                    "dexterity": data["stats"]["dexterity"],
                    "intelligence": data["stats"]["intelligence"],
                    "wisdom": data["stats"]["wisdom"],
                    "willpower": data["stats"]["willpower"],
                    "constitution": data["stats"]["constitution"],
                    "level": data.get("level", 1),
                    "health_per_level": data.get("health_per_level", 0),
                    "spell_points_per_level": data.get("spell_points_per_level", 0),
                    "health_per_constitution": data.get("health_per_constitution", 0),
                    "damage_per_strength": data.get("damage_per_strength", 0),
                    "spell_points_per_intelligence": data.get("spell_points_per_intelligence", 0),
                    "defense_per_constitution": data.get("defense_per_constitution", 0)
                    }
        print(f"[DEBUG from_dict base_stats] {data['name']} base_stats: {base_stats}")
        status_effects = data.get("status_effect", {"buffs": {}, "debuffs": {}}) # TODO: Check this

        instance = cls(
            combatant_id=data["id"],
            name=data["name"],
            base_stats = base_stats,
            level=data.get("level", 1),
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None),
        )
        instance.grudge_list = data.get("grudge_list", [])
        print(f"[DEBUG from_dict] {data['name']} base_stats: {base_stats}")
        instance.current_room = data.get("current_room", None)
        instance.stats = data.get("stats", instance.stats)
        instance.skills = data.get("skills", instance.skills)
        instance.grudge_list = data.get("grudge_list", instance.grudge_list)
        
        return instance

    def _update_cached_stats(self):
        cached_stats = self._calculate_stats()
        self._cached_stats = cached_stats
        self._max_health = cached_stats["health"]

    def select_ai_skill(self, target):
        """
        Selects a skill for the AI to use based on its health, skills, and aggression.

        Args:
            target: The target of the skill.

        Returns:
            The name of the skill to use (string), or None if no skill is chosen.
        """
        import random

        # Check if the AI should prioritize defensive magic
        if self.stats["spell_points"] > self._cached_stats["spell_points"] * 0.8 or self.stats["health"] < self._cached_stats["health"] * 0.8:
            # Check for available defensive magic skills
            available_defensive_skills = [
                skill_name
                for skill_name in self.skills.get("defensive_magic", {})
                if self.can_use_skill(skill_name)
            ]
            if available_defensive_skills:
                # TODO: The check if the current spell is active doesn't seem to be working and the combatant will use the spell even when there still should be duration left, but I'll have to double check this
                # Check if any of the defensive skills are already active
                for skill_name in available_defensive_skills:
                    skill_data = self.skills["defensive_magic"][skill_name]
                    if skill_name == "magic_shield":
                        if not any(effect.name == "magic_shield_effect" for effect in self.effects):
                            return skill_name  # Use the skill if its effect is not active
                # If all defensive skills are active, do not use any defensive skill
                print(f"[DEBUG select_ai_skill] All defensive skills are active for {self.name}, skipping defensive skill usage.")


        # Determine the needed skill category
        needed_category = None
        # max_health = self._cached_stats["max_health"]
        if self.stats["health"] < self._max_health * 0.6:
            needed_category = "restoration_magic"

        # If no specific category is needed, default to an offensive category
        if needed_category is None:
            if self.monster_type in ["dragon", "goblin", "wolf"]:
                needed_category = "offensive_melee"
            elif self.monster_type == "companion":
                needed_category = "offensive_melee"

        # If there is a needed category, try to use a skill from it
        if needed_category:
            available_skills_in_category = [
                skill_name
                for skill_name in self.skills.get(needed_category, {})
                if self.can_use_skill(skill_name)
            ]
            if available_skills_in_category:
                # Only heal self if needed
                if needed_category == "restoration_magic":
                    return "cure_light_wounds"
                else:
                    return random.choice(available_skills_in_category)

        # If no skill was chosen, return None
        return None

    def level_up_skill(self, skill_name):
        """Increases the level of a specific skill."""
        skill_data = None
        skill_category = None
        for category in self.skills:
            if skill_name in self.skills[category]:
                skill_data = self.skills[category][skill_name]
                skill_category = category
                break

        if skill_data is None:
            print(f"{self.name} does not have the skill {skill_name}.")
            return False

        if "level" not in skill_data:
            print(f"Skill {skill_name} does not have a level attribute.")
            return False

        skill_data["level"] += 1
        print(f"{self.name}'s skill {skill_name} has leveled up to level {skill_data['level']}!")
        self._update_cached_stats()
        return True

    def _calculate_stats(self):
        """Calculates the combatant's stats based on base stats, level, and scaling rules."""
        stats = {
            "health": self.base_stats["health"],
            "spell_points": self.base_stats["spell_points"] if "spell_points" in self.base_stats else self.base_stats["intelligence"] + self.base_stats["wisdom"] + self.base_stats["willpower"],
            "attack": self.base_stats["attack"],
            "defense": self.base_stats["defense"],
            "strength": self.base_stats["strength"],
            "dexterity": self.base_stats["dexterity"],
            "wisdom": self.base_stats["wisdom"],
            "intelligence": self.base_stats["intelligence"],
            "willpower": self.base_stats["willpower"],
            "constitution": self.base_stats["constitution"],
        }

        # Apply level-based scaling
        if "health_per_level" in self.base_stats:
            stats["health"] += self.base_stats["health_per_level"] * (self.level - 1)
        if "spell_points_per_level" in self.base_stats:
            stats["spell_points"] += self.base_stats["spell_points_per_level"] * (self.level - 1)

        # Apply stat-based scaling
        if "health_per_constitution" in self.base_stats:
            stats["health"] += self.base_stats["health_per_constitution"] * self.base_stats["constitution"]
        if "damage_per_strength" in self.base_stats:
            stats["attack"] += self.base_stats["damage_per_strength"] * self.base_stats["strength"]
        if "spell_points_per_intelligence" in self.base_stats:
            stats["spell_points"] += self.base_stats["spell_points_per_intelligence"] * self.base_stats["intelligence"]
        if "defense_per_constitution" in self.base_stats:
            stats["defense"] += self.base_stats["defense_per_constitution"] * self.base_stats["constitution"]

        # print(f"[DEBUG _calculate_stats]   stats: {stats}")
        return stats

    def describe_stats(self):
        """Returns a string describing the combatant's stats and skills."""
        stats_descriptions = [
            f"- health: {self._cached_stats['health']}",
            f"- attack: {self._cached_stats['attack']}",
            f"- defense: {self._cached_stats['defense']}",
            f"- strength: {self._cached_stats['strength']}",
            f"- dexterity: {self._cached_stats['dexterity']}",
            f"- intelligence: {self._cached_stats['intelligence']}",
            f"- wisdom: {self._cached_stats['wisdom']}",
            f"- willpower: {self._cached_stats['willpower']}",
            f"- constitution: {self._cached_stats['constitution']}",
            f"- spell_points: {self._cached_stats['spell_points']}"
        ]

        # Describe skills
        skill_descriptions = []
        for category, skills in self.skills.items():
            if skills:  # Only add category if it has skills
                skill_descriptions.append(f"  {category.replace('_', ' ').title()}:")
                for skill_name, skill_data in skills.items():
                    skill_level = skill_data.get("level", 1)  # Get the skill's level, default to 1
                    skill_descriptions.append(f"    - {skill_name} (Level {skill_level}): {skill_data.get('description', 'No description available')}")

        return (
            f"{self.name}'s stats:\n"
            + "\n".join(stats_descriptions)
            + "\n\n"
            + f"{self.name}'s Skills:\n"
            + "\n".join(skill_descriptions)
        )

    def is_alive(self):
            return self._cached_stats["health"] > 0

    def add_to_grudge_list(self, attacker_id):
        if attacker_id not in self.grudge_list:
            self.grudge_list.append(attacker_id)
            # print(f"[DEBUG] {self.name} adds {attacker_id} to grudge list")

    # Skills
    def add_skill(self, skill_category, skill_name, skill_data, initial_level=1):
        """Adds a skill to the combatant's repertoire under a specific category."""
        if skill_category not in self.skills:
            raise ValueError(f"Invalid skill category: {skill_category}")
        
        # Add the initial_level to the skill data
        skill_data_with_level = skill_data.copy()
        # Check if the skill has a level defined in available_skills
        if "level" in skill_data:
            skill_data_with_level["level"] = skill_data["level"]
        else:
            skill_data_with_level["level"] = initial_level
        skill_data_with_level["current_cooldown"] = 0
        if "cooldown" in skill_data:
            skill_data_with_level["cooldown"] = skill_data["cooldown"]
        
        self.skills[skill_category][skill_name] = skill_data_with_level
        self._update_cached_stats()

    def add_passive_skill(self, skill_category, skill_name, skill_data, initial_level=1):
        """Adds a passive skill to the combatant's repertoire under a specific category."""
        if skill_category not in self.skills:
            raise ValueError(f"Invalid skill category: {skill_category}")
        
        # Add the initial_level to the skill data
        skill_data_with_level = skill_data.copy()
        skill_data_with_level["level"] = initial_level
        
        self.skills[skill_category][skill_name] = skill_data_with_level
        self._update_cached_stats()

    def can_use_skill(self, skill_name):
        """Checks if a skill is available for use."""
        # Check if the skill exists in any category
        for category in self.skills:
            if skill_name in self.skills[category]:
                skill_data = self.skills[category][skill_name]
                return skill_data["current_cooldown"] == 0
        return False

    def use_skill(self, skill_name, target):
        """Uses a skill on a target."""
        from game.available_skills import available_skills
        # Find the skill in any category
        skill_data = None
        for category in self.skills:
            if skill_name in self.skills[category]:
                skill_data = self.skills[category][skill_name]
                break

        if skill_data is None:
            print(f"{self.name} does not have the skill {skill_name}.")
            return False

        if skill_data["current_cooldown"] > 0:
            print(f"{self.name} cannot use {skill_name} because it's on cooldown.")
            return False

        print(f"{self.name} uses {skill_name} on {target.name}!")

        if skill_name in available_skills["effects_skills"]:
            print(f"DEBUG CAST SPELL: {self.name} casts a {skill_name} on {target.name}!")
            self._apply_effect(skill_name, target)

        elif "base_damage" in skill_data: # Check if it's a damaging skill
            print(f"[DEBUG] {self.name} (ID: {self.id}) is using {skill_name} on {target.name} (ID: {target.id})")
            print(f"[DEBUG] {skill_name} base damage: {skill_data.get('base_damage', 0)}")
            if skill_data.get("stat_scaling"):
                print(f"[DEBUG] {skill_name} scaling stat: {skill_data.get('stat_scaling')}, scaling value: {self.stats.get(skill_data.get('stat_scaling'))}")
            if skill_data.get("flat_stat_scaling"):
                print(f"[DEBUG] {skill_name} flat scaling stat: {skill_data.get('flat_stat_scaling')}, scaling value: {self.stats.get(skill_data.get('flat_stat_scaling'))}")
            target.take_damage(skill_data.get("base_damage", 0), "physical", self, skill_data)

        elif "base_heal" in skill_data:
            base_heal = skill_data.get("base_heal", 0)
            if "stat_scaling" in skill_data["scaling_rules"]:
                scaling_stat = skill_data["scaling_rules"]["stat_scaling"]
                if scaling_stat in self.stats:
                    scaling_value = self.stats[scaling_stat]
                    base_heal = int(base_heal * (1 + (scaling_value / 10)))
            if "level_scaling_factor" in skill_data["scaling_rules"]:
                level_scaling_factor = skill_data["scaling_rules"]["level_scaling_factor"]
                base_heal = int(base_heal * (1 + (self.level * level_scaling_factor)))
            if "level" in skill_data:
                skill_level = skill_data["level"]
                base_heal = int(base_heal * (1 + (skill_level / 10)))
            target.heal(base_heal)

        if "effects" in skill_data:
            for effect_name in skill_data["effects"]:
                self._apply_effect(effect_name, target)

        if "cooldown" in skill_data:
            skill_data["current_cooldown"] = skill_data["cooldown"]

        return True

    def _calculate_damage(self, damage, damage_type, attacker=None, skill_data=None):
        """
        Calculates the final damage after applying various modifiers.

        Args:
            damage (int): The base damage value.
            damage_type (str): The type of damage (e.g., "physical", "magical", "fire").
            attacker (Combatant): The combatant dealing the damage (if applicable).
            skill_data (dict): Data about the skill used (if applicable).

        Returns:
            int: The final calculated damage.
        """
        final_damage = damage

        # --- Damage Rules ---

        # 1. Skill-Based Scaling (if applicable)
        if skill_data:
            if "stat_scaling" in skill_data["scaling_rules"]:
                scaling_stat = skill_data["scaling_rules"]["stat_scaling"]
                if scaling_stat in attacker.stats:
                    scaling_value = attacker.stats[scaling_stat]
                    final_damage = int(final_damage * (1 + (scaling_value / 10)))
            if "level_scaling_factor" in skill_data["scaling_rules"]:
                level_scaling_factor = skill_data["scaling_rules"]["level_scaling_factor"]
                final_damage = int(final_damage * (1 + (attacker.level * level_scaling_factor)))
            if "level" in skill_data:
                skill_level = skill_data["level"]
                final_damage = int(final_damage * (1 + (skill_level / 10)))
            if "flat_stat_scaling" in skill_data["scaling_rules"]:
                flat_stat_scaling = skill_data["scaling_rules"]["flat_stat_scaling"]
                if flat_stat_scaling in attacker.stats:
                    flat_scaling_stat_value = attacker.stats[flat_stat_scaling]
                    flat_scaling_value = skill_data["scaling_rules"].get("flat_scaling_value", 0)
                    final_damage = int(flat_scaling_stat_value * flat_scaling_value)
            if "combined_stat_scaling" in skill_data["scaling_rules"]:
                combined_scaling_total = 0
                for stat, weight in skill_data["scaling_rules"]["combined_stat_scaling"]:
                    if stat in attacker.stats:
                        combined_scaling_total += attacker.stats[stat] * weight
                    elif stat == "level":
                        combined_scaling_total += skill_level * weight
                    else:
                        print(f"Warning: Combined scaling stat '{stat}' not found in combatant's stats.")
                final_damage = int(combined_scaling_total * (1 + (attacker.level * level_scaling_factor)) * (1 + (skill_level / 10)))

        # 2. Defense/Resistance
        # Example: Reduce damage based on the defender's defense stat
        if skill_data and "base_heal" in skill_data:
            return final_damage
        final_damage = max(0, final_damage - self.stats["defense"])

        # 3. Passive Skill Effects (e.g., damage reduction)
        if attacker:
            total_flat_reduction = 0
            total_percent_reduction = 0
            for skill_name, skill_data in self.skills["passive_defense"].items():
                if skill_data.get("active", False):
                    if "flat_reduction" in skill_data:
                        total_flat_reduction += skill_data["flat_reduction"]
                    if "percent_reduction" in skill_data:
                        total_percent_reduction += skill_data["percent_reduction"]

            # Apply percentage reduction first
            final_damage = int(final_damage * (1 - total_percent_reduction))

            # Apply flat reduction second
            final_damage -= total_flat_reduction

        # 4. Effects (e.g., buffs, debuffs)
        # Example: Check for a "vulnerable" debuff that increases damage taken
        for effect in self.effects:
            if effect.name == "vulnerable":
                final_damage = int(final_damage * (1 + effect.modifier))
            elif effect.name == "magic_shield_effect":
                final_damage = max(0, final_damage - effect.flat_reduction) # Ensure damage doesn't go below zero

        # Ensure damage is not negative
        final_damage = max(0, final_damage)

        return final_damage


    def heal(self, amount):
        """Heals the combatant for a specified amount."""
        max_health = self._max_health
        heal_amount = min(amount, max_health - self.stats["health"])
        self.stats["health"] += heal_amount
        self._cached_stats["health"] = self.stats["health"]
        print(f"{self.name} heals for {heal_amount} health! Current health: {self.stats['health']}")

    def _calculate_combat_initiative(self):
        """Calculates the combat initiative for this combatant."""
        skill_data = None
        for category in self.skills:
            if "combat_initiative" in self.skills[category]:
                skill_data = self.skills[category]["combat_initiative"]
                break

        if skill_data is None:
            print(f"{self.name} does not have the skill combat_initiative.")
            return 0

        skill_level = skill_data.get("level", 1)

        # Calculate the sum of all relevant stats
        total_stats = 0
        for stat_name, stat_value in self._cached_stats.items():
            if stat_name in ["strength", "dexterity", "intelligence", "wisdom", "willpower", "constitution"]:
                total_stats += stat_value

        # Calculate initiative based on the total stats and skill level
        initiative = int(total_stats * (1 + (skill_level / 10)))

        # Add randomness based on skill level
        import random
        roll1 = random.randint(1, skill_level * 2)  # Roll 1
        roll2 = random.randint(1, skill_level * 2)  # Roll 2
        higher_roll = max(roll1, roll2)
        initiative += higher_roll

        return initiative

    def _apply_effect(self, effect_name, target):
        """Applies an effect to the target."""
        from game.available_skills import available_skills
        # Find the skill data for the effect
        skill_data = None
        for category in self.skills:
            # Check if the effect_name (which is actually a skill name) is a skill in the current category
            if effect_name in self.skills[category]:
                skill_data = self.skills[category][effect_name]
                break
        if skill_data is None:
            print(f"Effect '{effect_name}' not found in any skill's effects.")
            return

        if effect_name == "magic_shield":
            # Calculate flat_reduction
            base_flat_reduction = skill_data.get("base_flat_reduction", 0)
            skill_level = skill_data.get("level", 1)
            base_duration = skill_data.get("base_duration", 0)

            flat_reduction = base_flat_reduction
            for stat, weight in skill_data["scaling_rules"].get("stat_scaling", {}).items():
                flat_reduction += int(self.stats.get(stat, 0) * weight)
            flat_reduction += int(skill_level * skill_data["scaling_rules"].get("level_scaling_factor", 0))
            flat_reduction += int(skill_level * skill_data["scaling_rules"].get("flat_reduction_per_level", 0))
            duration = base_duration + (skill_level * skill_data["scaling_rules"].get("duration_per_level", 0))

            # Create the effect with the calculated flat_reduction
            effect = Effect(
                name="magic_shield_effect",
                duration=duration,
                modifier=0,
                description=skill_data["scaling_rules"]["description"],
                flat_reduction=flat_reduction,
                on_damage_taken=skill_data["scaling_rules"].get("on_damage_taken", None),
                skill_level=skill_level
            )
            target.effects.append(effect)
            effect.apply(target)
            print(f"{target.name} is now protected by a magic shield with {flat_reduction} flat reduction!")
        elif effect_name in available_skills["effects"]:
            effect_data = available_skills["effects"][effect_name]
            effect = Effect(
                name=effect_name,
                duration=effect_data.get("duration", None),
                modifier=effect_data.get("modifier", 0),
                description=effect_data["description"],
                flat_reduction=effect_data.get("flat_reduction", 0),
                on_damage_taken=effect_data.get("on_damage_taken", None),
                skill_level=skill_data.get("level", 1)
            )
            target.effects.append(effect)
            effect.apply(target)
            print(f"{target.name} is now affected by {effect_name}!")
        else:
            print(f"Effect '{effect_name}' not found.")


    def take_damage(self, damage, damage_type="physical", attacker=None, skill_data=None):
        """
        Applies damage to the combatant.

        Args:
            damage (int): The base damage value.
            damage_type (str): The type of damage (e.g., "physical", "magical", "fire").
            attacker (Combatant): The combatant dealing the damage (if applicable).
            skill_data (dict): Data about the skill used (if applicable).
        """

        final_damage = self._calculate_damage(damage, damage_type, attacker, skill_data)
        print(f"[DEBUG take_damage] {self.name} (ID: {self.id}) is taking {final_damage} damage!")

        # Update health using cached stats
        self._cached_stats["health"] -= final_damage
        self.stats["health"] = self._cached_stats["health"]
        print(f"[DEBUG take_damage] {self.name} (ID: {self.id}) health after damage: {self.stats['health']}")

        print(f"DEBUG: {self.stats['health']} vs {self._max_health}")

        # Trigger on_damage_taken effects
        for effect in self.effects:
            effect.damage_taken(self, final_damage)
        
        if self.stats["health"] <= 0:
            print(f"[DEBUG] {self.name} has been defeated!")
            self.grudge_list.clear()  # Clear grudges when defeated
            print(f"[DEBUG] Cleared grudge list for {self.name} (ID: {self.id})")
        return self.stats["health"] > 0

    def update_effects_start_of_turn(self):
        """Handles effects at the start of the turn."""
        for effect in self.effects:
            effect.turn_start(self)
        # Decrement skill cooldowns
        for category in self.skills.values():
            for skill_data in category.values():
                if skill_data["current_cooldown"] > 0:
                    skill_data["current_cooldown"] -= 1

    def update_effects_end_of_turn(self):
        """Handles effects at the end of the turn."""
        effects_to_remove = []
        for effect in self.effects:
            effect.duration -= 1
            if effect.duration <= 0:
                effects_to_remove.append(effect)

        for effect in effects_to_remove:
            effect.remove(self)
            self.effects.remove(effect)
            print(f"{effect.name} has worn off from {self.name}.")


class Player(Combatant):
    def __init__(self, combatant_id, name, base_stats, level, hates_all, hates_player_and_companions, hates, monster_type, has_traits, all_creature_traits_data, status_data, current_room=None, selected_traits=None):
        super().__init__(combatant_id, name, base_stats, level, hates_all, hates_player_and_companions, hates, monster_type)
        from game.managers import CombatantManager
        self.level = level
        self.has_traits = has_traits
        self.combatant_manager = CombatantManager(
            traits_dict=all_creature_traits_data,
            status_effects=status_data["status_effect"],
            selected_traits=selected_traits)
        self.inventory = ("inventory", [])
        self.equipment = ("equipment", {})
        self.current_room = current_room

    # Serialization method
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "inventory": self.inventory,
            "equipment": self.equipment,
            "current_room": self.current_room,
            "has_traits": self.has_traits,
            "all_creature_traits_data": self.combatant_manager.all_traits,
            "selected_traits": self.combatant_manager.selected_traits,
            "skills": self.skills
        })
        return base

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        # print(f"[DEBUG COMBATANT.PY] data in from_dict: {data}")

        base_stats = {
            "health": data["stats"]["health"],
            "attack": data["stats"]["attack"],
            "defense": data["stats"]["defense"],
            "strength": data["stats"]["strength"],
            "dexterity": data["stats"]["dexterity"],
            "intelligence": data["stats"]["intelligence"],
            "wisdom": data["stats"]["wisdom"],
            "willpower": data["stats"]["willpower"],
            "constitution": data["stats"]["constitution"],
            "level": data.get("level", 1),
            "health_per_level": data.get("health_per_level", 0),
            "spell_points_per_level": data.get("spell_points_per_level", 0),
            "health_per_constitution": data.get("health_per_constitution", 0),
            "damage_per_strength": data.get("damage_per_strength", 0),
            "spell_points_per_intelligence": data.get("spell_points_per_intelligence", 0),
            "defense_per_constitution": data.get("defense_per_constitution", 0)
        }

        # Extract and organize status effects properly
        status_data = {
            "status_effect": data.get("status_effect", {"buffs": {}, "debuffs": {}})
        }

        # Rebuild the Player object
        player = cls(
            combatant_id=data["id"],
            name=data["name"],
            base_stats=base_stats,
            level=data.get("level", 1),
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None),
            has_traits=data.get("has_traits", {}),
            all_creature_traits_data=data.get("all_creature_traits_data", {}),
            status_data=status_data,
            selected_traits=data.get("selected_traits", None),
            current_room=data.get("current_room", None)
        )
        player.skills = data.get("skills", {})
        player.stats = data.get("stats", player._calculate_stats())
        player.grudge_list = data.get("grudge_list", [])
        return player



class Companion(Combatant):
    def __init__(self, combatant_id, name, base_stats, level, hates_all, hates_player_and_companions, hates, monster_type, has_traits, all_creature_traits_data, status_data, current_room=None, selected_traits=None):
        super().__init__(combatant_id, name, base_stats, level, hates_all, hates_player_and_companions, hates, monster_type)
        self.level = level
        self.has_traits = has_traits
        from game.managers import CombatantManager
        self.combatant_manager = CombatantManager(
            traits_dict=all_creature_traits_data,
            status_effects=status_data["status_effect"],
            selected_traits=selected_traits)
        self.inventory =("inventory", [])
        self.equipment =("equipment", {})
        self.current_room = current_room

    # Serialization method
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "inventory": self.inventory,
            "equipment": self.equipment,
            "current_room": self.current_room,
            "has_traits": self.has_traits,
            "all_creature_traits_data": self.combatant_manager.all_traits,
            "selected_traits": self.combatant_manager.selected_traits,
            "skills": self.skills
        })
        return base

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        # print(f"[DEBUG COMBATANT.PY] data in from_dict: {data}")

        base_stats = {
            "health": data["stats"]["health"],
            "attack": data["stats"]["attack"],
            "defense": data["stats"]["defense"],
            "strength": data["stats"]["strength"],
            "dexterity": data["stats"]["dexterity"],
            "intelligence": data["stats"]["intelligence"],
            "wisdom": data["stats"]["wisdom"],
            "willpower": data["stats"]["willpower"],
            "constitution": data["stats"]["constitution"],
            "level": data.get("level", 1),
            "health_per_level": data.get("health_per_level", 0),
            "spell_points_per_level": data.get("spell_points_per_level", 0),
            "health_per_constitution": data.get("health_per_constitution", 0),
            "damage_per_strength": data.get("damage_per_strength", 0),
            "spell_points_per_intelligence": data.get("spell_points_per_intelligence", 0),
            "defense_per_constitution": data.get("defense_per_constitution", 0)
        }

        # Extract and organize status effects properly
        status_data = {
            "status_effect": data.get("status_effect", {"buffs": {}, "debuffs": {}})
        }


        companion = cls(
            combatant_id=data["id"],
            name=data["name"],
            base_stats=base_stats,
            level=data.get("level", 1),
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None),
            has_traits=data.get("has_traits", {}),
            all_creature_traits_data=data.get("all_creature_traits_data", {}),
            status_data=status_data,
            selected_traits=data.get("selected_traits", None),
            current_room = data.get("current_room", None)
        )
        companion.skills = data.get("skills", {})
        companion.stats = data.get("stats", companion._calculate_stats())
        companion.grudge_list = data.get("grudge_list", [])
        return companion


class Monster(Combatant):
    def __init__(self, combatant_id, name, base_stats, level, hates_all, hates_player_and_companions, hates, monster_type, has_traits, all_creature_traits_data, status_data, current_room=None, selected_traits=None):
        """
        :param level: The level of the monster, which affects its stats and descriptions.
        """
        # Include the 'level' argument when calling the parent constructor
        super().__init__(combatant_id, name, base_stats, level, hates_all, hates_player_and_companions, hates, monster_type)
        
        self.level = level
        self.has_traits = has_traits
        self.current_room = current_room
        
        from game.managers import CombatantManager
        self.combatant_manager = CombatantManager(
            traits_dict=all_creature_traits_data,
            status_effects=status_data["status_effect"],
            selected_traits=selected_traits
        )
        self._apply_selected_traits()
        # self.skills = {}

    def _apply_selected_traits(self):
        # Append selected traits to the monster's default traits
        self.has_traits.update(self.combatant_manager.selected_traits)

    def describe(self):
        """
        Provides a summary of the monster's attributes.
        """
        stats_description = ", ".join([f"{key}: {value}" for key, value in self.stats.items()])
        hates_description = (
            f"Hates All: {self.hates_all}, "
            f"Hates Player/Companions: {self.hates_player_and_companions}, "
            f"Hates Specific: {', '.join(self.hates) if self.hates else 'None'}"
        )
        return (
            f"{self.name} ({self.monster_type})\n"
            f"Stats: {stats_description}\nTraits: {self.has_traits}\n{hates_description}"
        )

    def _apply_selected_traits(self):
        self.has_traits.update(self.combatant_manager.selected_traits)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name,
            "stats": self.stats,
            "level": self.level,
            "has_traits": {key: value for key, value in self.has_traits.items()},
            "current_room": self.current_room,
            "all_creature_traits_data": self.combatant_manager.all_traits,
            "selected_traits": self.combatant_manager.selected_traits,
            "skills": self.skills
        })
        return base

    # Deserialization method
    @classmethod
    def from_dict(cls, data):
        # print(f"[DEBUG COMBATANT.PY] data in from_dict: {data}")

        base_stats = {
            "health": data["stats"]["health"],
            "attack": data["stats"]["attack"],
            "defense": data["stats"]["defense"],
            "strength": data["stats"]["strength"],
            "dexterity": data["stats"]["dexterity"],
            "intelligence": data["stats"]["intelligence"],
            "wisdom": data["stats"]["wisdom"],
            "willpower": data["stats"]["willpower"],
            "constitution": data["stats"]["constitution"],
            "level": data.get("level", 1),
            "health_per_level": data.get("health_per_level", 0),
            "spell_points_per_level": data.get("spell_points_per_level", 0),
            "health_per_constitution": data.get("health_per_constitution", 0),
            "damage_per_strength": data.get("damage_per_strength", 0),
            "spell_points_per_intelligence": data.get("spell_points_per_intelligence", 0),
            "defense_per_constitution": data.get("defense_per_constitution", 0)
        }

        
        # Extract and organize status effects properly
        status_data = {
            "status_effect": data.get("status_effect", {"buffs": {}, "debuffs": {}})
        }

        monster = cls(
            combatant_id=data["id"],
            name=data["name"],
            base_stats=base_stats,
            level=data.get("level", 1),
            hates_all=data.get("hates_all", False),
            hates_player_and_companions=data.get("hates_player_and_companions", False),
            hates=data.get("hates", []),
            monster_type=data.get("monster_type", None),
            has_traits=data.get("has_traits", {}),
            all_creature_traits_data=data.get("all_creature_traits_data", {}),
            status_data=status_data,
            selected_traits=data.get("selected_traits", None),
            current_room=data.get("current_room", None)
        )
        monster.skills = data.get("skills", {})
        monster.stats = data.get("stats", monster._calculate_stats())
        monster.grudge_list = data.get("grudge_list", [])
        return monster

    def _apply_selected_traits(self):
        self.has_traits.update(self.combatant_manager.selected_traits)
