import random

num_players = 10  # How many players
tokens_per_player = 3  # How many tokens per player
die = list("LCR..W")  # Faces of the die
debug = True


def left(player):  # Do left throw
    global players
    players[player] -= 1
    players[(player-1) % num_players] += 1


def centre(player):  # Do centre throw
    global players, pot
    players[player] -= 1
    pot += 1


def right(player):  # Do right throw
    global players
    players[player] -= 1
    players[(player+1) % num_players] += 1


def steal_random(player):  # Do single wild throw
    global players
    if still_playing():  # Check there is still someone to steal from, as the game might be over by now
        while True:
            victim = random.randint(0, num_players - 1)  # Pick a random victim
            if victim != player and players[victim] > 0:  # Check the victim isn't us, and has some tokens to steal
                players[victim] -= 1
                players[player] += 1
                return victim
    else:
        return None


def wild(player):  # Do 3x wild throw
    global players, pot
    players[player] += pot
    pot = 0


def still_playing():  # Predicate to test if game is still playing (does >1 player have at least 1 token)
    players_with_tokens = 0
    for player in players:
        if player > 0:
            players_with_tokens += 1
            if players_with_tokens > 1:
                return True
    else:
        return False

# Let's play


pot = 0  # Pot starts off empty
turn = random.randint(0, num_players - 1)  # Choose which player goes first
num_turns = 0  # Count turns for stats

players = [tokens_per_player for i in range(0, num_players)]  # Initialise list players with their token count
if debug:
    print(str(players) + " (pot=" + str(pot) + ")")

while still_playing():

    num_turns += 1  # Count the number of turns

    if players[turn] > 0:  # Player only gets a throw if they have at least one token
        throw = [die[random.randint(0, 5)] for i in range(0, min(players[turn], 3))]
        if debug:
            print("Player " + str(turn) + "'s turn. Throw was " + "".join(throw) + " ", end="")

        if throw == list("WWW"):  # Match 3x wild
            wild(turn)
        else:
            for dice in throw:  # Iterate through each die - do passing before stealing - more victims to steal from
                if dice == "L":  # Left
                    left(turn)
                elif dice == "C":  # Centre
                    centre(turn)
                elif dice == "R":  # Right
                    right(turn)
            for dice in throw:
                if dice == "W": # Steal
                    if debug:
                        print("(victim=" + str(steal_random(turn)) + ")", end="")

        if debug:
            print("\n" + str(players) + " (pot=" + str(pot) + ")")

    turn = (turn+1) % num_players  # Next player

for i in range(0, num_players):  # Game over. Find who won
    if players[i] > 0:  # This player has tokens still - they're the winner
        print("Winner was player " + str(i) + " of " + str(num_players) + " after " + str(num_turns)
              + " turns, with a win of " + str(players[i]) + " token(s)")
