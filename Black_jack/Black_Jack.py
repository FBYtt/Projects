import random
deck = []
cards = ["10","2","3","4","5","6","7","8","9","J","Q","K","A"]
suite = ["clubs", "diamonds", "hearts", "spades"]

for card in cards:
    for i in suite:
        pair = card + " " + i
        deck.append(pair)
shuffled_deck = random.sample(deck, len(deck))
player = []
dealer = []
turn = True
d_turn = True
split_hand = False
p1 = None
p2 = None
for i in range(2):
    player.append(shuffled_deck.pop())
    dealer.append(shuffled_deck.pop())

print(f"Players cards are {player}")
print(f"Dealers cards are: [{dealer[0]}, 'Hidden']")


def decision(deal):
    turn = True
    p_points = point_calculator(deal)
    while turn:
        d = input("Double, Hit, Stand?: ").lower()
        if d == "stand":
            break
        elif d == "hit":
            deal.append(shuffled_deck.pop())
            print(f"Players cards are {deal}")
            p_points = point_calculator(deal)
            print(f"Player points: {p_points}")
            if p_points >= 21:
                break
        elif d == "double":
            deal.append(shuffled_deck.pop())
            print(deal)
            p_points = point_calculator(deal)
            print(f"Player points: {p_points}")


            break
        else:
            print("Invalid input.")
    return p_points


def check_winner(hand_points):

    if d_points < hand_points < 22:
        print("Player wins!")
    elif hand_points == d_points:
        print("Draw!")
    elif d_points > hand_points and d_points > 21:
        print("Player wins!")
    else:
        print("Dealer wins!")


def point_calculator(hand):
    points = 0
    acecounter = 0
    for card in hand:
        n = card.split()
        n = n[0]
        if n == "A":
            points += 11
            acecounter += 1
        elif n == "K":
            points += 10
        elif n == "Q":
            points += 10
        elif n == "J":
            points += 10
        else:
            n = int(n)
            points += n
    while points > 21 and acecounter > 0:
        points -= 10
        acecounter -= 1
    return points
p_points = point_calculator(player)
d_points = point_calculator(dealer)
print(f"Player points: {p_points}")
print(f"Dealer points: {point_calculator([dealer[0]])} ???")
while turn:
    split_hand = False
    l1 = []
    l2 = []
    n = player.pop(0)
    m = player.pop(0)
    if n[0] != m[0]:
        player.append(n)
        player.append(m)
        decision(player)
        p_points = point_calculator(player)
        turn = False
        break

    while n[0] == m[0]:
        question = input("You have a pair. Split?(y/n): ").lower()
        if question == "n":
            player.append(n)
            player.append(m)
            decision(player)
            turn = False
            break
        if question == "y":
            split_hand = True
            l1.append(n)
            l1.append(shuffled_deck.pop())
            print(f"First pair of cards are: {l1}")
            p1 = point_calculator(l1)
            print(f"Pair one points are: {p1}")
            print(f"Dealer points: {point_calculator([dealer[0]])} ???")
            p1 = decision(l1)
            l2.append(m)
            l2.append(shuffled_deck.pop())
            p2 = point_calculator(l2)
            print(f"Second pair of cards are: {l2}")
            print(f"Pair two points are: {p2}")
            print(f"Dealer points: {point_calculator([dealer[0]])} ???")
            p2 = decision(l2)
            turn = False
            break

        else:
            print("Incorrect input.")
if p_points <= 21:
    print(f"Dealers actual cards are: {dealer}")
    print(f"Dealer points: {d_points}")
else:
    print("Busted")
if p_points <= 21:
    while d_points < 17:
           dealer.append(shuffled_deck.pop())
           print(f"Dealers cards are: {dealer}")
           d_points = point_calculator(dealer)
           print(f"Player points: {p_points}")
           print(f"Dealer points: {d_points}")

if split_hand:
    check_winner(p1)
    check_winner(p2)
else:
    check_winner(p_points)



