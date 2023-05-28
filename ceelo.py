#Onomateponymo: Panagiotis Trypos
#AM: 5131

#Fuctions
from random import randint
from time import sleep

#Set the players that will play
def set_players():
    number_of_players = input("Enter number of players [2-6]: ")

    try:
        number_of_players = eval(number_of_players)
    except Exception as ex:
        pass

    #checking if the value that the user gave is correct
    if type(number_of_players) == str:
        number_of_players = 3
        print("I expected between 2 and 6 players!")
        print("I am setting the number of players to 3\n")
    elif number_of_players < 2 or number_of_players > 6 or (number_of_players != int(number_of_players)):
        number_of_players = 3
        print("I expected between 2 and 6 players!")
        print("I am setting the number of players to 3\n")
    else:
        print("You setted the number of players to " + str(number_of_players) +"\n")

    #Creating a dictionary of players
    players = {player: "player " + str(player) for player in range(1, number_of_players+1)}    
    return players

#Set default coins to players
def set_coins():
    global players

    default_coins = input("Enter default coins [5-100]: ")

    try:
        default_coins = eval(default_coins)
    except Exception as ex:
        pass
    
    #checking if the value that the user gave is correct
    if type(default_coins) == str:
        default_coins = 10
        print("I expected between 5 and 100 coins!")
        print("I am setting the number of coins to 10")
    elif (default_coins < 5 or default_coins > 100) or (default_coins != int(default_coins)):
        default_coins = 10
        print("I expected between 5 and 100 coins!")
        print("I am setting the number of coins to 10")
    else:
        print("You setted the default coins to " + str(default_coins))
            
    #Creating a dictionary that have got the coins of each player
    players_coins = {player: default_coins for player in players}
    return players_coins

#Setting first banker
def set_banker():
    global players
    
    banker_number = randint(1, len(players))
    banker = players[banker_number]
    return [banker_number, banker]

#Showing player's coins
def show_coins():
    global coins, players
    
    print("\nCurrent balance:")
    for i in range(1, len(players)+1):
        print(players[i] + " has " + str(coins[i]) + " coins")

#Set players bet to 0
def set_bets():
    global players
    
    return {player: 0 for player in players}

#Players are betting
def players_bet():
    global coins, players, banker, bets
    
    sum_betting = 0

    #Setting banker's bet
    banker_bet = eval(input("\n" + str(banker[1]) + ": You are the banker! Please enter a valid bank amount: "))

    #Checking banker's bet if it's valid
    while banker_bet > coins[banker[0]]:
        banker_bet = eval(input("\n" + str(banker[1]) + ": You are the banker! Please enter a valid bank amount: "))

    bets[banker[0]] = banker_bet
    
    #Players betting
    for counter_player in range(1, len(players)+1):
        if players[counter_player] != banker[1]:            
            if banker_bet - sum_betting > 0:
                player_bet = eval(input(players[counter_player] + ": Please enter a valid bet: "))

                #Checking if player bet a valid ammount or else he must set new ammount
                while player_bet > banker_bet - sum_betting or player_bet > coins[counter_player]:
                    player_bet = eval(input(players[counter_player] + ": The ammount you setted is not valid! Please enter a valid bet: "))
                    
                bets[counter_player] = player_bet
                sum_betting += player_bet

    #Return to the banker the rest of the coins that didn't betted by the players (if it isn't 0)
    banker_bet = banker_bet - (banker_bet - sum_betting)
    coins[banker[0]] = coins[banker[0]] + (banker_bet - sum_betting)

    bets[banker[0]] = banker_bet

#Showing player's bets
def show_bets():
    global players, bets, banker
    
    for i in range(1, len(players)+1):
        if players[i] != banker[1]:
            print(players[i] + ": has bet " + str(bets[i]))
        else:
            print(players[i] + ": Banker with bank amount: " + str(bets[i]))

#Roll the dices and add their values in a list
def roll_dices():
    return [randint(1, 6) for i in range(3)]

