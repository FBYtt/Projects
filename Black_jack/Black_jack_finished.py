import pygame as pg
from random import shuffle
from pygame import MOUSEBUTTONDOWN

#screen stuff
screen_width, screen_height = 1920, 1080
screen_scale = 0.8
screen = pg.display.set_mode((0,0))
pg.display.set_caption("Black Jack")
clock = pg.time.Clock()


pg.init()
#Lists
player = []
dealer = []
deck = []
player_hand = []
dealer_hand = []
player_1 = []
player_2 = []
player_hand_1 = []
player_hand_2 = []
deal_hit = False
split_hand = 0
hidden = 0
p_points = 0
p_points_1 = 0
p_points_2 = 0
d_points = 0
cards_in_deck = 0
double_hit = 0
bet = 0
bet_1 = 0
bet_2 = 0
cooldown= 0
bet_active = True
player_turn_end = False
game_started = False
split_hit = False
decks_amount = 4
player_card_x = 655
dealer_card_x = 655
player_card_x_s1 = 395
player_card_x_s2 = 895
#for hit button
player_card_hit_x = 895
dealer_card_hit_x = 895
player_card_hit_x_s1 = 635
player_card_hit_x_s2 = 1135
player_card_number = 2


money = 500
p_cardy = 450
rank = ["2","3","4","5","6","7","8","9","Z","J","Q","K","A"]
suit = ["C","D","H","S"]
bg_color = (139,0,0)
color = (0, 128, 60)
#Deck
for i in range(decks_amount):
    for r in rank:
        for s in suit:
            pair = r + s
            deck.append(pair)
    shuffle(deck)


#functions
def point_calculator(hand):
    points = 0
    ace_counter = 0
    for _ in hand:
        n = _.split()
        n = n[-1][0]
        if n == "A":
            points += 11
            ace_counter += 1
        elif n == "K":
            points += 10
        elif n == "Q":
            points += 10
        elif n == "J":
            points += 10
        elif n == "Z":
            points += 10
        else:
            n = int(n)
            points += n
    while points > 21 and ace_counter > 0:
        points -= 10
        ace_counter -= 1
    return points


def deal_cards(hand,deck):
    del hand[:]
    for _ in range(2):
        hand.append(deck.pop())

def do_player_deal():
    global p_points,p_points_1,p_points_2,player_card_x,split_hand,player_card_x_s1,player_card_x_s2


    if split_hand == 1:
        player_hand_1.clear()
        hidden = 0
        for i in player_1:
            rank = i[0]
            suit = i[1]
            player_hand_1.append(Cards(rank, suit, player_card_x_s1, p_cardy, hidden))
            player_card_x_s1 += 120
        p_points_1 = point_calculator(player_1)

    if split_hand == 2:
        player_hand_2.clear()
        hidden = 0
        for i in player_2:
            rank = i[0]
            suit = i[1]
            player_hand_2.append(Cards(rank, suit, player_card_x_s2, p_cardy, hidden))
            player_card_x_s2 += 120
        p_points_2 = point_calculator(player_2)


    if split_hand == 0:
        deal_cards(player, deck)
        player_hand.clear()
        hidden = 0
        for i in player:
            rank = i[0]
            suit = i[1]
            player_hand.append(Cards(rank, suit, player_card_x, p_cardy, hidden))
            player_card_x += 120
        p_points = point_calculator(player)
    return p_points, p_points_1, p_points_2
def do_dealer_deal():
    global d_points,dealer_card_x
    deal_cards(dealer,deck)
    dealer_hand.clear()
    hidden = 0
    for i in dealer:
        rank = i[0]
        suit = i[1]
        dealer_hand.append(Cards(rank,suit,dealer_card_x,150,hidden))
        dealer_card_x += 120
        hidden = 1
    d_points = point_calculator(dealer)
    return d_points
