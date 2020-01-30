import random

characters = ['♥', '♣', '♦', '♠']
deck = []
players = []
_currentPlayer = int(-1)
played_deck = []
draw_count = 0
player_last_played = [(), (), (), (), (), ()]


def initialize_game(): # initializes the game and allows the player to choose number of players & their names.
    while True:
        try:
            player_count = int(input('How many players do you want to play?: '))

            for player_num in range(player_count):
                player_name = input('Give name of player {}: '.format(player_num))
                player_data = [player_name, [], 0, (), False]
                players.append(player_data)
            break
        except ValueError:
            print('Only numerical input allowed!')


def pick_initial_card(inp, out): # picks a random card to start off the game
    randomCard = random.choice(inp)
    out.append(randomCard)
    return out


def create_deck(): # creates the deck and assigns scores to each card
    global played_deck, deck
    deck = []
    for character in characters:
        for i in range(1, 14):
            card = str(i)
            value = i
            if i == 1:
                card = 'A'
                value = 11
            elif i == 11:
                card = 'J'
                value = 10
            elif i == 12:
                card = 'Q'
                value = 10
            elif i == 13:
                card = 'K'
                value = 10
            _tuple = (card, character, value)
            deck.append(_tuple)
    played_deck = pick_initial_card(deck, played_deck)


def matches(card1, card2): # check if a move is legal / card match (check readme)
    _return = False

    if card1[0] == card2[0]:
        _return = True
    elif card1[1] == card2[1]:
        _return = True
    return _return


def shuffle_deck():
    random.shuffle(deck)


def draw_card(closed_pile, player_cards): # draws 1 card from the deck into a player's hand
    global played_deck
    if len(closed_pile) == 0: # if there are no more cards left in the deck, reset it (check readme)
        _lastCard = getLastCard(played_deck)
        closed_pile = played_deck[:-1]
        played_deck = [_lastCard]
        print("{{ No cards left in the deck, shuffling and adjusting deck! }}")
    card = random.choice(closed_pile)
    closed_pile.remove(card)
    player_cards.append(card)


initialize_game()
create_deck()
shuffle_deck()


def draw_cards_for_players(): # draws the initial 7 cards for each player
    for player in players:
        for card_count in range(7):
            draw_card(deck, player[1])


def determine_next_turn(curr_player): # determines whose turn is next.
    curr_player += 1
    curr_player = curr_player % len(players) # using modulo to return to ID 0 once we get out of bounds
    return curr_player


def hasCardsLeft(player_id): #checks if the bot has got any cards left
    player = players[player_id]
    return len(player[1]) == 0


def getLastCard(player_cards):
    return player_cards[-1]


def getLastPlayer(player_id):
    if player_id == 0:
        return len(players) - 1
    else:
        return player_id - 1


def set_skipped_card(player_id):
    players[player_id][4] = True


def reset_skipped_card(player_id):
    players[player_id][4] = False


def skipped_card(player_id):
    return players[player_id][4]


def botPickCard(bot_id): # called when it is the bots turn to play a card
    global draw_count
    available = players[bot_id][1]
    foundCard = False
    lastPlayedCard = getLastCard(played_deck)

    if is_skip(lastPlayedCard) and get_player_last_played(bot_id) != lastPlayedCard:
        print("bot losing turn")
    else:
        if skipped_card(getLastPlayer(bot_id)):
            reset_skipped_card(getLastPlayer(bot_id))
        if is_plus_two(lastPlayedCard):
            if has_plus_two(bot_id):
                for card_id in range(len(available)):
                    if is_plus_two(available[card_id]):
                        card = available[card_id]
                        played_deck.append(card)
                        del players[bot_id][1][card_id]
                        foundCard = True
                        set_player_last_played(bot_id, card)
                        print("- {} got rid of a card.".format(players[bot_id][0]))
                        break
            else:
                draw_plus_cards(bot_id)
                draw_count = 0
        else:
            for card_id in range(len(available)):
                if matches(available[card_id], lastPlayedCard):
                    card = available[card_id]
                    played_deck.append(card)
                    del players[bot_id][1][card_id]
                    set_player_last_played(bot_id, card)
                    foundCard = True
                    print("- {} got rid of a card.".format(players[bot_id][0]))
                    break

        played_card = get_player_last_played(bot_id)
        if played_card != ():
            if is_replay(played_card):
                replay_played(bot_id)
            elif is_plus_two(played_card):
                plus_two_played()
            elif is_ace(played_card):
                for card_id in range(len(available)):
                    card = available[card_id]
                    played_deck.append(card)
                    del players[bot_id][1][card_id]
                    set_player_last_played(bot_id, card)
                    foundCard = True
                    print("- {} got rid of a second card (ace previously).".format(players[bot_id][0]))
                    break

        if not foundCard:
            draw_card(deck, players[bot_id][1])
            print("- {} drew a card (no cards to use).".format(players[bot_id][0]))
        return foundCard


