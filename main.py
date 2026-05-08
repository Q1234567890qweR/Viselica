import pygame
import sys
import random

with open("russian_noun.txt", "r", encoding="utf-8") as file:
 words = file.read().splitlines()


pygame.init()

# ---------------- НАСТРОЙКИ ----------------

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Виселица")

clock = pygame.time.Clock()

FONT_BIG = pygame.font.SysFont("arial", 54)
FONT_MID = pygame.font.SysFont("arial", 42)
FONT_KEY = pygame.font.SysFont("arial", 28)

# Слово
word = random.choice(words).strip().upper()

# Количество ошибок
mistakes = 0
MAX_MISTAKES = 7

# Угаданные буквы
guessed_letters = set()

hangman_images = [
    pygame.image.load("0.png"),
    pygame.image.load("1.png"),
    pygame.image.load("2.png"),
    pygame.image.load("3.png"),
    pygame.image.load("4.png"),
    pygame.image.load("5.png"),
    pygame.image.load("6.png"),
    pygame.image.load("7.png"),
]

for i in range(MAX_MISTAKES + 1):
    surface = pygame.Surface((320, 220))
    color = (40 + i * 25, 40, 40)
    surface.fill(color)

    text = FONT_BIG.render(f"{i}/7", True, (255, 255, 255))
    rect = text.get_rect(center=(160, 110))

    surface.blit(text, rect)

    hangman_images.append(surface)

# ---------------- РУССКАЯ КЛАВИАТУРА ----------------

keyboard_rows = [
    list("ЙЦУКЕНГШЩЗХЪ"),
    list("ФЫВАПРОЛДЖЭ"),
    list("ЯЧСМИТЬБЮ")
]

buttons = []

KEY_W = 55
KEY_H = 55
GAP = 8

keyboard_start_y = 470

for row_index, row in enumerate(keyboard_rows):

    row_width = len(row) * (KEY_W + GAP)
    start_x = (WIDTH - row_width) // 2

    for col_index, letter in enumerate(row):

        x = start_x + col_index * (KEY_W + GAP)
        y = keyboard_start_y + row_index * (KEY_H + GAP)

        rect = pygame.Rect(x, y, KEY_W, KEY_H)

        buttons.append((rect, letter))

# ---------------- ФУНКЦИИ ----------------

def draw_hangman():
    image = hangman_images[mistakes]
    rect = image.get_rect(center=(WIDTH // 2, 130))
    screen.blit(image, rect)


def draw_word():
    display = ""

    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    text = FONT_BIG.render(display, True, (255, 255, 255))

    rect = text.get_rect(center=(WIDTH // 2, 320))

    screen.blit(text, rect)


def draw_keyboard():

    mouse_pos = pygame.mouse.get_pos()

    for rect, letter in buttons:

        if letter in guessed_letters:
            color = (60, 120, 60)
        else:
            color = (70, 70, 90)

        if rect.collidepoint(mouse_pos):
            color = (120, 120, 150)

        pygame.draw.rect(screen, color, rect, border_radius=10)

        txt = FONT_KEY.render(letter, True, (255, 255, 255))

        txt_rect = txt.get_rect(center=rect.center)

        screen.blit(txt, txt_rect)


def check_letter(letter):

    global mistakes

    if letter in guessed_letters:
        return

    guessed_letters.add(letter)

    if letter not in word:
        mistakes += 1


# ---------------- GAME LOOP ----------------

running = True

while running:

    screen.fill((25, 25, 35))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Мышка
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, letter in buttons:
                if rect.collidepoint(event.pos):
                    check_letter(letter)


    draw_hangman()
    draw_word()
    draw_keyboard()
    won = True
    for letter in word:
        if letter not in guessed_letters:
            won = False

    if won:
        text = FONT_MID.render("ПОБЕДА!", True, (0, 255, 100))
        screen.blit(text, (40, 40))

    if mistakes >= MAX_MISTAKES:
        text = FONT_MID.render("ПОРАЖЕНИЕ!", True, (255, 80, 80))
        screen.blit(text, (40, 40))

    pygame.display.flip()
    clock.tick(60)