def deal():
    global cards_in_deck,player_card_x,dealer_card_x,player_card_number,player_card_hit_x,double_hit,player_turn_end,bet,bet_active,game_started,deal_hit,dealer_card_hit_x,money,d_points,p_points,split_hand,split_hit,player_card_x_s1,player_card_x_s2,player_card_hit_x_s1,player_card_hit_x_s2
    if not deal_hit and bet != 0:
        do_player_deal()
        do_dealer_deal()
        cards_in_deck = len(deck)
        player_card_x = 655
        dealer_card_x = 655
        player_card_x_s1 = 395
        player_card_x_s2 = 895
        player_card_number = 2
        player_card_hit_x = 895
        player_card_hit_x_s1 = 635
        player_card_hit_x_s2 = 1135
        double_hit = 0
        player_turn_end = False
        game_started = True
        bet_active = False
        deal_hit = True
        split_hit = False
        if p_points == 21:
            stand()
        split_hand = 0


def hit():
    global player_card_hit_x,dealer_card_hit_x,player_card_hit_x_s1,player_card_hit_x_s2,player_card_number,p_points,p_points_1,p_points_2,d_points,cards_in_deck,player_turn_end,bet_active,bet,bet_1,bet_2,deal_hit,money,split_hand,cooldown
    hidden = 0
    p_points = point_calculator(player)
    if game_started:
        if split_hand == 0:
            if p_points < 21:
                player.append(deck.pop())
                player_hand.append(Cards(player[player_card_number][0], player[player_card_number][1], player_card_hit_x, p_cardy, hidden))
                player_card_number += 1
                player_card_hit_x += 120
                p_points = point_calculator(player)
            if p_points > 21:
                dealer_hand[1].reveal()
                player_turn_end = True
                bet_active = True
                bet = 0
                deal_hit = False
            if p_points == 21:
                dealer_hand[1].reveal()
                dealer.append(deck.pop())
                dealer_new_card = dealer[-1]
                dealer_hand.append(Cards(dealer_new_card[0], dealer_new_card[1], dealer_card_hit_x, 150, hidden))
                dealer_card_hit_x += 120
                d_points = point_calculator(dealer)
                if p_points == d_points:
                    print("Draw")
                elif p_points > d_points and d_points < 21:
                    money += bet * 2
                player_turn_end = True
                bet = 0
                bet_active = True
                deal_hit = False

        if split_hand == 1:
            if p_points_1 < 21:
                player_1.append(deck.pop())
                player_hand_1.append(Cards(player_1[player_card_number][0], player_1[player_card_number][1], player_card_hit_x_s1,p_cardy, hidden))
                player_card_number += 1
                player_card_hit_x_s1 += 120
                p_points_1 = point_calculator(player_1)
            if p_points_1 > 21:
                player_card_number = 2
                split_hand += 1
            if p_points_1 == 21:
                player_card_number = 2
                split_hand += 1
            cooldown = pg.time.get_ticks()
            print(f"split_hand is {split_hand}")

        if split_hand == 2 and pg.time.get_ticks() - cooldown > 20:
            if p_points_2 < 21:
                player_2.append(deck.pop())
                player_hand_2.append(Cards(player_2[player_card_number][0], player_2[player_card_number][1], player_card_hit_x_s2,p_cardy, hidden))
                player_card_number += 1
                player_card_hit_x_s2 += 120
                p_points_2 = point_calculator(player_2)
            if p_points_2 > 21:
                dealer_hand[1].reveal()
                player_turn_end = True
                bet_active = True
                bet_2 = 0
                deal_hit = False
                bet_1 = 0
                check_winner(p_points_1,bet_1)
            if p_points_2 == 21:
                dealer_hand[1].reveal()
                dealer.append(deck.pop())
                dealer_new_card = dealer[-1]
                dealer_hand.append(Cards(dealer_new_card[0], dealer_new_card[1], dealer_card_hit_x, 150, hidden))
                dealer_card_hit_x += 120
                d_points = point_calculator(dealer)
                if p_points_1 == d_points:
                    print("Pair one is a draw")
                elif p_points_1 > d_points and d_points < 21:
                    money += bet_1 * 2
                if p_points_2 == d_points:
                    print("Pair two is a draw")
                elif p_points_2 > d_points and d_points < 21:
                    money += bet_2 * 2
                player_turn_end = True
                bet_1 = 0
                bet_2 = 0
                bet_active = True
                # cards_in_deck = len(deck)
                deal_hit = False
        cards_in_deck = len(deck)
