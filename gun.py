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
playersLeft = 0

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
    print(f"{healthPerPlayer} health each.")

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
    global player1Items, player2Items, player3Items, player4Items

    # Skip jammed player
    if jammed[currentPlayer]:
        print(f"\n{players_list[currentPlayer]} is jammed and skips their turn!")
        t.sleep(0.5)
        jammed[currentPlayer] = False
        currentPlayer = (currentPlayer + 1) % players
        return
    if (player1Health <= 0 and currentPlayer == 0) or (player2Health <= 0 and currentPlayer == 1) or (player3Health <= 0 and currentPlayer == 2) or (player4Health <= 0 and currentPlayer == 3):
        print(f"\n{players_list[currentPlayer]} is dead")
        t.sleep(2)
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
            print("Players' items:")
            if currentPlayer == 0:
                print(f"  {players_list[currentPlayer]}: {player1Items}")
            elif currentPlayer == 1:
                print(f"  {players_list[currentPlayer]}: {player2Items}")
            elif currentPlayer == 2:
                print(f"  {players_list[currentPlayer]}: {player3Items}")
            elif currentPlayer == 3:
                print(f"  {players_list[currentPlayer]}: {player4Items}")
            print("Use an item by typing its name. Type 'back' to go back.")
            item_input = input("Enter the name of the item you want to use: ").strip()
            if item_input.lower() == "back":
                continue
            elif item_input in itemList:
                
                if item_input == "Hand Saw":
                    sawed = True
                    print(f"The next shot will deal double damage... If it's live")
                
                elif item_input == "Jammer":
                    item_target_input = input(f"Who do you want to jam? {players_list}: ").strip()
                    matched_item_target = None
                    if item_target_input.lower() == players_list[currentPlayer].lower():
                        print("You cannot jam yourself. Try again.")
                        continue
                    if item_target_input.lower() == players_list[0].lower():
                        matched_item_target = players_list[0]
                    elif item_target_input.lower() == players_list[1].lower():
                        matched_item_target = players_list[1]
                    elif players >= 3 and item_target_input.lower() == players_list[2].lower():
                        matched_item_target = players_list[2]
                    elif players == 4 and item_target_input.lower() == players_list[3].lower():
                        matched_item_target = players_list[3]
                    if matched_item_target:
                        target_index = players_list.index(matched_item_target)
                        jammed[target_index] = True
                        print(f"{matched_item_target} has been jammed and will skip their next turn!")

                elif item_input == "Magnifying Glass":
                    print(f"The bullet is: {loadout[currentBullet]}")
                    t.sleep(1)
                
                elif item_input == "Inverter":
                    loadout[currentBullet] = "Live" if loadout[currentBullet] == "Blank" else "Blank"
                    print(f"The bullet has been inverted")

                elif item_input == "Burner Phone":
                    # Ensure there are enough future bullets left in the loadout
                    min_future_index = currentBullet + 1  # Look at least 1 bullet ahead
                    max_future_index = len(loadout) - 1   # Last valid index in loadout list

                    if min_future_index <= max_future_index:
                      future_idx = r.randint(min_future_index, max_future_index)
                      print(f"[Burner Phone]: Bullet #{future_idx + 1} is {loadout[future_idx]}.")
                    else:
                        print("[Burner Phone]: How unfortunate...")

                elif item_input == "Beer":
                    print(f"Racked the shotgun. out came a {loadout[currentBullet]}")
                    currentBullet += 1
                elif item_input == "Cigarettes":
                    print(f"Gained a health point.")
                    if currentPlayer == 0:
                        player1Health = min(player1Health + 1, maxHealth)
                    elif currentPlayer == 1:
                        player2Health = min(player2Health + 1, maxHealth)
                    elif currentPlayer == 2:
                        player3Health = min(player3Health + 1, maxHealth)
                    elif currentPlayer == 3:
                        player4Health = min(player4Health + 1, maxHealth)
                elif item_input == "Remote":
                    print(f"Turn order of players has been reversed.")
                    players_list.reverse()  
                                      
            else:
                print("Invalid item. Try again.")
        else:
            print("Invalid option. Please enter 'shoot' or 'item'.")

for i in range(roundCount):
    print(f"Round {i + 1}")
    healthHandout(r.randint(3, 5))
    itemHandout(r.randint(2, 6))
    t.sleep(1)
    loadGun(r.randint(2, 6))
    playersLeft = len(players_list)
    while currentBullet < len(loadout) and playersLeft > 1:
        turn()