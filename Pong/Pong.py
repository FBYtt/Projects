import pygame as pg
import random



pg.init()

screen_width = pg.display.get_desktop_sizes()[0][0]
screen_height = pg.display.get_desktop_sizes()[0][1]
print(screen_width, screen_height)

screen = pg.display.set_mode((screen_width,screen_height),pg.RESIZABLE)
clock = pg.time.Clock()
paddle_left_x = 0
scale_x = screen_width / 1536
scale_y = screen_height / 864
#constants
score_left = 0
score_right = 0
game_state = "menu"
paddle_width = 20 * scale_x
paddle_height = 150 * scale_y
ball_radious = 17 * ((scale_x + scale_y) / 2)
ball_outline = 3 * ((scale_x + scale_y) / 2)
small_font = 30 * ((scale_x + scale_y) / 2)
big_font = 220 * ((scale_x + scale_y) / 2)
button_font = 100 * ((scale_x + scale_y) / 2)
velocities_y = [-480,-360,-240,-120,120,240,360,480]
#functions



#classes
class Ball():
    def __init__(self, x, y,vel_x, vel_y):
        self.x = x
        self.y = y
        self.width = ball_radious
        self.height = ball_radious
        self.vel_x = vel_x
        self.vel_y = vel_y
    def move(self):
        self.x += self.vel_x * dt / 1000
        self.y += self.vel_y * dt / 1000
    def draw(self, screen):
        pg.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), ball_radious)
        pg.draw.circle(screen, (57, 255, 20), (int(self.x), int(self.y)), ball_radious,int(ball_outline))

    def check_collision(self,paddle_left, paddle_right,score_left,score_right):
        if self.x >= screen_width - self.width - paddle_right.width and self.y + self.height >= paddle_right.y and self.y <= paddle_right.y + paddle_right.height and self.vel_x > 0:
            if self.vel_x <= 1800 :
                self.vel_x += 120
                self.vel_x *= -1
            else:
                self.vel_x *= -1
        elif self.x > screen_width + self.width:
            self.vel_x *= 0
            self.vel_y *= 0
            score_left += 1
            self.y = screen_height / 2
            self.x = screen_width / 2
        if self.x <= 0 + self.width + paddle_left.width and self.y + self.height >= paddle_left.y and self.y <= paddle_left.y + paddle_left.height and self.vel_x < 0:
            if self.vel_x <= 1800:
                self.vel_x -= 120
                self.vel_x *= -1
                self.vel_y += random.choice(velocities_y)
            else:

                self.vel_x *= -1
                self.vel_y += random.choice(velocities_y)
        elif self.x < 0 - self.width:
            self.vel_x *= 0
            self.vel_y *= 0
            score_right += 1
            self.y = screen_height / 2
            self.x = screen_width / 2

        if self.y >= screen_height - self.height and self.vel_y > 0:
            self.vel_y *= -1
        elif self.y <= 0 + self.height and self.vel_y < 0:
            self.vel_y *= -1
        return score_left, score_right
    def reset(self):
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.vel_x = 0
        self.vel_y = 0


class Paddle:
    def __init__(self, x, y,up_key,down_key,colour):
        self.x = x
        self.y = y
        self.width = paddle_width
        self.height = paddle_height
        self.speed = 1320
        self.up_key = up_key
        self.colour = colour
        self.down_key = down_key
    def move(self,dt):
        keys = pg.key.get_pressed()

        if keys[self.up_key] and self.y > 0:
            self.y -= self.speed * dt/1000

        if keys[self.down_key] and self.y < screen_height - self.height:
            self.y += self.speed * dt/1000
    def draw(self, screen):
        pg.draw.rect(screen, (255,255,255), (self.x, self.y, self.width, self.height))
        pg.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height),3)
    def reset(self):
        self.x = screen_width - paddle_width
        self.y = screen_height /2



class BotPaddle(Paddle):

    def move(self,ball):
        if self.y + self.height / 2 > ball.y + ball.height / 2 and self.y > 0:
            self.y -= 1320 * dt/1000
        if self.y + self.height / 2 < ball.y + ball.height / 2 and self.y < screen_height - paddle_height:
            self.y += 1320 * dt/1000



