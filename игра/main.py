from pygame import *
import random

font.init()
mixer.init()

class GameSprite(sprite.Sprite):
    def __init__(self, picture, x, y, w, h, speed):
        super().__init__()
        self.original_image = transform.scale(image.load(picture), (w, h))
        self.image = self.original_image.copy()
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_w = w
        self.original_h = h
        self.picture = picture
        
    def fill(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, x, y, w, h, speed):
        super().__init__(picture, x, y, w, h, speed)
        self.is_big = False
        self.big_timer = 0
        self.is_small = False
        self.small_timer = 0
        
    def update(self):
        keys = key.get_pressed()
        
        # Обычное движение
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 654:
            self.rect.x += self.speed
        
        # Увеличение по пробелу
        if keys[K_SPACE] and not self.is_big and not self.is_small:
            self.image = transform.scale(image.load(self.picture), 
            (self.original_w + 30, self.original_h + 30))
            self.is_big = True
            self.big_timer = time.get_ticks()
            self.rect.x = self.rect.x - 15
        
        # Возврат в исходную форму через 0.5 секунды
        if self.is_big and time.get_ticks() - self.big_timer > 500:
            self.image = self.original_image.copy()
            self.is_big = False
            self.rect.x = self.rect.x + 15

        if keys[K_s] and not self.is_small and not self.is_big:
            self.image = transform.scale(image.load(self.picture), 
            (self.original_w - 30, self.original_h - 30))
            self.is_small = True
            self.small_timer = time.get_ticks()
            self.rect.x = self.rect.x + 15
        
        if self.is_small and time.get_ticks() - self.small_timer > 500:
            self.image = self.original_image.copy()
            self.is_small = False
            self.rect.x = self.rect.x - 15

class Obstacle(GameSprite):
    def __init__(self, picture, x, y, w, h, speed):
        super().__init__(picture, x, y, w, h, speed)
        
    def update(self):
        # Движение вниз
        self.rect.y += self.speed
        
        # Если препятствие ушло за нижнюю границу экрана, удаляем его
        if self.rect.y > 788:
            self.kill()
    
    def fill(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

window = display.set_mode((788, 788))
display.set_caption('Лабиринт')
background = transform.scale(image.load('fon.png'), (788, 788))

player = Player('1.png', 329, 600, 130, 100, 7)

# Группа для всех препятствий
obstacles = sprite.Group()

# Таймер для появления препятствий
obstacle_timer = 0
obstacle_delay = 60  # Задержка между появлениями (чем меньше, тем чаще)

# Счетчик очков (за уклонение от препятствий)
score = 0
font_score = font.Font(None, 36)

FPS = 60
finish = False
clock = time.Clock()
game = True
treasure = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:
        window.blit(background, (0, 0))
        
        # Появление препятствий
        obstacle_timer += 1
        if obstacle_timer >= obstacle_delay:
            obstacle_timer = 0

            obstacle_x_rand = random.randint(1,3)
            if obstacle_x_rand == 1:
                obstacle_x = 37
            elif obstacle_x_rand == 2:
                obstacle_x = 294
            else:
                obstacle_x = 551  

            obstacle_wh_rand = random.randint(1,6)
            if obstacle_wh_rand == 1 or obstacle_wh_rand == 2:
                obstacle_width = 200
                obstacle_height = 200
                if obstacle_wh_rand == 1:
                    obstacle_image = 'free.png'
                elif obstacle_wh_rand == 2:
                    obstacle_image = 'lump.png'
            elif obstacle_wh_rand == 3 or obstacle_wh_rand == 4 or obstacle_wh_rand == 5 or obstacle_wh_rand == 6:
                obstacle_height = 100
                if obstacle_wh_rand == 3 or obstacle_wh_rand == 4:
                    obstacle_image = 'kust.png'
                    obstacle_width = 100
                    obstacle_x = obstacle_x + 50
                elif obstacle_wh_rand == 5 or obstacle_wh_rand == 6:
                    obstacle_image = 'zabor.png'
                    obstacle_width = 150
                    obstacle_x = obstacle_x + 25
  
            obstacle_speed = 4
            
            obstacle = Obstacle(obstacle_image, obstacle_x, -obstacle_height, obstacle_width, obstacle_height, obstacle_speed)

            obstacles.add(obstacle)
        
        obstacles.update()
        obstacles.draw(window)
        player.fill()
        player.update()

        if sprite.spritecollide(player, obstacles, False):
            finish = True
            print("Game Over!")
        
        # Увеличение счета за время жизни
        '''score += 1
        score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))'''
        
        # Отображение количества препятствий на экране
        '''obstacles_count = font_score.render(f"Obstacles: {len(obstacles)}", True, (255, 255, 255))
        window.blit(obstacles_count, (10, 50))'''
    
    else:
        game_over_font = font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        window.blit(game_over_text, (788//2 - game_over_text.get_width()//2, 788//2 - 50))

        # Отображение финального счета на экране
        '''score_final = font_score.render(f"Final Score: {score}", True, (255, 255, 255))
        window.blit(score_final, (788//2 - score_final.get_width()//2, 788//2 + 20))'''
        
        restart_text = font_score.render("Press R to restart or ESC to quit", True, (255, 255, 255))
        window.blit(restart_text, (788//2 - restart_text.get_width()//2, 788//2 + 80))
        
        keys = key.get_pressed()
        if keys[K_r]:
            finish = False
            score = 0
            obstacles.empty()  
            player.rect.x = 329
            player.rect.y = 600
            obstacle_timer = 0
        if keys[K_ESCAPE]:
            game = False
    
    display.update()
    clock.tick(FPS)