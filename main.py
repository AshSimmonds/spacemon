from fasthtml.common import *
from fasthtml.components import *
import random

app, rt = fast_app()

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
            return f"{self.name}'s {self.special_ability} is on cooldown for {self.ability_cooldown} more turn(s)!"
        
        if random.random() < self.ability_chance:
            if self.special_ability == "Cosmic Blast":
                damage = self.attack * 1.5
                target.hp -= damage
                result = f"{target.name} takes {damage:.0f} damage!"
            elif self.special_ability == "Gravity Shield":
                self.defense *= 1.5
                result = f"{self.name}'s defense increased!"
            elif self.special_ability == "Nebula Heal":
                heal = self.max_hp * 0.3
                self.hp = min(self.max_hp, self.hp + heal)
                result = f"{self.name} heals for {heal:.0f} HP!"
            elif self.special_ability == "Meteor Shower":
                damage = self.attack * 0.8
                target.hp -= damage
                result = f"{target.name} takes {damage:.0f} damage!"
            elif self.special_ability == "Black Hole":
                target.attack *= 0.7
                result = f"{target.name}'s attack decreased!"
            self.ability_cooldown = 3
            return f"{self.special_ability} succeeds! {result}"
        else:
            self.ability_cooldown = 1
            return f"{self.special_ability} fails!"

    def reduce_cooldowns(self):
        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

space_monsters = [
    SpaceMonster("Solara", 100, 20, 15, "Cosmic Blast", "Deals 1.5x attack damage", 0.7),
    SpaceMonster("Nebulos", 120, 18, 20, "Gravity Shield", "Increases defense by 50%", 0.8),
    SpaceMonster("Astralis", 90, 22, 12, "Nebula Heal", "Heals 30% of max HP", 0.6),
    SpaceMonster("Meteoron", 110, 25, 10, "Meteor Shower", "Deals 0.8x attack damage", 0.75),
    SpaceMonster("Vortexia", 95, 21, 18, "Black Hole", "Decreases enemy attack by 30%", 0.65)
]

player_monster = None
enemy_monster = None
turn_count = 0
game_log = []

def monster_info(monster):
    return [
        H3(monster.name),
        P(f"HP: {monster.hp:.0f}/{monster.max_hp}"),
        P(f"Attack: {monster.attack}"),
        P(f"Defense: {monster.defense:.1f}"),
        P(f"Special Ability: {monster.special_ability}"),
        P(f"Description: {monster.ability_description}"),
        P(f"Success Chance: {monster.ability_chance * 100:.0f}%"),
        P(f"Cooldown: {max(monster.ability_cooldown - 1, 0)} turn(s)")
    ]

@rt("/")
def get():
    return [
        H1("Space Monsters Game"),
        P("Choose your Space Monster to start the game:"),
        *[A(monster.name, href=f"/start-game/{i}") for i, monster in enumerate(space_monsters)]
    ]

@rt("/start-game/{monster_index}")
def start_game(monster_index: int = None):
    global player_monster, enemy_monster, turn_count, game_log
    
    try:
        monster_index = int(monster_index)
    except (TypeError, ValueError):
        monster_index = None

    if monster_index is None or not (0 <= monster_index < len(space_monsters)):
        return [
            H1("Error"),
            P("Invalid monster selection. Please choose a valid monster."),
            A("Go back to selection", href="/")
        ]
    
    player_monster = space_monsters[monster_index]
    enemy_monster = random.choice([m for m in space_monsters if m != player_monster])
    turn_count = 0
    game_log = [f"Battle: {player_monster.name} vs {enemy_monster.name}"]
    return battle_ui()

def battle_ui():
    return [
        H2("Battle"),
        *monster_info(player_monster),
        *monster_info(enemy_monster),
        A("Attack", href="/player-turn?action=attack"),
        A("Use Special Ability", href="/player-turn?action=special"),
        H3("Game Log"),
        *[P(entry) for entry in game_log[-5:]]  # Show last 5 entries
    ]

@rt("/player-turn")
def player_turn(request):
    global turn_count, game_log
    
    action = request.query_params.get("action")

    if player_monster is None or enemy_monster is None:
        return [
            H1("Error"),
            P("Game not properly initialized. Please start a new game."),
            A("Start New Game", href="/")
        ]
    
    turn_count += 1
    game_log.append(f"--- Turn {turn_count} ---")
    player_monster.reduce_cooldowns()
    enemy_monster.reduce_cooldowns()

    if action == "attack":
        damage = max(1, player_monster.attack - enemy_monster.defense)
        enemy_monster.hp -= damage
        game_log.append(f"{player_monster.name} deals {damage:.0f} damage to {enemy_monster.name}!")
    elif action == "special":
        result = player_monster.use_special_ability(enemy_monster)
        game_log.append(result)
    else:
        game_log.append("Invalid action. Turn skipped.")

    if enemy_monster.hp <= 0:
        game_log.append(f"{enemy_monster.name} fainted! {player_monster.name} wins!")
        return game_over("You Win!")

    # Enemy turn
    if enemy_monster.ability_cooldown == 0 and random.random() < enemy_monster.ability_chance:
        result = enemy_monster.use_special_ability(player_monster)
        game_log.append(result)
    else:
        damage = max(1, enemy_monster.attack - player_monster.defense)
        player_monster.hp -= damage
        game_log.append(f"{enemy_monster.name} deals {damage:.0f} damage to {player_monster.name}!")

    if player_monster.hp <= 0:
        game_log.append(f"{player_monster.name} fainted! {enemy_monster.name} wins!")
        return game_over("You Lose!")

    return battle_ui()

def game_over(result):
    return [
        H2("Game Over"),
        H3(result),
        *[P(entry) for entry in game_log],
        A("Play Again", href="/")
    ]

serve()