def calculate_scores(): # gets the scores for the players, ordering them from player with the least score (first) to the one with highest (last).
    scores = []
    for i in range(len(players)): # calculate the score for player
        player = players[i]
        score = 0
        for card in player[1]:
            score += card[2]
        scores.append((i, score))
    scores.sort(key=lambda tup: tup[1]) # sort the array

    for _tuple in scores:
        players[_tuple[0]][2] += _tuple[1]
        print("User: {} | Score: {}".format(players[_tuple[0]][0], players[_tuple[0]][2]))
    return scores


def reset_player_cards(): #
    for player in players:
        player[1] = []


def restart_game(): # starts a new round
    create_deck()
    shuffle_deck()
    reset_player_cards()
    draw_cards_for_players()


def is_plus_two(card):
    return card[0] == '7'


def is_replay(card):
    return  card[0] == '8'


def is_skip(card):
    return card[0] == '9'


def is_ace(card):
    return card[0] == 'A'


def replay_played(player_id): # called when a replay card is played
    global _currentPlayer
    if not hasCardsLeft(player_id):
        draw_card(deck, players[player_id][1])
        print("Can't replay if you do not have any more cards on you.")
    else:
        _currentPlayer -= 1


def plus_two_played(): # called when a player calls a plus 2 card
    global draw_count
    draw_count += 2


def ace_played(player_id): # called when a player plays ace card.
    if player_id == 0:
        print("Available cards: ")
        print(players[player_id][1])
        choice = input("> 'Ace'! You can play a card of your choice: ")
        if 0 <= int(choice) <= len(players[_currentPlayer][1]) - 1:
            card = players[_currentPlayer][1][int(choice)]
            played_deck.append(card)
            del players[_currentPlayer][1][int(choice)]

            if is_plus_two(card):
                plus_two_played()
            elif is_replay(card):
                replay_played(_currentPlayer)
            elif is_ace(card):
                ace_played(_currentPlayer)
        else:
            print("Invalid range input.")


def has_plus_two(player_id): # checks if the player has got a +2 card
    for card in players[player_id][1]:
        if is_plus_two(card):
            return True
    return False


def draw_plus_cards(player_id): # draws the extra cards for a player
    global draw_count
    for i in range(draw_count):
        draw_card(deck, players[player_id][1])
    draw_count = 0


def get_player_last_played(player_id): # returns the card the player last played.
    return players[player_id][3]


def set_player_last_played(player_id, card): # updates the card the player last played.
    players[player_id][3] = card


def start_game(): # basically, handling all game calls.
    global _currentPlayer, deck, played_deck, draw_count
    _currentPlayer = determine_next_turn(_currentPlayer)
    while hasCardsLeft(_currentPlayer):
        if _currentPlayer == 0:
            lastCard = getLastCard(played_deck)

            if is_plus_two(lastCard) and not get_player_last_played(_currentPlayer) == lastCard:
                if has_plus_two(_currentPlayer):
                    print("As last card drawn by the other user, was a +2 card, you can also draw a +2 (and you have "
                          "one on you!).")
                elif not has_plus_two(_currentPlayer):
                    print("Last card was a +2, and you do not have any on you, drawing +{}".format(draw_count))
                    draw_plus_cards(_currentPlayer)
                    draw_count = 0

            if is_skip(lastCard) and get_player_last_played(_currentPlayer) != lastCard:
                print("losing turn")
            else:
                print("Last played card: {}".format(lastCard))
                print("Available cards: ")
                print(players[_currentPlayer][1])
                while True:
                    choice = input("> Choose a card from 0 to {}, or 'skip' to pick a card from the deck: ".format(
                        len(players[_currentPlayer][1]) - 1))
                    if choice == 'skip':
                        draw_card(deck, players[_currentPlayer][1])
                        if lastCard == get_player_last_played(_currentPlayer):
                            set_skipped_card(_currentPlayer)
                        break
                    else:
                        if 0 <= int(choice) <= len(players[_currentPlayer][1]) - 1:
                            card = players[_currentPlayer][1][int(choice)]
                            if matches(card, lastCard):
                                played_deck.append(card)
                                del players[_currentPlayer][1][int(choice)]
                                set_player_last_played(_currentPlayer, card)

                                if is_plus_two(lastCard):
                                    if has_plus_two(_currentPlayer):
                                        if not is_plus_two(card):
                                            print("You drew {} cards (because of last card played)".format(draw_count))
                                            draw_plus_cards(_currentPlayer)

                                if is_plus_two(card):
                                    plus_two_played()
                                elif is_replay(card):
                                    replay_played(_currentPlayer)
                                elif is_ace(card):
                                    ace_played(_currentPlayer)
                                break
                            else:
                                print("Invalid card chosen; either skip, or pick a valid one.")
                        else:
                            print("Invalid range input.")

        else:
            botPickCard(_currentPlayer)

        if not hasCardsLeft(_currentPlayer):

            print(calculate_scores())
            winner_count = 0
            for i in range(len(players)):
                if players[i][2] >= 50:
                    winner_count += 1
            if winner_count == 0:
                print("One round is over! Continuing!")
                restart_game()
            else:
                print("GAME OVER!!")
                print(calculate_scores())
                break
        _currentPlayer = determine_next_turn(_currentPlayer)


draw_cards_for_players()
start_game()