paddle_left = Paddle(paddle_left_x, screen_height/2 ,pg.K_w,pg.K_s,(255, 16, 240))
paddle_right = Paddle(screen_width - paddle_width ,screen_height/2,pg.K_UP,pg.K_DOWN,(31, 81, 255))
ball = Ball(screen_width/2,screen_height/2,0,0)
font = pg.font.SysFont("comicsans", int(small_font))
big_font = pg.font.SysFont("comicsans", int(big_font))
button_font = pg.font.SysFont("comicsans", int(button_font))
score_left_text = font.render(str(score_left), True, (255,255,255))
score_right_text = font.render(str(score_right), True, (255,255,255))
#Buttons
solo_button = pg.Rect((screen_width * 0.15),(screen_height / 2 - (50 * scale_y)),350 * scale_x ,150 * scale_y )
duo_button = pg.Rect((screen_width * 0.6),(screen_height / 2 - (50 * scale_y)) ,350 * scale_x,150 * scale_y)


running = True
paused = False
while running:
    dt = clock.tick(240)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if solo_button.collidepoint(event.pos):
                game_state = "solo"
                paddle_left = BotPaddle(paddle_left_x, (screen_height / 2 - (50 *scale_y)), pg.K_w, pg.K_s,(255, 16, 240))
            if duo_button.collidepoint(event.pos):
                game_state = "duo"
                paddle_left = Paddle(paddle_left_x, (screen_height / 2 - (50 * scale_y)), pg.K_w, pg.K_s,(255, 16, 240))
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                paused = not paused
            if event.key == pg.K_BACKSPACE:
                running = False
            if game_state != "menu" and event.key == pg.K_m:
                print("Reset")
                game_state = "menu"
                ball.reset()
                paddle_left.reset()
                paddle_right.reset()
            if event.key == pg.K_r:
                ball.reset()
                score_left = 0
                score_right = 0
            if event.key == pg.K_SPACE:
                velocities = [ -840, -720, -600, 600, 720, 840]
                ball = Ball(screen_width / 2, screen_height / 2, random.choice(velocities), random.choice(velocities))
    if game_state == "menu":
        screen.fill((100,100,100))
        pg.draw.rect(screen,(0,0,255),solo_button)
        pg.draw.rect(screen,(0,0,255),duo_button)
        screen.blit(button_font.render(str("SOLO"), True, (255,255,255)),(screen_width * 0.17 ,screen_height * 0.45 ))
        screen.blit(button_font.render(str("DUO"), True, (255,255,255)),(screen_width * 0.64 ,screen_height * 0.45 ))





    if game_state == "solo":
        if not paused:
            screen.fill((0, 0, 0))
            paddle_left.move(ball)
            paddle_right.move(dt)
            paddle_left.draw(screen)
            paddle_right.draw(screen)
            ball.draw(screen)
            score_left, score_right = ball.check_collision(paddle_left, paddle_right, score_left, score_right)
            ball.move()
            score_left_text = font.render(str(score_left), True, (255, 255, 255))
            score_right_text = font.render(str(score_right), True, (255, 255, 255))
            screen.blit(score_left_text, (50 * scale_x, 10 * scale_y))
            screen.blit(score_right_text, ((screen_width - 70), 10 * scale_y))

        else:
            paused_text = big_font.render(str("Paused"), True, (255, 255, 255))
            screen.blit(paused_text, (150 * scale_x, 40 * scale_y))

    if game_state == "duo":

        if not paused:
            screen.fill((0, 0, 0))
            paddle_left.move(dt)
            paddle_right.move(dt)
            paddle_left.draw(screen)
            paddle_right.draw(screen)
            ball.draw(screen)
            score_left, score_right = ball.check_collision(paddle_left, paddle_right, score_left, score_right)
            ball.move()
            score_left_text = font.render(str(score_left), True, (255, 255, 255))
            score_right_text = font.render(str(score_right), True, (255, 255, 255))
            screen.blit(score_left_text, (50 * scale_x, 10 * scale_y))
            screen.blit(score_right_text, ((screen_width - 70 ), 10 * scale_y))

        else:
            paused_text = big_font.render(str("Paused"), True, (255, 255, 255))
            screen.blit(paused_text, (150 * scale_x, 40 * scale_y))

    pg.display.flip()