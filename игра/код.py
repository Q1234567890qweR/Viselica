from pygame import *
font.init()
mixer.init()

class GameSprite(sprite.Sprite):
    def __init__(self, picture, x, y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def fill(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

jump = 1

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 654:
            self.rect.x += self.speed
        if keys[K_e] and jump == 1:
            self.image = transform.scale((w + 20, h + 20))
        
'''class Obstacles(GameSprite):
    def update(self):'''


window = display.set_mode((788, 788))
display.set_caption('Лабиринт')
backgroup = transform.scale(image.load('fon.png'), (788, 788))

player = Player('1.png', 329, 600, 130, 100, 7)

FPS = 60

finish = False
clock = time.Clock()
game = True
treasure = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(backgroup, (0,0))
        player.fill()
        player.update()

    display.update()
    clock.tick(FPS)