def split_cards():
    global player_1,player_2,player_hand_1,player_hand_2,split_hand,p_points,player_card_number,player_card_hit_x,player_turn_end,bet_active,bet,bet_1,bet_2,money,dealer_card_hit_x,p_points_1,p_points_2,split_hit,cards_in_deck
    split_hit = True
    player_1.extend([player.pop(0),deck.pop()])
    player_2.extend([player.pop(),deck.pop()])
    del player_hand[:]
    p_points_1 = point_calculator(player_1)
    p_points_2 = point_calculator(player_2)
    split_hand += 1
    money -= bet
    if split_hand == 1:
        do_player_deal()
        bet_1 = bet
        split_hand += 1
    if split_hand == 2:
        do_player_deal()
        bet_2 = bet
        split_hand = 1
        if p_points_1 == 21:
            split_hand = 2
        elif p_points_2 == 21:
            stand()
    cards_in_deck = len(deck)
    bet = 0


def check_winner(hand_points,hand_bet):
    global money,bet_active,deal_hit
    if d_points < hand_points < 22:
        money += hand_bet * 2
        bet_active = True
        deal_hit = False
    elif hand_points == d_points:
        money += hand_bet
        bet_active = True
        deal_hit = False
    elif d_points > hand_points and d_points > 21:
        money += hand_bet * 2
        bet_active = True
        deal_hit = False
    elif hand_points > 21:
        bet_active = True
        deal_hit = False
    else:
        bet_active = True
        deal_hit = False

def stand():
    global d_points,deck,p_points,dealer_card_hit_x,cards_in_deck,player_turn_end,bet_active,deal_hit,split_hand,bet,bet_1,bet_2,player_card_number
    if game_started:
        if split_hand == 1:
            player_card_number = 2
            split_hand += 1
        elif split_hand == 2:
            while d_points < 18 and p_points_1 < 21 or d_points < 18 and p_points_2 < 21:
                dealer.append(deck.pop())
                dealer_new_card = dealer[-1]
                dealer_hand.append(Cards(dealer_new_card[0], dealer_new_card[1], dealer_card_hit_x, 150, hidden))
                dealer_card_hit_x += 120
                d_points = point_calculator(dealer)
            dealer_card_hit_x = 895
            check_winner(p_points_1,bet_1)
            check_winner(p_points_2,bet_2)
            cards_in_deck = len(deck)
            player_turn_end = True
            dealer_hand[1].reveal()
            bet_active = True
            deal_hit = False
            bet_1 = 0
            bet_2 = 0
        elif split_hand == 0:
            while d_points < 18 and d_points < p_points < 21:
                dealer.append(deck.pop())
                dealer_new_card = dealer[-1]
                dealer_hand.append(Cards(dealer_new_card[0], dealer_new_card[1], dealer_card_hit_x, 150, hidden))
                dealer_card_hit_x += 120
                d_points = point_calculator(dealer)
            dealer_card_hit_x = 895
            check_winner(p_points,bet)
            bet = 0
            cards_in_deck = len(deck)
            player_turn_end = True
            dealer_hand[1].reveal()
            bet_active = True
            deal_hit = False

