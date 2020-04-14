from random import randint, shuffle
from tqdm import tqdm

all_52_cards = [ ]
suits = [ 'Diamonds' , 'Clubs', 'Hearts', 'Spades' ]
all_value_cards = [  '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K' , 'A']
score_values = [ [ all_value_cards[index], index + 1 ] for index in range(13) ]
score_values.reverse()
number_of_trials = int(1e3)
scoreboard = [0,0,0]

def refresh_all_cards():
    global all_52_cards

    all_52_cards = [ ]
    for element in all_value_cards:
        for item in suits:
            all_52_cards.append([ element, item])
    
    shuffle(all_52_cards)

def heads_up():
    global hero_hole_cards, villain_hole_cards, all_52_cards
    for integer in range(2): # Both hero and villain were dealt 2 hole cards each
        hero_hole_cards.append( all_52_cards.pop(randint(0, len(all_52_cards) - 1)))
        villain_hole_cards.append( all_52_cards.pop(randint(0, len(all_52_cards) - 1)))

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
    
    if set(these_specific_face_cards) == { 'A', '2' , '3', '4', '5' }:
        return [5, 1]
    if set(these_specific_face_cards) == { '2' , '3', '4', '5' , '6' }:
        return [5, 2]
    if set(these_specific_face_cards) == {  '3', '4', '5' , '6', '7' }:
        return [5, 3]
    if set(these_specific_face_cards) == { '4', '5' , '6', '7', '8' }:
        return [5, 4]
    if set(these_specific_face_cards) == {'5' , '6', '7', '8' , '9'}:
        return [5, 5]

    if set(these_specific_face_cards) == { '6', '7', '8' , '9', '10' }:
        return [5, 6]

    if set(these_specific_face_cards) == {  '7', '8' , '9', '10' , 'J' }:
        return [5, 7]

    if set(these_specific_face_cards) == {'8' , '9', '10' , 'J', 'Q' }:
        return [5, 8]

    if set(these_specific_face_cards) == {  '9', '10' , 'J', 'Q', 'K' }:
        return [5, 9]

    if set(these_specific_face_cards) == {  '10' , 'J', 'Q', 'K', 'A'}:
        return [5, 10]

    return False

def straight_flush_checker(those_7_cards):
    if not(flush_checker(those_7_cards) == False) and not(straight_checker(those_7_cards) == False):
        return straight_checker(those_7_cards)

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

def comparing_equal_hand_ranking(first_hand,second_hand):
    global scoreboard
    draw = True
    for index in range(len(first_hand)):
        if first_hand[index] > second_hand[index]:
            scoreboard[0] += 1
            draw = False
            break
        elif first_hand[index] < second_hand[index]:
            scoreboard[1] += 1
            draw = False
            break

    if draw == True: scoreboard[2] += 1

def four_of_a_kind_strength(some_hole_cards, some_community_cards):
    this_seven_cards = choose_the_best_five_cards(some_hole_cards, some_community_cards)
    this_seven_face_cards = just_find_face_cards(this_seven_cards)

    for element in score_values:
        if this_seven_face_cards.count(element[0]) == 4:
            four_leading_strength = element[1]
            for integer in range(4): this_seven_face_cards.remove(element[0])
            break
    
    # Find the only blocker
    for element in score_values:
        if element[0] in this_seven_face_cards:
            blocker = element[1]

    return [four_leading_strength, blocker]

def full_house_strength(some_hole_cards, some_community_cards):
    this_seven_cards = choose_the_best_five_cards(some_hole_cards, some_community_cards)
    this_seven_face_cards = just_find_face_cards(this_seven_cards)

    for element in score_values:
        if this_seven_face_cards.count(element[0]) == 3:
            three_leading_strength = element[1]
            for integer in range(3): this_seven_face_cards.remove(element[0])
            break
    
    # Find the largest blocker pair
    for element in score_values:
        if element[0] in this_seven_face_cards:
            if this_seven_face_cards.count(element[0]) >= 2:
                pair_blocker = element[1]
                break

    return [three_leading_strength, pair_blocker]

def three_of_a_kind_strength(some_hole_cards, some_community_cards):
    this_seven_cards = choose_the_best_five_cards(some_hole_cards, some_community_cards)
    this_seven_face_cards = just_find_face_cards(this_seven_cards)

    for element in score_values:
        if this_seven_face_cards.count(element[0]) == 3:
            other_three_leading_strength = element[1]
            for integer in range(3): this_seven_face_cards.remove(element[0])
            break
    
    two_blockers = [] 
    # Find the 2 largest blockers
    for element in score_values:
        if element[0] in this_seven_face_cards:
            two_blockers.append(element[1])
            if len(two_blockers) == 2:
                break

    return [other_three_leading_strength, two_blockers[0], two_blockers[1]]

def two_pairs_strength(some_hole_cards, some_community_cards):
    this_seven_cards = choose_the_best_five_cards(some_hole_cards, some_community_cards)
    this_seven_face_cards = just_find_face_cards(this_seven_cards)

    two_leading_pairs = []
    for repetition in range(2):
        for element in score_values:
            if this_seven_face_cards.count(element[0]) == 2:
                two_leading_pairs.append(  element[1] )
                for integer in range(2): this_seven_face_cards.remove(element[0])
                break
    
    # Find the largest blockers
    for element in score_values:
        if element[0] in this_seven_face_cards:
            one_blockers = element[1]
            break

    return [two_leading_pairs[0], two_leading_pairs[1], one_blockers ]

