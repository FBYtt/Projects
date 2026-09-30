import pygame as pg
from random import shuffle

#screen stuff
screen_width, screen_height = 1920, 1000
screen_scale = 0.8
screen = pg.display.set_mode((screen_width * screen_scale,screen_height * screen_scale))
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
split_hand = 1
hidden = 0
p_points = 0
d_points = 0
cards_in_deck = 0
double_hit = 0
bet = 0
bet_active = True
player_turn_end = False
game_started = False
decks_amount = 4
player_card_x = 655
dealer_card_x = 655
#for hit button
player_card_hit_x = 895
dealer_card_hit_x = 895
player_card_number = 2

money = 500
p_cardy = 550
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
    global p_points
    global player_card_x
    deal_cards(player,deck)
    player_hand.clear()
    hidden = 0
    for i in player:
        rank = i[0]
        suit = i[1]
        player_hand.append(Cards(rank,suit,player_card_x,550,hidden))
        player_card_x += 120
    p_points = point_calculator(player)
    return p_points
def do_dealer_deal():
    global d_points
    global dealer_card_x
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
    global cards_in_deck
    global player_card_x
    global dealer_card_x
    global player_card_number
    global player_card_hit_x
    global double_hit
    global player_turn_end
    global bet
    global bet_active
    global game_started
    global deal_hit
    if not deal_hit and bet != 0:
        do_player_deal()
        do_dealer_deal()
        cards_in_deck = len(deck)
        player_card_x = 655
        dealer_card_x = 655
        player_card_number = 2
        player_card_hit_x = 895
        double_hit = 0
        player_turn_end = False
        game_started = True
        bet_active = False
        deal_hit = True

def hit():
    global player_card_hit_x
    global dealer_card_hit_x
    global player_card_number
    global p_points
    global d_points
    global cards_in_deck
    global player_turn_end
    global bet_active
    global bet
    global deal_hit
    hidden = 0
    p_points = point_calculator(player)
    if game_started:
        if p_points < 21:
            player.append(deck.pop())
            player_hand.append(Cards(player[player_card_number][0], player[player_card_number][1], player_card_hit_x, 550, hidden))
            player_card_number += 1
            player_card_hit_x += 120
            p_points = point_calculator(player)
        if p_points == 21 or p_points == 0:
            player_card_number = 2
            player_card_hit_x = 895
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

        cards_in_deck = len(deck)
        p_points = point_calculator(player)
        d_points = point_calculator(dealer)
        if not player_turn_end:
            bet_active = False

def split_cards():
    global player_1
    global player_2
    global split_hand
    global p_points
    global player_card_number
    global player_card_hit_x
    global player_turn_end
    global bet_active
    global bet
    global dealer_card_hit_x
    player_2.append(player[1])
    player_2.append(deck.pop())
    if split_hand == 1:
        if p_points < 21:
            player_1.append(player[0])
            player_1.append(deck.pop())
            player_hand_1.append(Cards(player_1[player_card_number][0], player_1[player_card_number][1], player_card_hit_x, 550, hidden))
            player_card_number += 1
            player_card_hit_x += 120
            p_points = point_calculator(player_1)
        if p_points == 21 or p_points == 0:
            player_card_number = 2
            player_card_hit_x = 895
        if p_points > 21:
            dealer_hand[1].reveal()
            player_turn_end = True
            bet_active = True
            bet = 0
        if p_points == 21:
            dealer_hand[1].reveal()
            dealer.append(deck.pop())
            dealer_new_card = dealer[-1]
            dealer_hand.append(Cards(dealer_new_card[0], dealer_new_card[1], dealer_card_hit_x, 150, hidden))
            dealer_card_hit_x += 120
            d_points = point_calculator(dealer)
            if p_points == d_points:
                print("Draw")
        split_hand += 1
    if split_hand == 2:
        if p_points < 21:
            player_2.append(player[0])
            player_2.append(deck.pop())
            player_hand_2.append(Cards(player_2[player_card_number][0], player_2[player_card_number][1], player_card_hit_x, 550, hidden))
            player_card_number += 1
            player_card_hit_x += 120
            p_points = point_calculator(player_2)
        if p_points == 21 or p_points == 0:
            player_card_number = 2
            player_card_hit_x = 895
        if p_points > 21:
            dealer_hand[1].reveal()
            player_turn_end = True
            bet_active = True
            bet = 0
        if p_points == 21:
            dealer_hand[1].reveal()
            dealer.append(deck.pop())
            dealer_new_card = dealer[-1]
            dealer_hand.append(Cards(dealer_new_card[0], dealer_new_card[1], dealer_card_hit_x, 150, hidden))
            dealer_card_hit_x += 120
            d_points = point_calculator(dealer)
            if p_points == d_points:
                print("Draw")







def check_winner(hand_points):
    global money
    global bet
    global bet_active
    global deal_hit
    if d_points < hand_points < 22:
        print("Player wins!")
        money += bet * 2
        bet = 0
        bet_active = True
        deal_hit = False
    elif hand_points == d_points:
        print("Draw!")
        money += bet
        bet = 0
        bet_active = True
        deal_hit = False
    elif d_points > hand_points and d_points > 21:
        print("Player wins!")
        money += bet * 2
        bet = 0
        bet_active = True
        deal_hit = False
    elif hand_points > 21:
        print("Dealer wins!")
        bet = 0
        bet_active = True
        deal_hit = False
    else:
        bet = 0
        bet_active = True
        deal_hit = False
