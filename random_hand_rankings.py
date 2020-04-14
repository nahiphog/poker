from random import randint, shuffle
from tqdm import tqdm
from tabulate import tabulate

all_52_cards = [ ]
suits = [ 'Diamonds' , 'Clubs', 'Hearts', 'Spades' ]
all_value_cards = [  '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K' , 'A']
score_values = [ [ all_value_cards[index], index + 1 ] for index in range(13) ]
score_values.reverse()
number_of_trials = int(1e4)

royal_flush_frequency,straight_flush_frequency,four_of_a_kind_frequency,full_house_frequency,flush_frequency,straight_frequency,three_of_a_kind_frequency,two_pairs_frequency,pair_frequency,high_card_frequency = 0,0,0,0,0,0,0,0,0,0

def refresh_all_cards():
    global all_52_cards

    all_52_cards = [ ]
    for element in all_value_cards:
        for item in suits:
            all_52_cards.append([ element, item])
    
    shuffle(all_52_cards)

def hero_dealt():
    global hero_hole_cards, all_52_cards
    for integer in range(2): # Dealt two cards
        hero_hole_cards.append( all_52_cards.pop(randint(0, len(all_52_cards) - 1)))

def burn_card(): all_52_cards.pop(0)

def deal_5_community_cards():
    global all_52_cards
    burn_card()  
    # Flop
    draw_cards = all_52_cards[:3]
    for integer in range(4): all_52_cards.pop(0) # Remove the first 3 cards, and burn a card

    # Turn
    draw_cards.append(all_52_cards[0])
    for integer in range(2): all_52_cards.pop(0) # Remove the first 1 card, and burn a card

    # River
    draw_cards.append(all_52_cards[0])
    all_52_cards.pop(0) # Remove the first 1 card 

    return draw_cards

def just_find_face_cards(those_7_cards):
    these_faces = []
    for element in those_7_cards:
        these_faces.append(element[0])
    return these_faces

def just_find_suit_cards(those_7_cards):
    these_suits = []
    for element in those_7_cards:
        these_suits.append(element[1])
    return these_suits

def royal_flush_checker(those_7_cards):

    these_specific_face_cards = just_find_face_cards(those_7_cards)
    these_specific_suit_cards = just_find_suit_cards(those_7_cards)

    if '10' in these_specific_face_cards:
        if 'J' in these_specific_face_cards:
            if 'Q' in these_specific_face_cards:
                if 'K' in these_specific_face_cards:
                    if 'A' in these_specific_face_cards:
                        if len(set(these_specific_suit_cards)) == 1:
                            return True

    return False           

def four_of_a_kind_checker(those_7_cards):
    these_specific_face_cards = just_find_face_cards(those_7_cards)

    frequency_counter = [ these_specific_face_cards.count(element) for element in all_value_cards ]
    if 4 in frequency_counter:
        return True
    
    return False

def full_house_checker(those_7_cards):
    these_specific_face_cards = just_find_face_cards(those_7_cards)

    frequency_counter = [ these_specific_face_cards.count(element) for element in all_value_cards ]
    if 3 in frequency_counter:
        if 2 in frequency_counter:
            return True
    
    return False

def flush_checker(those_7_cards):
    these_specific_suit_cards = just_find_suit_cards(those_7_cards)
    frequency_counter = [ these_specific_suit_cards.count(element) for element in suits ]
    if max(frequency_counter) < 5:
        return False
    else:
        this_specific_face_cards = just_find_face_cards(those_7_cards)
        for item in score_values:
            if item[0] in this_specific_face_cards:
                return [6, item[1] ]

def straight_checker(those_7_cards):
    these_specific_face_cards = just_find_face_cards(those_7_cards)

    modified_score_values = score_values
    modified_score_values.append('A')

    presence = []
    for element in modified_score_values:
        if element[0] in these_specific_face_cards: presence.append(1)
        else: presence.append(0)

    for index in range(10):
        if sum(presence[index : index + 5]) == 5: return [ 5, 10 - index]
    
    return False

def straight_flush_checker(those_7_cards):
    if not(flush_checker(those_7_cards) == False) and not(straight_checker(those_7_cards) == False):
        return [9, straight_checker(those_7_cards)[1] ]

    return False

def three_of_a_kind_checker(those_7_cards):
    these_specific_face_cards = just_find_face_cards(those_7_cards)

    frequency_counter = [ these_specific_face_cards.count(element) for element in all_value_cards ]

    if max(frequency_counter) == 3:
        if 2 not in frequency_counter:
            return True
    
    return False

def two_pair_checker(those_7_cards):
    these_specific_face_cards = just_find_face_cards(those_7_cards)

    frequency_counter = []
    for element in these_specific_face_cards:
        this_specific_frequency = these_specific_face_cards.count(element)
        frequency_counter.append(this_specific_frequency)

    if max(frequency_counter) == 2:
        if frequency_counter.count(2) >= 4:
            return True
    
    return False

