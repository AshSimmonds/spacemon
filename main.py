<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Space Monsters Game</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        button { margin: 5px; padding: 5px 10px; }
        #gameLog { border: 1px solid #ccc; padding: 10px; margin-top: 20px; height: 300px; overflow-y: scroll; }
    </style>
</head>
<body>
    <h1>Space Monsters Game</h1>
    <div id="gameArea">
        <div id="monsterSelection"></div>
        <div id="battleArea" style="display:none;">
            <h2>Battle</h2>
            <div id="playerInfo"></div>
            <div id="enemyInfo"></div>
            <button id="attackBtn">Attack</button>
            <button id="specialBtn">Use Special Ability</button>
            <button id="infoBtn">View Monster Info</button>
        </div>
    </div>
    <div id="gameLog"></div>

    <script>
        class SpaceMonster {
            constructor(name, hp, attack, defense, specialAbility, abilityDescription, abilityChance) {
                this.name = name;
                this.hp = hp;
                this.maxHp = hp;
                this.attack = attack;
                this.defense = defense;
                this.specialAbility = specialAbility;
                this.abilityDescription = abilityDescription;
                this.abilityChance = abilityChance;
                this.abilityCooldown = 0;
            }

            useSpecialAbility(target) {
                if (this.abilityCooldown > 0) {
                    log(`${this.name}'s ${this.specialAbility} is on cooldown for ${this.abilityCooldown} more turn(s)!`);
                    return false;
                }

                log(`${this.name} attempts to use ${this.specialAbility}!`);
                if (Math.random() < this.abilityChance) {
                    log(`${this.specialAbility} succeeds!`);
                    switch (this.specialAbility) {
                        case "Cosmic Blast":
                            const damage = this.attack * 1.5;
                            target.hp -= damage;
                            log(`${target.name} takes ${damage.toFixed(0)} damage!`);
                            break;
                        case "Gravity Shield":
                            this.defense *= 1.5;
                            log(`${this.name}'s defense increased!`);
                            break;
                        case "Nebula Heal":
                            const heal = this.maxHp * 0.3;
                            this.hp = Math.min(this.maxHp, this.hp + heal);
                            log(`${this.name} heals for ${heal.toFixed(0)} HP!`);
                            break;
                        case "Meteor Shower":
                            const meteorDamage = this.attack * 0.8;
                            target.hp -= meteorDamage;
                            log(`${target.name} takes ${meteorDamage.toFixed(0)} damage!`);
                            break;
                        case "Black Hole":
                            target.attack *= 0.7;
                            log(`${target.name}'s attack decreased!`);
                            break;
                    }
                    this.abilityCooldown = 3;
                    return true;
                } else {
                    log(`${this.specialAbility} fails!`);
                    this.abilityCooldown = 1;
                    return false;
                }
            }

            reduceCooldowns() {
                if (this.abilityCooldown > 0) {
                    this.abilityCooldown--;
                }
            }
        }

        const spaceMonsters = [
            new SpaceMonster("Solara", 100, 20, 15, "Cosmic Blast", "Deals 1.5x attack damage", 0.7),
            new SpaceMonster("Nebulos", 120, 18, 20, "Gravity Shield", "Increases defense by 50%", 0.8),
            new SpaceMonster("Astralis", 90, 22, 12, "Nebula Heal", "Heals 30% of max HP", 0.6),
            new SpaceMonster("Meteoron", 110, 25, 10, "Meteor Shower", "Deals 0.8x attack damage", 0.75),
            new SpaceMonster("Vortexia", 95, 21, 18, "Black Hole", "Decreases enemy attack by 30%", 0.65)
        ];

        let playerMonster, enemyMonster;
        let turnCount = 0;

        function log(message) {
            const gameLog = document.getElementById('gameLog');
            gameLog.innerHTML += message + '<br>';
            gameLog.scrollTop = gameLog.scrollHeight;
        }

        function displayMonsterInfo(monster) {
            return `
                <h3>${monster.name}</h3>
                <p>HP: ${monster.hp.toFixed(0)}/${monster.maxHp}</p>
                <p>Attack: ${monster.attack}</p>
                <p>Defense: ${monster.defense.toFixed(1)}</p>
                <p>Special Ability: ${monster.specialAbility}</p>
                <p>Description: ${monster.abilityDescription}</p>
                <p>Success Chance: ${(monster.abilityChance * 100).toFixed(0)}%</p>
                <p>Cooldown: ${Math.max(monster.abilityCooldown - 1, 0)} turn(s)</p>
            `;
        }

        function updateBattleInfo() {
            document.getElementById('playerInfo').innerHTML = displayMonsterInfo(playerMonster);
            document.getElementById('enemyInfo').innerHTML = displayMonsterInfo(enemyMonster);
        }

        function startBattle() {
            document.getElementById('monsterSelection').style.display = 'none';
            document.getElementById('battleArea').style.display = 'block';
            enemyMonster = spaceMonsters[Math.floor(Math.random() * spaceMonsters.length)];
            while (enemyMonster.name === playerMonster.name) {
                enemyMonster = spaceMonsters[Math.floor(Math.random() * spaceMonsters.length)];
            }
            log(`Battle: ${playerMonster.name} vs ${enemyMonster.name}`);
            updateBattleInfo();
        }

        function playerTurn(action) {
            turnCount++;
            log(`--- Turn ${turnCount} ---`);
            playerMonster.reduceCooldowns();
            enemyMonster.reduceCooldowns();

            if (action === 'attack') {
                const damage = Math.max(1, playerMonster.attack - enemyMonster.defense);
                enemyMonster.hp -= damage;
                log(`${playerMonster.name} deals ${damage.toFixed(0)} damage to ${enemyMonster.name}!`);
            } else if (action === 'special') {
                playerMonster.useSpecialAbility(enemyMonster);
            }

            if (enemyMonster.hp <= 0) {
                log(`${enemyMonster.name} fainted! ${playerMonster.name} wins!`);
                endBattle();
                return;
            }

            // Enemy turn
            if (enemyMonster.abilityCooldown === 0 && Math.random() < enemyMonster.abilityChance) {
                enemyMonster.useSpecialAbility(playerMonster);
            } else {
                const damage = Math.max(1, enemyMonster.attack - playerMonster.defense);
                playerMonster.hp -= damage;
                log(`${enemyMonster.name} deals ${damage.toFixed(0)} damage to ${playerMonster.name}!`);
            }

            if (playerMonster.hp <= 0) {
                log(`${playerMonster.name} fainted! ${enemyMonster.name} wins!`);
                endBattle();
                return;
            }

            updateBattleInfo();
        }

        function endBattle() {
            document.getElementById('attackBtn').disabled = true;
            document.getElementById('specialBtn').disabled = true;
        }

        function initGame() {
            const monsterSelection = document.getElementById('monsterSelection');
            monsterSelection.innerHTML = '<h2>Choose your Space Monster:</h2>';
            spaceMonsters.forEach((monster, index) => {
                const button = document.createElement('button');
                button.textContent = monster.name;
                button.onclick = () => {
                    playerMonster = new SpaceMonster(
                        monster.name, monster.maxHp, monster.attack, monster.defense,
                        monster.specialAbility, monster.abilityDescription, monster.abilityChance
                    );
                    startBattle();
                };
                monsterSelection.appendChild(button);
            });

            document.getElementById('attackBtn').onclick = () => playerTurn('attack');
            document.getElementById('specialBtn').onclick = () => playerTurn('special');
            document.getElementById('infoBtn').onclick = () => log(displayMonsterInfo(playerMonster));
        }

        initGame();
    </script>
</body>
</html>