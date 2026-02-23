import pygame
import random
import sys
from os import path
import time

pygame.init()


img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 640
HEIGHT = 960
FPS = 30


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

level = [
"-------------------------------------",
"-                                   -",
"-   -                               -",
"-               ---                 -",
"-                                   -",
"-                                   -",
"-      ---                          -",
"-                   --              -",
"-   -------                         -",
"-                                   -",
"-             -                     -",
"-              --                   -",
"-                                   -",
"-                                   -",
"------------------------------------"]

PLATFORM_COLOR = "#FF6262"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 64


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class PACMAN(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pacman_img

        self.image_up = pacman_img_up
        self.image_down = pacman_img_down
        self.image_right = pacman_img_right
        self.image_left =pacman_img_left

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 150
        self.speedx = 0
        self.speedy = 0
        self.speed = 10
        self.hp =100

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.image = self.image_left
            self.speedx = -self.speed
        if keystate[pygame.K_RIGHT]:
            self.image = self.image_right
            self.speedx = self.speed
        if keystate[pygame.K_UP]:
            self.image = self.image_up
            self.speedy = -self.speed
        if keystate[pygame.K_DOWN]:
            self.image = self.image_down
            self.speedy = self.speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 950:
            self.rect.bottom = 950
    

class Ghost1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ghost_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 5
        self.rect.bottom = HEIGHT - 150
        self.speedx = 0
        self.speedy = 0
        self.speed = 10
        self.hp = 100

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed() 
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_w]:
            self.speedy = -8
        if keystate[pygame.K_s]:
            self.speedy = 8
        self.rect.x += self.speedx 
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 950:
            self.rect.bottom = 950

class GHOST(pygame.sprite.Sprite):
    def __init__(self,ghost_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = ghost_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.damage = 10
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -700
        self.speedx = random.randrange(1,10)
        self.speedy = random.randrange(-75,5)

    def update(self):
        self.rect.x +=  ((pacmanX - self.rect.x) / 30) #+ self.speedx #self.speedx
        self.rect.y +=  ((pacmanY - self.rect.y) / 30) #+ self.speedy #self.speedy
        if self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-80,-60)            
            self.speedy = random.randrange(0,25)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pacman_img = pygame.image.load(path.join(img_dir,"pacman.png")).convert()

pacman_img_down = pygame.image.load(path.join(img_dir,"pacman_down.png")).convert()
pacman_img_up = pygame.image.load(path.join(img_dir,"pacman_up.png")).convert()
pacman_img_right = pygame.image.load(path.join(img_dir,"pacman_right.png")).convert()
pacman_img_left = pygame.image.load(path.join(img_dir,"pacman_left.png")).convert()

ghost_img = pygame.image.load(path.join(img_dir,"Blinky.png")).convert()
ghost_imgs = []
for i in range(2):
    ghost_imgs.append(pygame.image.load(path.join(img_dir,"ghostyellow_small.png")).convert())
background = pygame.image.load(path.join(img_dir,"black.png")).convert()
background_rect = background.get_rect()


clock = pygame.time.Clock()
pygame.display.set_caption("PAC-MAN")

all_sprites = pygame.sprite.Group()
ghosts = pygame.sprite.Group()
pacman = PACMAN()
ghost = Ghost1()
all_sprites.add(pacman)
all_sprites.add(ghost)
ghosts.add(ghost)

platforms = []


for i in range(2):
    g = GHOST(random.choice(ghost_imgs))
    all_sprites.add(g)
    ghosts.add(g)


pacmanX = WIDTH / 2
pacmanY = HEIGHT - 150

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    all_sprites.update()
    pacmanX = pacman.rect.x
    pacmanY = pacman.rect.y
    hits = pygame.sprite.spritecollide(pacman,ghosts,True)
    if hits :
        running = False               

    hits = pygame.sprite.spritecollide(pacman,platforms,False)
    if hits:
        for p in platforms:
            if pygame.sprite.collide_rect(pacman, p): # если есть пересечение платформы с игроком
                if pacman.rect.right >= p.rect.left: # если движется вправо
                    pacman.rect.right = p.rect.left  # то не движется вправо
                    continue
                if pacman.rect.left <= p.rect.right:  # если движется влево
                    pacman.rect.left = p.rect.right  # то не движется влево
                    continue
                if pacman.rect.bottom >= p.rect.top: # если падает вниз
                    pacman.rect.bottom = p.rect.top  # то не падает вниз
                    continue
                if pacman.rect.top <= p.rect.bottom: # если движется вверх
                    pacman.rect.top = p.rect.bottom  # то не движется вверх
                    continue
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)   


    platforms_group = pygame.sprite.Group()
    x1=y1=0 
    for row in level: 
      for col in row:
          if col == "-":
             
               pf = Platform(x1,y1)
               all_sprites.add(pf)
               platforms.append(pf)
                    
          x1 += PLATFORM_WIDTH 
      y1 += PLATFORM_HEIGHT    
      x1 = 0   
    pygame.display.flip()




pygame.quit()