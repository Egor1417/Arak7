#Создай собственный Шутер!
from pygame import *
from random import randint

font.init()
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

lost = 0
lost_max = 10

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()

        if key_pressed[K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x <= 620:
            self.rect.x += self.speed
        if key_pressed[K_w] and self.rect.y >= 25:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y <= 475:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top, 15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
           self.rect.x = randint(5, 630)
           self.rect.y = -50
           lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()    

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Space shooter")
clock = time.Clock()
background = image.load("galaxy.jpg")
background = transform.scale(background,(win_width,win_height))

rocket = Player("rocket.png", 330, 430, 80, 100, 10)
aliens = sprite.Group()
for i in range(6):
    alien = Enemy("ufo.png", randint(5, 630), -50, 100, 80, randint(1,4))
    aliens.add(alien)
    bullets = sprite.Group()

score = 0
game = True
while game:
    window.blit(background,(0, 0))
    rocket.reset()
    aliens.draw(window)
    bullets.draw(window)

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
               rocket.fire()
               fire_sound.play()

    collides = sprite.groupcollide(aliens, bullets, True, True)
    for c in collides:
        score += 1
        alien = Enemy("ufo.png", randint(5, 630), -50, 100, 80, randint(1,4))  
        aliens.add(alien)

    if sprite.spritecollide(rocket,aliens,False): 
       game = False

    if lost > lost_max:
        game = False 

    if score > 10:
       game = False                  
     
    rocket.update()
    aliens.update()
    bullets.update()
    display.update()
    clock.tick(60)