def stand():
    global d_points
    global deck
    global p_points
    global dealer_card_hit_x
    global cards_in_deck
    global player_turn_end
    global bet_active
    global deal_hit
    if game_started:
        while d_points < 18 and p_points < 21:
            dealer.append(deck.pop())
            dealer_new_card = dealer[-1]
            dealer_hand.append(Cards(dealer_new_card[0], dealer_new_card[1], dealer_card_hit_x, 150, hidden))
            dealer_card_hit_x += 120
            d_points = point_calculator(dealer)
        dealer_card_hit_x = 895
        check_winner(p_points)
        cards_in_deck = len(deck)
        player_turn_end = True
        dealer_hand[1].reveal()
        bet_active = True
        deal_hit = False


def split_hand():
    pass
def double():
    global player_card_hit_x
    global dealer_card_hit_x
    global player_card_number
    global p_points
    global d_points
    global double_hit
    global player_card_number
    global bet_active
    global money
    global bet
    bet_active = False
    hidden = 0
    if double_hit == 0 and player_card_number == 2:
        money -= bet
        bet *= 2
        player.append(deck.pop())
        player_hand.append(Cards(player[player_card_number][0], player[player_card_number][1], player_card_hit_x, 550, hidden))
        player_card_hit_x += 120
        p_points = point_calculator(player)
        double_hit += 1
        player_card_number += 1
        stand()



def reset():
    global deck
    global p_points
    global d_points
    global player_card_x
    global dealer_card_x
    global cards_in_deck
    global double_hit
    global player_turn_end
    global bet
    global bet_active
    global game_started
    global money
    global deal_hit
    del deck[:]
    del player[:]
    del dealer[:]
    del player_hand[:]
    del dealer_hand[:]
    bet = 0
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
empty_button_image = pg.image.load("../img/empty_button.png")
bet_image = pg.image.load("../img/bet_button.png")
all_in_image = pg.image.load("../img/bet_chip_all_in.png")
chip_clear_image = pg.image.load("../img/bet_chip_clear.png")
split_image = pg.image.load("../img/split_button.png")

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
        self.clicked = False
    def draw(self):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
        screen.blit(self.image, self.rect)
        return action

deal_button = Button(200,400,deal_image,0.2)
hit_button = Button(400,400,hit_image,0.2)
money_button = Button(150,100,money_image,0.2)
stand_button = Button(700,300,stand_image,0.2)
double_button = Button(200,500,double_image,0.2)
reset_button = Button(400,500,reset_image,0.2)
empty_bet_button = Button(900,500,empty_button_image,0.2)
bet_5 = Button(900,700,chip_5,0.2)
bet_10 = Button(1010,700,chip_10,0.2)
bet_25 = Button(1120,700,chip_25,0.2)
bet_50 = Button(1230,700,chip_50,0.2)
bet_button = Button(350,100,bet_image,0.2)
all_in_chip = Button(1340,700,all_in_image,0.2)
clear_chip = Button(1450,700,chip_clear_image,0.2)
split_button = Button(300,600,split_image,0.22)


#image load and xy for player

#image load xy for dealer


#else
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False



    screen.fill(bg_color)
    #shapes
    pg.draw.circle(screen, color,(720, 0),780)
    pg.draw.circle(screen, (255,255,255),(720, 0),770,3)
    pg.draw.circle(screen, (0,0,0),(720,0),780, 10)

    if deal_button.draw():
        if len(deck) > 4:
             deal()
        else:
            print("Empty")
    if hit_button.draw():
        if len(deck) > 0:
            hit()
    money_button.draw()
    bet_button.draw()
    if game_started:
       if player[0][0] == player [1][0]:
          if split_button.draw():
             split_cards()
    if stand_button.draw():
        stand()
    if double_button.draw() and game_started:
        double()
    if reset_button.draw():
        reset()
    if bet_active:
        if clear_chip.draw():
            money += bet
            bet = 0
        if bet_5.draw() and money >= 5:
            bet += 5
            money -= 5
        if bet_10.draw() and money >= 10:
            bet += 10
            money -= 10
        if bet_25.draw() and money >= 25:
            bet += 25
            money -= 25
        if bet_50.draw() and money >= 50:
            bet += 50
            money -= 50
        if all_in_chip.draw() and money != 0:
            bet += money
            money = 0
    money_number = font.render(f"£{money}", True, (240, 215, 140))
    screen.blit(money_number,(125,100))
    bet_number = font.render(f"£{bet}",True,(240,215,140))
    screen.blit(bet_number,(330  ,100))
    player_points = font.render(f"Player points: {p_points}", True, (240, 215, 140))
    screen.blit(player_points,(1200,200))
    if money == 0 and bet == 0:
        loser_text = big_font.render("YOU LOSE BROKEY!!", True, (240, 215, 140))
        screen.blit(loser_text, (screen_width/6,screen_height/4))
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
    screen.blit(deck_cards,(1000,100),)
    for p in player_hand:
        p.draw()
    for d in dealer_hand:
        d.draw()


    pg.display.flip()
    clock.tick(60)

pg.quit()