def double():
    global player_card_hit_x,player_card_hit_x_s1,player_card_hit_x_s2,dealer_card_hit_x,p_points,p_points_1,p_points_2,player_card_number,d_points,double_hit,bet_active,bet,bet_1,bet_2,money,split_hand,cooldown
    bet_active = False
    hidden = 0
    if split_hand == 0:
        if double_hit == 0 and player_card_number == 2 and money >= bet:
            money -= bet
            bet *= 2
            player.append(deck.pop())
            player_hand.append(Cards(player[player_card_number][0], player[player_card_number][1], player_card_hit_x, p_cardy, hidden))
            player_card_hit_x += 120
            p_points = point_calculator(player)
            double_hit += 1
            player_card_number += 1
            stand()
    if split_hand == 1:
        if double_hit == 0 and player_card_number == 2 and money >= bet_1:
            money -= bet_1
            bet_1 *= 2
            player_1.append(deck.pop())
            player_hand_1.append(Cards(player_1[player_card_number][0], player_1[player_card_number][1], player_card_hit_x_s1, p_cardy, hidden))
            player_card_hit_x_s1 += 120
            p_points_1 = point_calculator(player_1)
            split_hand += 1
        cooldown = pg.time.get_ticks()
        print(f"double hit is {double_hit}")

    if split_hand == 2 and pg.time.get_ticks() - cooldown > 20:
        if double_hit == 0 and player_card_number == 2 and money >= bet_2:
            money -= bet_2
            bet_2 *= 2
            player_2.append(deck.pop())
            player_hand_2.append(Cards(player_2[player_card_number][0], player_2[player_card_number][1], player_card_hit_x_s2, p_cardy, hidden))
            player_card_hit_x_s2 += 120
            p_points_2 = point_calculator(player_2)
            double_hit += 1
            player_card_number += 1
            stand()


def reset():
    global deck,p_points,d_points,player_card_x,dealer_card_x,cards_in_deck,double_hit,player_turn_end,bet,bet_1,bet_2,bet_active,game_started,money,deal_hit,split_hand,split_hit
    del deck[:],player[:],dealer[:],player_hand[:],dealer_hand[:],player_hand_1[:],player_hand_2[:]
    bet = 0
    bet_1 = 0
    bet_2 = 0
    for i in range(decks_amount):
        for r in rank:
            for s in suit:
                pair = r + s
                deck.append(pair)
        shuffle(deck)
    cards_in_deck = len(deck)
    player_card_x = 655
    dealer_card_x = 655
    p_points = point_calculator(player)
    d_points = point_calculator(dealer)
    double_hit = 0
    player_turn_end = False
    bet_active = True
    game_started = False
    money = 500
    deal_hit = False
    split_hand = 0
    split_hit = False



font = pg.font.SysFont("arial", 26,bold=True)
big_font = pg.font.SysFont("arial", 90,bold=True)
deal_image = pg.image.load("../img/deal_button.png")
chip_5 = pg.image.load("../img/bet_chip_5.png")
chip_10 = pg.image.load("../img/bet_chip_10.png")
chip_25 = pg.image.load("../img/bet_chip_25.png")
chip_50 = pg.image.load("../img/bet_chip_50.png")
hit_image = pg.image.load("../img/hit_button.png")
money_image = pg.image.load("../img/money_button.png")
stand_image = pg.image.load("../img/stand_button.png")
double_image = pg.image.load("../img/double_button.png")
reset_image = pg.image.load("../img/reset_button.png")
bet_image = pg.image.load("../img/bet_button.png")
all_in_image = pg.image.load("../img/bet_chip_all_in.png")
chip_clear_image = pg.image.load("../img/bet_chip_clear.png")
split_image = pg.image.load("../img/split_button.png")
arrow_image = pg.image.load("../img/arrow.png")
split_bet_image = pg.image.load("../img/split_bet_button.png")
class Cards:
    def __init__(self,rank,suit,x,y,hidden):
        self.rank = rank
        self.suit = suit
        self.hidden = hidden
        if hidden == 1:
            self.image = pg.image.load("../img/back.png")
        else:
            self.image = pg.image.load(f"img/{rank}{suit}.png")
        self.card = self.rank + self.suit
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def draw(self):
        screen.blit(self.image,self.rect)
    def reveal(self):
        self.hidden = 0
        self.image = pg.image.load(f"img/{self.rank}{self.suit}.png")