def pair_checker(those_7_cards):
    these_specific_face_cards = just_find_face_cards(those_7_cards)

    frequency_counter = []
    for element in these_specific_face_cards:
        this_specific_frequency = these_specific_face_cards.count(element)
        frequency_counter.append(this_specific_frequency)

    if max(frequency_counter) == 2:
        if frequency_counter.count(2) == 2:
            return True
    
    return False

def choose_the_best_five_cards(player_hole_cards, community_cards):
    cards_presented = []
    for item in player_hole_cards: cards_presented.append(item)
    for item in community_cards: cards_presented.append(item)

    return cards_presented
    
def hand_ranking(player_cards, dealt_five_cards):
    this_specific_7_cards = []
    for element in player_cards: this_specific_7_cards.append(element)
    for element in dealt_five_cards: this_specific_7_cards.append(element)

    if royal_flush_checker(this_specific_7_cards):
        return [10 ]
    
    if not(straight_flush_checker(this_specific_7_cards) == False):
        return [9 , straight_flush_checker(this_specific_7_cards)]
    
    if four_of_a_kind_checker(this_specific_7_cards):
        return [8 ]

    if full_house_checker(this_specific_7_cards):
        return [7 ]

    if not( flush_checker(this_specific_7_cards) == False):
        return flush_checker(this_specific_7_cards)

    if not(straight_checker(this_specific_7_cards) == False):
        return straight_checker(this_specific_7_cards)

    if three_of_a_kind_checker(this_specific_7_cards):
        return [4 ]

    if two_pair_checker(this_specific_7_cards):
        return [3 ]
    
    if pair_checker(this_specific_7_cards):
        return [2 ]
    
    return [1 ]

def solo_mode():
    global all_52_cards, hero_hole_cards, royal_flush_frequency, straight_flush_frequency,four_of_a_kind_frequency ,full_house_frequency,flush_frequency,straight_frequency,three_of_a_kind_frequency,two_pairs_frequency ,pair_frequency,high_card_frequency

    hero_hole_cards = []
    refresh_all_cards()
    hero_dealt()
    burn_card()
    dealt_five_cards = deal_5_community_cards()
    heros_strength = hand_ranking(hero_hole_cards, dealt_five_cards)

    # print("")
    # print("Hero's hole cards: \t", end = '')
    # for element in hero_hole_cards:
    #     print(element, end = ' ')
    # print("\n")
    # print("Community cards: \t", end = '')
    # for element in dealt_five_cards:
    #     print(element, end = ' ')
    # print("\n")
    # print("Hero's top 7 cards: \t", end = '')
    # for element in choose_the_best_five_cards(hero_hole_cards, dealt_five_cards):
    #     print(element, end = ' ')
    # print("\n")
    # print(f"Hero's strength cards: \t\t\t{ heros_strength }")
    # print("\n")

    hero_hand = choose_the_best_five_cards(hero_hole_cards, dealt_five_cards)

    if heros_strength[0] == 10: # Royal flush
        royal_flush_frequency += 1

    if (heros_strength[0] == 9): # Straight flush
        straight_flush_frequency += 1
        
    if heros_strength[0] == 8: # Four of a kind
        four_of_a_kind_frequency += 1

    if heros_strength[0] == 7: # Full house
        full_house_frequency += 1

    if heros_strength[0] == 6: # Flush
        flush_frequency += 1

    if heros_strength[0] == 5: # Straight
        straight_frequency += 1

    if heros_strength[0] == 4: # Three of a Kind
        three_of_a_kind_frequency += 1

    if heros_strength[0] == 3: # Two Pairs
        two_pairs_frequency += 1

    if heros_strength[0] == 2: # Pair
        pair_frequency += 1

    if heros_strength[0] == 1: # High card
        high_card_frequency += 1

for _ in tqdm( range(number_of_trials) ): solo_mode()

print(f"Number of trials: \t {number_of_trials:,}\n")
# print(f"Hero won: \t\t {scoreboard[0]:,}")
# print(f"Villain won: \t\t {scoreboard[1]:,}")
# print(f"It's a draw: \t\t {scoreboard[2]:,}")

display_hand_ranking_frequencies = [ ['Royal flush', royal_flush_frequency, royal_flush_frequency / number_of_trials * 100],
['Straight flush', straight_flush_frequency, straight_flush_frequency / number_of_trials * 100 ],
['Four of a kind', four_of_a_kind_frequency, four_of_a_kind_frequency / number_of_trials * 100 ],
['Full house', full_house_frequency, full_house_frequency / number_of_trials * 100],
['Flush', flush_frequency, flush_frequency / number_of_trials * 100],
['Straight', straight_frequency, straight_frequency / number_of_trials * 100],
['Three of a kind', three_of_a_kind_frequency, three_of_a_kind_frequency / number_of_trials * 100],
['Two pairs', two_pairs_frequency, two_pairs_frequency  / number_of_trials * 100],
['Pair', pair_frequency, pair_frequency / number_of_trials * 100],
['High card', high_card_frequency, high_card_frequency  / number_of_trials * 100]]

print(tabulate(display_hand_ranking_frequencies, ["Hand rankings","Frequency", "Relative frequency (%)" ], tablefmt="fancy_grid", numalign="center"), "\n")
