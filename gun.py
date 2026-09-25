import random as r
import time as t


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


player1 = ""
player2 = ""
player3 = ""
player4 = ""

for i in range(players):
    if i == 1:
        player1 = input("Enter the name of player 1: ")
    elif i == 2:
        player2 = input("Enter the name of player 2: ")
    elif i == 3:
        player3 = input("Enter the name of player 3: ")
    elif i == 4:
        player4 = input("Enter the name of player 4: ")

