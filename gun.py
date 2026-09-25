import random as r
import time as t

# Set up players
players = 0
player1 = ""
player2 = ""
player3 = ""
player4 = ""
players_list = []

# Set up playerdata
player1Health = 0
player2Health = 0
player3Health = 0
player4Health = 0

player1Items = []
player2Items = []
player3Items = []
player4Items = []

# Set up game variables
roundCount = 0
round = 0
load = 0
itemsEnabled = True
maxHealth = 8
maxItemsPerPlayer = 8
loadout = []
itemsPerLoadout = 3
currentPlayer = 0
currentBulletLive = False
currentBullet = 0
itemList = ["Hand Saw", "Magnifying Glass", "Inverter", "Burner Phone", "Beer", "Cigarettes", "Jammer"]
sawed = False
jammed = [False] * 4

#get players
while True:
    try:
        players = int(input("Enter the number of players: "))
        
        if players < 2:
            print("You need at least 2 players to play this game.")
            continue 
        elif players > 4:
            print("You can only have a maximum of 4 players.")
            continue
        
        break
        
    except ValueError:
        print("Invalid input. Please enter a whole number.")

jammed = [False] * players
if players <= 3:
    itemList.append("Remote")

for i in range(players):
    if i == 0:
        player1 = input("Enter the name of player 1: ")
    elif i == 1:
        player2 = input("Enter the name of player 2: ")
    elif i == 2:
        player3 = input("Enter the name of player 3: ")
    elif i == 3:
        player4 = input("Enter the name of player 4: ")

#list of players (zero indexed)
players_list = [player1, player2, player3, player4]

'''
for i in range(players):
    print(f"{players_list[i]} is player {i + 1}.")
'''

while True:
    try:
        roundCount = int(input("Enter the number of rounds: "))

        if roundCount > 3:
            print("You can only have a maximum of 3 rounds.")
            continue
        break
        
    except ValueError:
        print("Invalid input. Please enter a whole number.")

while True:
    itemsEnabled = input("Do you want to enable items? (y/n): ").lower()

    if itemsEnabled == "y":
        itemsEnabled = True
        break
    elif itemsEnabled == "n":
        itemsEnabled = False
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

def itemHandout(itemsPerPlayer):
    global player1Items, player2Items, player3Items, player4Items

    if itemsEnabled:
        limitedItemsPerPlayer = min(itemsPerPlayer, maxItemsPerPlayer)
        for i in range(players):
            if i == 0:
                player1Items = r.choices(itemList, k=limitedItemsPerPlayer)
            elif i == 1:
                player2Items = r.choices(itemList, k=limitedItemsPerPlayer)
            elif i == 2:
                player3Items = r.choices(itemList, k=limitedItemsPerPlayer)
            elif i == 3:
                player4Items = r.choices(itemList, k=limitedItemsPerPlayer)


def healthHandout(healthPerPlayer):
    global player1Health, player2Health, player3Health, player4Health, maxHealth

    for i in range(players):
        if i == 0:
            player1Health = healthPerPlayer
        elif i == 1:
            player2Health = healthPerPlayer
        elif i == 2:
            player3Health = healthPerPlayer
        elif i == 3:
            player4Health = healthPerPlayer
    maxHealth = healthPerPlayer

def loadGun(totalBullets):
    global load, currentBulletLive, currentBullet, loadout
    load += 1
    loadout = []

    if totalBullets > 1:
        loadout.append("Live")
        loadout.append("Blank")

    while len(loadout) < totalBullets:
        loadin = r.randint(0, 1)
        if loadin == 1:
            loadout.append("Live")
        else:
            loadout.append("Blank")

    r.shuffle(loadout)

def turn():
    global currentPlayer, currentBulletLive, currentBullet, loadout, players_list, sawed
    global player1Health, player2Health, player3Health, player4Health, jammed

    # Skip jammed player
    if jammed[currentPlayer]:
        print(f"\n{players_list[currentPlayer]} is jammed and skips their turn!")
        jammed[currentPlayer] = False
        currentPlayer = (currentPlayer + 1) % players
        return

    print(f"\n--- {players_list[currentPlayer]}'s Turn ---")
    
    while True:
        choice = input("Do you want to shoot or use an item? (shoot/item): ").strip().lower()

        if choice == "shoot":
            # Prompt target selection
            target_input = input(f"Who do you want to shoot? {players_list}: ").strip()
            
            # Match input to player (case-insensitive check)
            matched_player = None
            for p in players_list[:players]:
                if p.lower() == target_input.lower():
                    matched_player = p
                    break

            if not matched_player:
                print("Invalid player name. Try again.")
                continue

            target_index = players_list.index(matched_player)
            bullet_type = loadout[currentBullet]
            is_self = (target_index == currentPlayer)

            print(f"\n*CLICK* ... It was a {bullet_type.upper()}!")

            if bullet_type == "Live":
                # Determine damage
                damage = 2 if sawed else 1
                sawed = False  # Reset saw status after shooting

                print(f"{players_list[currentPlayer]} shot {matched_player} for {damage} damage!")

                # Apply damage
                if target_index == 0:
                    player1Health -= damage
                elif target_index == 1:
                    player2Health -= damage
                elif target_index == 2:
                    player3Health -= damage
                elif target_index == 3:
                    player4Health -= damage

                # Pass to next player
                currentPlayer = (currentPlayer + 1) % players

            elif bullet_type == "Blank":
                sawed = False # Sawing a blank still consumes the saw effect
                
                if is_self:
                    print(f"{players_list[currentPlayer]} shot themselves with a blank! They get another turn.")
                    # Player keeps their turn (currentPlayer is not incremented)
                else:
                    print(f"{players_list[currentPlayer]} shot {matched_player} with a blank. No damage done.")
                    currentPlayer = (currentPlayer + 1) % players

            # Advance to the next bullet
            currentBullet += 1
            break

        elif choice == "item":
            print("Item mechanic placeholder - implement item selection here.")
            break
        else:
            print("Invalid option. Please enter 'shoot' or 'item'.")