import random

class SpaceMonster:
    def __init__(self, name, hp, attack, defense, special_ability, ability_description, ability_chance):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.special_ability = special_ability
        self.ability_description = ability_description
        self.ability_chance = ability_chance
        self.ability_cooldown = 0

    def use_special_ability(self, target):
        if self.ability_cooldown > 0:
            print(f"{self.name}'s {self.special_ability} is on cooldown for {self.ability_cooldown} more turn(s)!")
            return False

        print(f"{self.name} attempts to use {self.special_ability}!")
        if random.random() < self.ability_chance:
            print(f"{self.special_ability} succeeds!")
            if self.special_ability == "Cosmic Blast":
                damage = self.attack * 1.5
                target.hp -= damage
                print(f"{target.name} takes {damage:.0f} damage!")
            elif self.special_ability == "Gravity Shield":
                self.defense *= 1.5
                print(f"{self.name}'s defense increased!")
            elif self.special_ability == "Nebula Heal":
                heal = self.max_hp * 0.3
                self.hp = min(self.max_hp, self.hp + heal)
                print(f"{self.name} heals for {heal:.0f} HP!")
            elif self.special_ability == "Meteor Shower":
                damage = self.attack * 0.8
                target.hp -= damage
                print(f"{target.name} takes {damage:.0f} damage!")
            elif self.special_ability == "Black Hole":
                target.attack *= 0.7
                print(f"{target.name}'s attack decreased!")
            self.ability_cooldown = 3  # Set cooldown to 3 (will be 2 at start of next turn)
            return True
        else:
            print(f"{self.special_ability} fails!")
            self.ability_cooldown = 1  # Set cooldown to 1 on failure (will be 0 at start of next turn)
            return False

    def reduce_cooldowns(self):
        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

def display_monster_info(monster):
    print(f"\n{monster.name}")
    print(f"HP: {monster.hp:.0f}/{monster.max_hp}")
    print(f"Attack: {monster.attack}")
    print(f"Defense: {monster.defense}")
    print(f"Special Ability: {monster.special_ability}")
    print(f"Description: {monster.ability_description}")
    print(f"Success Chance: {monster.ability_chance*100:.0f}%")
    print(f"Cooldown: {max(monster.ability_cooldown - 1, 0)} turn(s)")

def battle(player_monster, enemy_monster):
    print(f"\nBattle: {player_monster.name} vs {enemy_monster.name}")
    
    turn_count = 0
    while player_monster.hp > 0 and enemy_monster.hp > 0:
        turn_count += 1
        print(f"\n--- Turn {turn_count} ---")
        print(f"{player_monster.name} HP: {player_monster.hp:.0f}")
        print(f"{enemy_monster.name} HP: {enemy_monster.hp:.0f}")
        
        # Reduce cooldowns at the start of each turn
        player_monster.reduce_cooldowns()
        enemy_monster.reduce_cooldowns()
        
        # Player's turn
        while True:
            action = input("Choose action (1: Attack, 2: Special Ability, 3: View Monster Info): ")
            if action == "1":
                damage = max(1, player_monster.attack - enemy_monster.defense)
                enemy_monster.hp -= damage
                print(f"{player_monster.name} deals {damage:.0f} damage to {enemy_monster.name}!")
                break
            elif action == "2":
                if player_monster.use_special_ability(enemy_monster):
                    break
            elif action == "3":
                display_monster_info(player_monster)
            else:
                print("Invalid choice. Please try again.")
        
        if enemy_monster.hp <= 0:
            print(f"\n{enemy_monster.name} fainted! {player_monster.name} wins!")
            return
        
        # Enemy's turn
        if enemy_monster.ability_cooldown == 0 and random.random() < enemy_monster.ability_chance:
            enemy_monster.use_special_ability(player_monster)
        else:
            damage = max(1, enemy_monster.attack - player_monster.defense)
            player_monster.hp -= damage
            print(f"{enemy_monster.name} deals {damage:.0f} damage to {player_monster.name}!")
        
        if player_monster.hp <= 0:
            print(f"\n{player_monster.name} fainted! {enemy_monster.name} wins!")
            return

def main():
    space_monsters = [
        SpaceMonster("Solara", 100, 20, 15, "Cosmic Blast", "Deals 1.5x attack damage", 0.7),
        SpaceMonster("Nebulos", 120, 18, 20, "Gravity Shield", "Increases defense by 50%", 0.8),
        SpaceMonster("Astralis", 90, 22, 12, "Nebula Heal", "Heals 30% of max HP", 0.6),
        SpaceMonster("Meteoron", 110, 25, 10, "Meteor Shower", "Deals 0.8x attack damage", 0.75),
        SpaceMonster("Vortexia", 95, 21, 18, "Black Hole", "Decreases enemy attack by 30%", 0.65)
    ]
    
    print("Welcome to Space Monsters!")
    print("Choose your Space Monster:")
    for i, monster in enumerate(space_monsters, 1):
        print(f"{i}. {monster.name}")
    
    while True:
        try:
            choice = int(input("Enter the number of your chosen Space Monster: ")) - 1
            if 0 <= choice < len(space_monsters):
                player_monster = space_monsters[choice]
                break
            else:
                print("Invalid choice. Please select a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    display_monster_info(player_monster)
    input("Press Enter to start the battle...")
    
    enemy_monster = random.choice([m for m in space_monsters if m != player_monster])
    
    battle(player_monster, enemy_monster)

if __name__ == "__main__":
    main()