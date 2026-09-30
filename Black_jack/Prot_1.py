import pygame as pg
from random import shuffle



pg.init()
#Lists
player = []
dealer = []
deck = []
money = 100

#functions
def redeal_cards(hand,deck):
    del hand[:]
    for _ in range(2):
        hand.append(deck.pop())
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
def do_player_redeal():
    global p_card1, p_card2, p_points
    p_card1, p_card2, p_points = redeal_cards(player,deck)
def do_dealer_redeal():
    global d_card1, d_card2, d_points
    d_card1, d_card2, d_points = redeal_cards(dealer,deck)

def redeal():
    do_player_redeal()
    do_dealer_redeal()
#Button
buttons = [
    {"rect": pg.Rect(200,200,100,100),"label":"Redeal","action": redeal},
    ]
money_button = pg.Rect(200,400,100,100)
clicked = False
#screen stuff
screen = pg.display.set_mode((1440,810))
pg.display.set_caption("Black Jack")
clock = pg.time.Clock()
color = (0, 128, 60)
bg_color = (139,0,0)
font = pg.font.SysFont("arial", 28)
redeal_text = font.render("Redeal", True, (255, 255, 255))
redeal_rect = redeal_text.get_rect()
redeal_rect.center = buttons[0]["rect"].center
money_text = font.render(" Money", True, (255, 255, 255))


#Deck shuffler
cards = ["2","3","4","5","6","7","8","9","Z","J","Q","K","A"]# Z=10 for simpler code
suite = ["C", "D", "H", "S"]
for _ in range(4):

    for suit in suite:
        for card in cards:
            pair = card + suit
            deck.append(pair)
shuffle(deck)

for i in range(2):
    player.append(deck.pop())
    dealer.append(deck.pop())

p_points = point_calculator(player)
d_points = point_calculator(dealer)

#image load and xy for player
p_card1 = pg.image.load(f"img/{player[0]}.png")
p_card2 = pg.image.load(f"img/{player[1]}.png")
p_card_rect1 = p_card1.get_rect()
p_card_rect2 = p_card2.get_rect()
p_card_rect1.midleft = (550,450)
p_card_rect2.midright = (750,450)
#image load xy for dealer
d_card1 = pg.image.load(f"img/{dealer[0]}.png")
d_card2 = pg.image.load("../img/back.png")
d_card_rect1 = d_card1.get_rect()
d_card_rect2 = d_card2.get_rect()
d_card_rect1.topleft = (550,150)
d_card_rect2.topright = (750,150)
background = pg.image.load("../img/background.jpg")

#else







running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            for b in buttons:
                if len(deck) > 0:
                    if b["rect"].collidepoint(pg.mouse.get_pos()):
                        b["action"]()
                else:
                    break

    screen.fill(bg_color)



    #shapes
    pg.draw.circle(screen, color,(720, 0),780)
    pg.draw.circle(screen, (255,255,255),(720, 0),770,3)
    pg.draw.circle(screen, (0,0,0),(720,0),780, 10)
    screen.blit(p_card1,p_card_rect1)
    screen.blit(p_card2,p_card_rect2)
    screen.blit(d_card1,d_card_rect1)
    screen.blit(d_card2,d_card_rect2)
    pg.draw.rect(screen, (0,0,0), buttons[0]["rect"])
    pg.draw.rect(screen, (0,0,0), money_button)
    screen.blit(redeal_text, redeal_rect)
    screen.blit(money_text,(200,400))
    money_number = font.render(f"   {money}", True, (255, 255, 255))
    screen.blit(money_number,(200,450))



    pg.display.flip()
    clock.tick(60)

pg.quit()