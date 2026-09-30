import pygame as pg
from random import shuffle
#screen stuff
screen = pg.display.set_mode((1440,810))
pg.display.set_caption("Black Jack")
clock = pg.time.Clock()


pg.init()
#Lists
player = []
dealer = []
deck = []
cards_in_deck = 0
decks_amount = 4
#for hit button
x = 895
card_number = 2

money = 100
extrax = 230
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
for _ in range(2):
    player.append(deck.pop())
    dealer.append(deck.pop())

#functions
def point_calculator(hand):
    points = 0
    acecounter = 0
    for _ in hand:
        n = _.split()
        n = n[-1][0]
        if n == "A":
            points += 11
            acecounter += 1
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
    while points > 21 and acecounter > 0:
        points -= 10
        acecounter -= 1
    return points


def redeal_cards(hand,deck):
    del hand[:]
    for _ in range(2):
        hand.append(deck.pop())

def do_player_redeal():
    global p_points
    global player_cardx
    redeal_cards(player,deck)
    player_hand.clear()
    x = 655
    hidden = 0
    for i in player:
        rank = i[0]
        suit = i[1]
        player_hand.append(Cards(rank,suit,x,550,hidden))
        x += 120
    p_points = point_calculator(player)
    return p_points
def do_dealer_redeal():
    global d_points
    redeal_cards(dealer,deck)
    dealer_hand.clear()
    x = 655
    hidden = 0
    for i in dealer:
        rank = i[0]
        suit = i[1]
        dealer_hand.append(Cards(rank,suit,x,150,hidden))
        x += 120
        hidden = 1
    d_points = point_calculator(dealer)
    return d_points
def redeal():
    global cards_in_deck
    do_player_redeal()
    do_dealer_redeal()
    cards_in_deck = len(deck)
def hit():
    global x
    global card_number
    global cards_in_deck
    p_points = point_calculator(player)
    if p_points < 21:
        player.append(deck.pop())
        player_hand.append(Cards(player[card_number][0], player[card_number][1], x, 550, hidden))
        card_number += 1
        x += 120
        p_points = point_calculator(player)
    if p_points >= 21 or 0:
        card_number = 2
        x = 895
    cards_in_deck = len(deck)

def reset():
    global deck
    global cards_in_deck
    del deck[:]
    del player[:]
    del dealer[:]
    del player_hand[:]
    del dealer_hand[:]
    for i in range(decks_amount):
        for r in rank:
            for s in suit:
                pair = r + s
                deck.append(pair)
        shuffle(deck)
    for _ in range(2):
        player.append(deck.pop())
        dealer.append(deck.pop())
    hidden = 0
    x = 655
    for i in player:
        card_rank = i[0]
        card_suit = i[1]
        player_hand.append(Cards(card_rank, card_suit, x, 550, hidden))
        x += 120
    x = 655
    for i in dealer:
        card_rank = i[0]
        card_suit = i[1]
        dealer_hand.append(Cards(card_rank, card_suit, x, 150, hidden))
        x += 120
        hidden += 1
    cards_in_deck = len(deck)
def stand():
    pass





font = pg.font.SysFont("arial", 26,bold=True)
redeal_image = pg.image.load("../img/redeal_button.png")
hit_image = pg.image.load("../img/hit_button.png")
money_image = pg.image.load("../img/money_button.png")
stand_image = pg.image.load("../img/stand_button.png")
double_image = pg.image.load("../img/double_button.png")
reset_image = pg.image.load("../img/reset_button.png")
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

#First cards display
#Player cards display
hidden = 0
player_hand = []
x = 655
for i in player:
    card_rank = i[0]
    card_suit = i[1]
    player_hand.append(Cards(card_rank, card_suit,x,550,hidden))
    x += 120
#Dealer cards display
dealer_hand = []
x = 655
for i in dealer:
    card_rank = i[0]
    card_suit = i[1]
    dealer_hand.append(Cards(card_rank, card_suit, x, 150,hidden))
    x += 120
    hidden += 1
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

redeal_button = Button(250,250,redeal_image,0.2)
hit_button = Button(400,400,hit_image,0.2)
money_button = Button(150,100,money_image,0.2)
stand_button = Button(800,800,stand_image,0.2)
double_button = Button(1000,1000,double_image,0.2)
reset_button = Button(400,600,reset_image,0.2)


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

    if redeal_button.draw():
        if len(deck) > 4:
             redeal()
        else:
            print("Empty")
    if hit_button.draw():
        if len(deck) > 0:
            hit()

    money_button.draw()
    stand_button.draw()
    double_button.draw()
    if reset_button.draw():
        reset()
    money_number = font.render(f"{money}", True, (240, 215, 140))
    screen.blit(money_number,(125,100),)
    deck_cards = font.render(f"{cards_in_deck}", True, (240, 215, 140))
    screen.blit(deck_cards,(1000,100),)
    for p in player_hand:
        p.draw()
    for d in dealer_hand:
        d.draw()


    pg.display.flip()
    clock.tick(60)

pg.quit()