#banker's turn to play
def banker_play():
    #create automatic win and lose possibilities
    automatic_win = [[i, i, 6] for i in range(1, 7)] + [[i, i, i] for i in range(1, 7)] + [[4, 5, 6]]
    automatic_lose = [[1, i, i] for i in range(2, 7)] + [[1, 2, 3]]
    banker_score = 0
    
    while banker_score == 0:
        banker_dices = roll_dices()
        print("Banker rolled the dices: " + str(banker_dices))
        banker_dices = sorted(banker_dices)
        
        if banker_dices in automatic_win:
            banker_score = "win"
        elif banker_dices in automatic_lose:
            banker_score = "lose"
        elif banker_dices[0] != banker_dices[1] == banker_dices[2] or banker_dices[2] != banker_dices[1] == banker_dices[0]:
            if banker_dices[0] != banker_dices[1] == banker_dices[2]:
                banker_score = banker_dices[0]
                print("Banker scored: " + str(banker_score))
            elif banker_dices[2] != banker_dices[1] == banker_dices[0]:
                banker_score = banker_dices[2]
                print("Banker scored: " + str(banker_score))
            else:
                banker_score = banker_dices[1]
        else:
            print("Banker rolls again")
            sleep(1)

    return banker_score

#Players' turn to playe
def players_play():
    global players, banker, bets

    player_score = 0
        
    #Player roll the dices
    player_win = [[i, i, i] for i in range(1, 7)] + [4, 5, 6]
    player_lose = [1, 2, 3]

    #Repeat rolling dices till score points or win the banker
    while player_score == 0:
        player_dices = roll_dices()
        player_dices = sorted(player_dices)
        print(players[i] + " rolled the dices: " + str(player_dices))
        sleep(1)

        #Checking if player wins with triple or (4, 5, 6)
        if player_dices in player_win:                
            player_score = 6
        elif player_dices in player_lose:
            player_score = -1
        #Checking if player score points
        elif player_dices[0] == player_dices[1] != player_dices[2] or player_dices[0] != player_dices[1] == player_dices[2]:
            #Setting score points of the player
            if player_dices[0] != player_dices[1] == player_dices[2]:
                player_score = player_dices[0]
                print("Player scored: " + str(player_score))
            elif player_dices[2] != player_dices[1] == player_dices[0]:
                player_score = player_dices[2]
                print("Player scored: " + str(player_score))
        #Player rolls again
        else:
            print(players[i] + " rolls again")

    if player_dices == [4, 5, 6]:
        return [player_score, True]
    else:
        return [player_score, False]

#Global variables
players = set_players()
coins = set_coins()
banker = set_banker()
bets = set_bets()

#Main program
continue_playing = True

print("\nGame starts with " + str(len(players)) + " players")
print("Each player has " + str(coins[1]) + " coins")
print(banker[1] + " is randomly chosen as banker")

while continue_playing:
    bets = set_bets()
        
    players_bet()
    print("\nRound starts:")
    show_bets()
    
    input("\nBanker: press ENTER to roll the dices!")
    banker_score = banker_play()
    
    #Counting banker's loses
    counting_loses = 0
    
    #Banker Automatic wins and get the coins
    if banker_score == "win":
        for i in range(1, len(players)+1):
            if players[i] != banker[1]:
                coins[i] = coins[i] - bets[i]
            else:
                coins[i] = coins[i] + bets[i]
        print("Automatic Win! Banker wins all bets! Round ends!")
    #Banker Automatic lose and give the coins
    elif banker_score == "lose":
        for i in range(1, len(players)+1):
            if players[i] != banker[1]:
                coins[i] = coins[i] + bets[i]
            else:
                coins[i] = coins[i] - bets[i]
        print("Automatic Lose! Players wins their bets! Round ends!")
    else:
        current_player_banker = True

        for i in range(1, len(players)+1):
            if bets[i] != 0 and players[i] != banker[1]:
                input("\n" + players[i] + ": press ENTER to roll dice")

                player_score = players_play()

                if player_score[1]:
                    banker[0], banker[1] = i, players[i]
                    current_player_banker = False

                #Checking who wins between current player and banker and transfer the coins to the right player
                if player_score[0] > banker_score:
                    coins[i] = coins[i] + bets[i]
                    coins[banker[0]] = coins[banker[0]] - bets[i]
                    print("Player wins!")
                    counting_loses += 1
                elif player_score[0] < banker_score:
                    coins[i] = coins[i] - bets[i]
                    coins[banker[0]] = coins[banker[0]] + bets[i]
                    print("Banker wins!")
                else:
                    print("It's a tie between the banker and the player!")

    #Checking if banker must change
    if counting_loses == len(players)-1 and player_score[1]:
        if banker[0] == len(players):
            banker[0], banker[1] = 1, players[1]
        else:
            banker[0], banker[1] = banker[0]+1, players[banker[0]+1]

    #Check if the game ends
    i = 1
    while i <= len(bets):
        if coins[i] <= 0:
            print(players[i] + " is bankrupted. The game ends")
            continue_playing = False
            break
        i = i+1

    #Show the coins of players
    show_coins()

input("\nPress ENTER to exit...")