#First cards display
#Player cards display
cards_in_deck = len(deck)
class Button:
    def __init__(self, x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def draw(self):
        screen.blit(self.image,self.rect)
    def is_clicked(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False

deal_button = Button(1400,600,deal_image,0.2)
hit_button = Button(750,700,hit_image,0.2)
money_button = Button(120,100,money_image,0.2)
stand_button = Button(950,700,stand_image,0.2)
double_button = Button(550,700,double_image,0.2)
reset_button = Button(150,700,reset_image,0.2)
bet_5 = Button(1005,700,chip_5,0.175)
bet_10 = Button(1100,700,chip_10,0.175)
bet_25 = Button(1195,700,chip_25,0.175)
bet_50 = Button(1290,700,chip_50,0.175)
bet_button = Button(320,100,bet_image,0.2)
all_in_chip = Button(1385,700,all_in_image,0.175)
clear_chip = Button(1480,700,chip_clear_image,0.175)
split_button = Button(750,600,split_image,0.2)
arrow_button_1 = Button(550,300,arrow_image,0.2)
arrow_button_2 = Button(1000,300,arrow_image,0.2)
split_bet_button = Button(320,100,split_bet_image,0.12)



#else
running = True
paused = False
while running:
    for event in pg.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if not deal_hit and deal_button.is_clicked(event):
                if len(deck) >= 4:
                    deal()
                else:
                    pass
            if deal_hit and not player_turn_end and hit_button.is_clicked(event):
                hit()
            if reset_button.is_clicked(event):
                reset()
            if bet_active:
                if clear_chip.is_clicked(event):
                    money += bet
                    bet = 0
                    del player[:], dealer[:], player_hand[:], dealer_hand[:],player_1[:], player_hand_1[:], player_2[:], player_hand_2[:]
                    p_points = 0
                    split_hand = 0
                if bet_5.is_clicked(event) and money >= 5:
                    bet += 5
                    money -= 5
                    del player[:], dealer[:], player_hand[:], dealer_hand[:],player_1[:], player_hand_1[:], player_2[:], player_hand_2[:]
                    p_points = 0
                    split_hand = 0
                if bet_10.is_clicked(event) and money >= 10:
                    bet += 10
                    money -= 10
                    del player[:], dealer[:], player_hand[:], dealer_hand[:],player_1[:], player_hand_1[:], player_2[:], player_hand_2[:]
                    p_points = 0
                    split_hand = 0
                if bet_25.is_clicked(event) and money >= 25:
                    bet += 25
                    money -= 25
                    del player[:], dealer[:], player_hand[:], dealer_hand[:],player_1[:], player_hand_1[:], player_2[:], player_hand_2[:]
                    p_points = 0
                    split_hand = 0
                if bet_50.is_clicked(event) and money >= 50:
                    bet += 50
                    money -= 50
                    del player[:], dealer[:], player_hand[:], dealer_hand[:],player_1[:], player_hand_1[:], player_2[:], player_hand_2[:]
                    p_points = 0
                    split_hand = 0
                if all_in_chip.is_clicked(event) and money != 0:
                    bet += money
                    money = 0
                    split_hand = 0
                    del player[:], dealer[:], player_hand[:], dealer_hand[:],player_1[:], player_hand_1[:], player_2[:], player_hand_2[:]
                    p_points = 0
            if deal_hit and double_hit == 0 and p_points != 21 and not bet_active and double_button.is_clicked(event):
                double()
            if (deal_hit and p_points > 0 and stand_button.is_clicked(event)) or (deal_hit and p_points_1 > 0 and p_points_2 > 0 and stand_button.is_clicked(event)):
                stand()
            if game_started and deal_hit and split_hit == False and len(player) == 2 and money >= bet and player[0][0] == player[1][0] and split_button.is_clicked(event):
                split_cards()

        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                paused = not paused
            elif event.key == pg.K_BACKSPACE:
                running = False




    if not paused:
        screen.fill(bg_color)
        # shapes
        pg.draw.circle(screen, color, (768, 0), 780)
        pg.draw.circle(screen, (255, 255, 255), (768, 0), 770, 3)
        pg.draw.circle(screen, (0, 0, 0), (768, 0), 780, 10)

        if not deal_hit:
            deal_button.draw()
        if deal_hit and not player_turn_end:
                hit_button.draw()
        money_button.draw()
        if game_started and deal_hit and split_hit == False and len(player) == 2 and player[0][0] == player[1][0]:
            split_button.draw()

        if deal_hit and p_points > 0 or deal_hit and p_points_1 > 0 and p_points_2 > 0:
            stand_button.draw()

        if deal_hit and double_hit == 0 and p_points != 21 and not bet_active:
            double_button.draw()
        reset_button.draw()
        if bet_active:
             clear_chip.draw()
             bet_5.draw() and money >= 5
             bet_10.draw() and money >= 10
             bet_25.draw() and money >= 25
             bet_50.draw() and money >= 50
             all_in_chip.draw() and money != 0
        if split_hand == 1:
            arrow_button_1.draw()
        elif split_hand == 2:
            arrow_button_2.draw()
        if split_hand == 0:
            bet_button.draw()
            bet_number = font.render(f"£{bet}", True, (240, 215, 140))
            screen.blit(bet_number, (300, 100))
        elif split_hand == 1 or split_hand == 2:
            split_bet_button.draw()
            bet_number_1 = font.render(f"£{bet_1}", True, (240, 215, 140))
            screen.blit(bet_number_1, (250, 100))
            bet_number_2 = font.render(f"£{bet_2}", True, (240, 215, 140))
            screen.blit(bet_number_2, (350, 100))

        money_number = font.render(f"£{money}", True, (240, 215, 140))
        screen.blit(money_number, (85, 100))

        if split_hand == 0:
            player_points = font.render(f"Player points: {p_points}", True, (240, 215, 140))
            screen.blit(player_points, (1200, 200))
        elif split_hand == 1 or split_hand == 2:
            player_1_points = font.render(f"Hand 1 points: {p_points_1}", True, (240, 215, 140))
            screen.blit(player_1_points, (1200, 170))
            player_2_points = font.render(f"Hand 2 points: {p_points_2}", True, (240, 215, 140))
            screen.blit(player_2_points, (1200, 230))
        if money == 0 and bet == 0:
            loser_text = big_font.render("YOU LOSE BROKEY!!", True, (240, 215, 140))
            screen.blit(loser_text, (screen_width / 6, screen_height / 4))
        if not player_turn_end and len(dealer) > 0:
            dealer_points = font.render(f"Dealer points: {point_calculator([dealer[0]])} + ???", True, (240, 215, 140))
            screen.blit(dealer_points, (1200, 100))
        elif not game_started:
            dealer_points = font.render(f"Dealer points: 0", True, (240, 215, 140))
            screen.blit(dealer_points, (1200, 100))
        elif player_turn_end:
            dealer_points = font.render(f"Dealer points: {point_calculator(dealer)}", True, (240, 215, 140))
            screen.blit(dealer_points, (1200, 100))

        deck_cards = font.render(f"Cards left: {cards_in_deck}", True, (240, 215, 140))
        screen.blit(deck_cards, (1200, 300))

#Draws the cards for respective hand
        for p in player_hand:
            p.draw()
        for d in dealer_hand:
            d.draw()
        for p in player_hand_1:
            p.draw()
        for p in player_hand_2:
            p.draw()

    else:
        text_paused = big_font.render("GAME PAUSED", True, (240, 215, 140))
        text_paused_rect = text_paused.get_rect(center=(screen_width / 2 - 200, screen_height / 2 - 100))
        screen.blit(text_paused, text_paused_rect)

    pg.display.flip()
    clock.tick(60)

pg.quit()