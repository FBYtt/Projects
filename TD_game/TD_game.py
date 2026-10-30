import pygame as pg
import math
pg.init()
screen_width = pg.display.get_desktop_sizes()[0][0]
screen_height = pg.display.get_desktop_sizes()[0][1]
print(screen_width, screen_height)
screen_scale_y = 1536 / screen_width
screen_scale_x = 960 / screen_height
# print(screen_scale_x, screen_scale_y)
screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
clock = pg.time.Clock()

minions = []
bullets = []
seconds = 0
lives = 3
shoot_timer = 0
small_font = 20
#Fonts
font = pg.font.SysFont("comicsans", int(small_font))



class Monster:
    def __init__(self,health,width,height,speed,y):
        self.health = health
        self.width = width
        self.height = height
        self.colour = (35,35,35)
        self.speed = speed
        self.x = 200
        self.y = y
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
        self.state = 0
    def move(self):
        if self.y >= screen_height / 3 and self.x == 200:
            self.y -= self.speed
            self.state = 1
        if self.y <= screen_height / 3 and self.x <= screen_width - 200:
            self.x += self.speed
            self.state = 2
        if self.x >= screen_width - 200 - self.width and self.y < screen_height:
            self.y += self.speed
            self.state = 3
    def draw(self,screen):
        pg.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        health = font.render(str(self.health), True, (255,255,255))
        screen.blit(health,(self.x + self.width /3,self.y + self.height - 10))


class Tower():
    def __init__(self,x,y,colour,shoot_speed):
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
        self.colour = colour
        self.shoot_speed = shoot_speed
        self.time_passed = 0
    def calculate(self,minion):

        if minion[0].state == 1:
            dx = ((minion[0].x + minion[0].width / 2) - (self.x + self.width / 2)) / 60
            dy = ((minion[0].y + minion[0].height / 3) - (self.y + self.height / 2)) / 60
            vel_x = (dx * -1) / 0.2
            vel_y = (dy * -1) / 0.2
        if minion[0].state == 2:
            dx = ((minion[0].x + minion[0].width/1.5) - (self.x + self.width / 2)) / 60
            dy = ((minion[0].y + minion[0].height / 2) - (self.y + self.height / 2)) / 60
            vel_x = ((dx * -1) / 0.2)
            vel_y = ((dy * -1) / 0.2)
        if minion[0].state == 3:
            dx = ((minion[0].x + minion[0].width / 2) - (self.x + self.width / 2)) / 60
            dy = ((minion[0].y + minion[0].height) - (self.y + self.height / 2)) / 60
            vel_x = ((dx * -1) / 0.2)
            vel_y = ((dy * -1) / 0.2)
        return vel_x, vel_y
    def draw(self,screen):
        pg.draw.rect(screen,self.colour, (self.x, self.y, self.width, self.height))
    def shoot(self,dt):
        if self.time_passed < self.shoot_speed:
            self.time_passed += dt
        if self.time_passed >= self.shoot_speed and len(minions) > 0:
            bullets.append(Bullet(self.x + self.width/2,self.y + self.height/2,self.calculate(minions)[0],self.calculate(minions)[1],20,(140,0,0)))
            self.time_passed = 0




class Bullet:
    def __init__(self,x,y,vel_x,vel_y,damage,colour):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = damage
        self.colour = colour
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

    def move(self):
            self.y -= self.vel_y
            self.x -= self.vel_x

    def draw(self,screen):
        pg.draw.circle(screen,self.colour, (self.x, self.y), self.width, self.height)
    def check_collision(self,minion):
        minion.rect = pg.Rect(minion.x,minion.y,minion.width,minion.height)
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
        if self.rect.colliderect(minion.rect):

            minion.health -= self.damage
            return True
        else:
            return False


tower = Tower(screen_width/2,screen_height/1.1,(255,255,255),0.5)
tower2 = Tower(screen_width/2 + 100,screen_height/1.1,(255,255,255),0.5)
running = True
paused = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                running = False
            if event.key == pg.K_ESCAPE:
                paused = not paused
            if event.key == pg.K_SPACE:
                list.clear(minions)
                list.clear(bullets)
            if event.key == pg.K_DELETE:
                pass

    if not paused:
        dt = clock.tick(60) / 1000
        seconds += dt
        screen.fill((120, 120, 200))
        tower.draw(screen)
        tower2.draw(screen)
        tower2.shoot(dt)
        if seconds >= 1:
            minions.append(Monster(100, 100, 100, 2, screen_height))
            seconds = 0
            print(f"Nr of minions: {len(minions)}")

        for minion in minions[:]:
            minion.move()
            minion.draw(screen)
            if minion.x >= screen_width - 200 - minion.width and minion.y >= screen_height:
                minions.remove(minion)
            if minion.health <= 0:
                minions.remove(minion)
        tower.shoot(dt)

        for bullet in bullets[:]:
            if len(minions) != 0:
                bullet.move()
                bullet.draw(screen)
                if bullet.check_collision(minions[0]):
                    bullets.remove(bullet)
                elif bullet.y < screen_height / 3 or bullet.x < 200 or bullet.x > screen_width - 200:
                    bullets.remove(bullet)
            if len(minions) == 0:
                list.clear(bullets)






    pg.display.flip()