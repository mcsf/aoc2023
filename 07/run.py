#!/usr/bin/env python3

from sys import stdin
from collections import Counter
from itertools import combinations_with_replacement as combine

# Types of hand
HIGH, ONE, TWO, THREE, FULL, FOUR, FIVE = range(7)

# Individual card values
VALUES = {card: i for i, card in enumerate('23456789TJQKA')}
VALUES_JOKER = VALUES | {'J': -1}


def parse():
    for line in stdin:
        hand, bid = line.strip().split(' ')
        yield (hand, int(bid))


def winnings(hands, jokers=False):
    ranking = sort_hands(hands, jokers)
    return sum(rank * hand[-1] for rank, hand in enumerate(ranking, start=1))


def sort_hands(hands, jokers=False):
    type_classifier, values = \
            (hand_type, VALUES) if not jokers else \
            (find_best_type, VALUES_JOKER)

    def key(pair):
        hand, bid = pair
        type_value = type_classifier(hand)
        card_values = map(values.get, hand)
        return [type_value, *card_values]

    return sorted(hands, key=key)


def hand_type(hand):
    shape = sorted(Counter(hand).values())
    types = [([5], FIVE), ([1, 4], FOUR), ([2, 3], FULL), ([1, 1, 3], THREE),
             ([1, 2, 2], TWO), ([1, 1, 1, 2], ONE), ([1, 1, 1, 1, 1], HIGH)]
    return next(t for (s, t) in types if shape == s)


def find_best_type(hand):
    return max(map(hand_type, possible_hands(hand)))


def possible_hands(hand):
    if hand == 'JJJJJ':
        yield hand
        return

    counts = Counter(hand)
    joker_count = counts['J']
    base_cards = hand.replace('J', '')

    for replacement_cards in combine(set(base_cards), r=joker_count):
        new_hand = base_cards + ''.join(replacement_cards)
        yield new_hand


hands = list(parse())
print(winnings(hands))
print(winnings(hands, jokers=True))
