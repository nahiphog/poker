from random import randint, shuffle

all_52_cards = [ ]
suits = [ 'Diamond' , 'Club', 'Hearts', 'Spade' ]
all_value_cards = [ 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K' ]


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
    return True

def straight_checker(those_7_cards):
    these_specific_face_cards = just_find_face_cards(those_7_cards)
    
    if set(these_specific_face_cards) == { 'A', '2' , '3', '4', '5' }:
        return True
    if set(these_specific_face_cards) == { '2' , '3', '4', '5' , '6' }:
        return True
    if set(these_specific_face_cards) == {  '3', '4', '5' , '6', '7' }:
        return True
    if set(these_specific_face_cards) == { '4', '5' , '6', '7', '8' }:
        return True
    if set(these_specific_face_cards) == {'5' , '6', '7', '8' , '9'}:
        return True

    if set(these_specific_face_cards) == { '6', '7', '8' , '9', '10' }:
        return True

    if set(these_specific_face_cards) == {  '7', '8' , '9', '10' , 'J' }:
        return True

    if set(these_specific_face_cards) == {'8' , '9', '10' , 'J', 'Q' }:
        return True

    if set(these_specific_face_cards) == {  '9', '10' , 'J', 'Q', 'K' }:
        return True

    if set(these_specific_face_cards) == {  '10' , 'J', 'Q', 'K', 'A'}:
        return True

    return False

def straight_flush_checker(those_7_cards):
    if flush_checker(those_7_cards) and straight_checker(those_7_cards):
        return True   

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
        return [1, 'Royal flush' ]
    
    if straight_flush_checker(this_specific_7_cards):
        return [2 ,'Straight flush' ]
    
    if four_of_a_kind_checker(this_specific_7_cards):
        return [3, 'Four of a kind' ]

    if full_house_checker(this_specific_7_cards):
        return [4 , 'Full house' ]

    if flush_checker(this_specific_7_cards):
        return [5 , 'Flush' ]

    if straight_checker(this_specific_7_cards):
        return [6, 'Straight' ]

    if three_of_a_kind_checker(this_specific_7_cards):
        return [7, 'Three of a kind' ]

    if two_pair_checker(this_specific_7_cards):
        return [8, 'Two pairs' ]
    
    if pair_checker(this_specific_7_cards):
        return [9 , 'Pair' ]
    
    return [10 , 'High card' ]

number_of_trials = int(1e3)
scoreboard = [0,0,0]

for integer in range(number_of_trials):
    hero_hole_cards, villain_hole_cards = [], []
    refresh_all_cards()
    heads_up()
    dealt_five_cards = deal_5_community_cards()

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

    heros_strength = hand_ranking(hero_hole_cards, dealt_five_cards)
    villains_strength = hand_ranking(villain_hole_cards, dealt_five_cards)

    # print(f"Hero's strength cards: \t\t\t{ heros_strength }")
    # print(f"Villain's strength cards: \t\t{ villains_strength }")
    # print("\n")

    if heros_strength[0] < villains_strength[0]: scoreboard[0] += 1
    elif heros_strength[0] > villains_strength[0]: scoreboard[1] += 1
    else: scoreboard[2] += 1

print(scoreboard)




# Not complete

def four_of_a_kind_strength(some_hole_cards, some_community_cards):
    this_seven_cards = choose_the_best_five_cards(some_hole_cards, some_community_cards)

    remaining_face_cards_left = just_find_face_cards(all_52_cards)

    for element in all_value_cards:
        if element not in remaining_face_cards_left:
            four_repeated = element
            break
    

    return four_repeated

    
# # print(four_of_a_kind_strength)
