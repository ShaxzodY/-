from pygame import *
from random import randint
from time import time as timer
win_width = 900
win_height = 700
win = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (900, 700))
width = 900
height = 700

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 40
lost = 0
kills = 0
font.init()
font1 = font.Font(None, 40)
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 1100:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 900:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 50, 50, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            lost += 1
            self.rect.x = randint(20, 620)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            
winner = transform.scale(image.load('WIN.jpg'), (900, 700))
looser = transform.scale(image.load('loss.jpg'), (900, 700))
ship = Player('rocket.png', 350, 400, 80, 120, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(20, 620), 0, 80, 120, randint(1, 1))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    asteroid = Enemy('asteroid.png', randint(20, 620), 0, 80, 120, randint(1, 1))
    asteroids.add(asteroid)
   
finish = False
run = True
rel_time = False
num_fire = 0
life = 3
while run:
    win.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time  == False:
                    end_time = timer()
                    rel_timer = True
                
    if not finish:
        ship.reset()
        ship.update()
        monsters.draw(win)
        monsters.update()
        bullets.draw(win)
        bullets.update()
        asteroids.draw(win)
        asteroids.update()
        if rel_time == True:
            new_time = timer()
            if new_time - end_time < 3:
                win.blit(font1.render("Wait, reloading...", True, (255, 255, 0), (win_width-200, win_height-200)))
            else:
                rel_time = False
                num_fire = 5

        text1 = font1.render('Пропущено:'+ str(lost), True, (255 ,255, 255))
        text2 = font1.render('Убито:'+ str(kills), True, (250, 250, 0))
        lose_text = font1.render('Ты проиграл', True, (250, 250, 0))
        win.blit(text1, (10, 10))
        win.blit(text2, (10, 50))
        text_life = font1.render('Life:'+ str(life), True, (255, 255, 0))
        win.blit(text_life, (100, 200))
        win.blit(text_life, (10, 80))
    collides = sprite.groupcollide(monsters, bullets, True, True)
        
       

    for collide in collides:
        kills += 1
        monster = Enemy('ufo.png', randint(20, 620), 0, 80, 120, randint(1, 5))
        monsters.add(monster)

    if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
        sprite.spritecollide(ship, monsters, True)
        sprite.spritecollide(ship, monsters, True)

        life -= 1
        
    if life <= 1:
        finish = True
        win.blit(looser, (0, 0))



    if kills >= 10:
        finish = True
        win.blit(winner, (0, 0))

    display.update()
    clock.tick(FPS)
    