def pair_strength(some_hole_cards, some_community_cards):
    this_seven_cards = choose_the_best_five_cards(some_hole_cards, some_community_cards)
    this_seven_face_cards = just_find_face_cards(this_seven_cards)

    for element in score_values:
        if this_seven_face_cards.count(element[0]) == 2:
            pair_value = element[1]
            this_seven_face_cards.remove(element[0])
            break

    four_blockers = []
    
    # Find the 4 blocker
    for element in score_values:
        if element[0] in this_seven_face_cards:
            four_blockers.append(element[1])
            if len(four_blockers) == 4: break

    return [pair_value, four_blockers[0], four_blockers[1], four_blockers[2], four_blockers[3] ]

def high_card(some_hole_cards, some_community_cards):
    this_seven_cards = choose_the_best_five_cards(some_hole_cards, some_community_cards)
    this_seven_face_cards = just_find_face_cards(this_seven_cards)
    five_blockers = []
    
    # Find the 4 blocker
    for element in score_values:
        if element[0] in this_seven_face_cards:
            five_blockers.append(element[1])
            if len(five_blockers) == 5: break

    return five_blockers

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

def run_heads_up():
    global scoreboard, all_52_cards, hero_hole_cards, villain_hole_cards

    hero_hole_cards, villain_hole_cards = [], []
    refresh_all_cards()
    heads_up()
    burn_card()
    dealt_five_cards = deal_5_community_cards()
    heros_strength = hand_ranking(hero_hole_cards, dealt_five_cards)
    villains_strength = hand_ranking(villain_hole_cards, dealt_five_cards)

    # print("")
    # print("Hero's hole cards: \t", end = '')
    # for element in hero_hole_cards:
    #     print(element, end = ' ')
    # print("\n")
    # print("Villain's hole cards: \t", end = '')
    # for element in villain_hole_cards:
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
    # print("Villain's top 7 cards: \t", end = '')
    # for element in choose_the_best_five_cards(villain_hole_cards, dealt_five_cards):
    #     print(element, end = ' ')
    # print("\n")

    # print(f"Hero's strength cards: \t\t\t{ heros_strength }")
    # print(f"Villain's strength cards: \t\t{ villains_strength }")
    # print("\n")
    if heros_strength[0] > villains_strength[0]: scoreboard[0] += 1
    elif heros_strength[0] < villains_strength[0]: scoreboard[1] += 1
    else:
        hero_hand = choose_the_best_five_cards(hero_hole_cards, dealt_five_cards)
        villain_hand = choose_the_best_five_cards(villain_hole_cards, dealt_five_cards)

        if heros_strength[0] == 10: # Royal flush
            scoreboard[2] += 1

        if (heros_strength[0] == 9) or (heros_strength[0] == 5): # Straight flush or just straight
            hero_straight = straight_checker(hero_hand)
            villain_straight = straight_checker(villain_hand)

            comparing_equal_hand_ranking(hero_straight, villain_straight)
            
        if heros_strength[0] == 8: # Four of a kind
            hero_four_of_a_kind = four_of_a_kind_strength(hero_hole_cards, dealt_five_cards)
            villain_four_of_a_kind = four_of_a_kind_strength(villain_hole_cards, dealt_five_cards)

            comparing_equal_hand_ranking(hero_four_of_a_kind, villain_four_of_a_kind)

        if heros_strength[0] == 7: # Full house
            hero_full_house = full_house_strength(hero_hole_cards, dealt_five_cards)
            villain_full_house = full_house_strength(villain_hole_cards, dealt_five_cards)

            comparing_equal_hand_ranking(hero_full_house, villain_full_house)

        if heros_strength[0] == 6: # Flush
            hero_flush = flush_checker(hero_hand)
            villain_flush = flush_checker(villain_hand)

            comparing_equal_hand_ranking(hero_flush, villain_flush)

        if heros_strength[0] == 4: # Three of a Kind
            hero_three_of_a_kind = three_of_a_kind_strength(hero_hole_cards, dealt_five_cards)
            villain_three_of_a_kind = three_of_a_kind_strength(villain_hole_cards, dealt_five_cards)

            comparing_equal_hand_ranking(hero_three_of_a_kind, villain_three_of_a_kind)

        if heros_strength[0] == 3: # Two Pairs
            hero_two_pairs = two_pairs_strength(hero_hole_cards, dealt_five_cards)
            villain_two_pairs = two_pairs_strength(villain_hole_cards, dealt_five_cards)

            comparing_equal_hand_ranking(hero_two_pairs, villain_two_pairs)

        if heros_strength[0] == 2: # Pair
            hero_pair = pair_strength(hero_hole_cards, dealt_five_cards)
            villain_pair = pair_strength(villain_hole_cards, dealt_five_cards)

            comparing_equal_hand_ranking(hero_pair, villain_pair)

        if heros_strength[0] == 1: # High card
            hero_high_card = high_card(hero_hole_cards, dealt_five_cards)
            villain_high_card = high_card(villain_hole_cards, dealt_five_cards)

            comparing_equal_hand_ranking(hero_high_card, villain_high_card)

for _ in tqdm( range(number_of_trials) ): run_heads_up()

print(f"Number of trials: \t {number_of_trials:,}")
print(f"Hero won: \t\t {scoreboard[0]:,}")
print(f"Villain won: \t\t {scoreboard[1]:,}")
print(f"It's a draw: \t\t {scoreboard[2]:,}")
