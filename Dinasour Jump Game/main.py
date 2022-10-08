import pygame
from pygame.locals import (
    QUIT,
)

pygame.init()

width = 800
height = 600
hit = 0
dmg = 20

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("GAME TEST 1")

background = pygame.transform.scale(pygame.image.load("background.png"), (800, 600))
start_bg = pygame.transform.scale(pygame.image.load("background.png"), (800, 600))

# Death Counter
death = 0

# Velocity
vel = 10
vel_y = 10

# Assets
character = pygame.transform.scale(pygame.image.load("character.png"), (64, 80))
character_rect = character.get_rect()

obstacle = pygame.transform.scale(pygame.image.load("obstacle.png"), (44, 60))
obstacle_rect = obstacle.get_rect()

# HP Bar
RED = (255, 0, 0)
GREEN = (0, 255, 0)
player_health = 300
hp_x = 10
hp_y = 10
hp_width = 10


def pos():
    # Pos (x, y) for objects
    character_rect.x = 100
    character_rect.y = 380
    obstacle_rect.x = 700
    obstacle_rect.y = 400


# Text
def start_game_text():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_colour = (235, 144, 26)
    text = font.render("PRESS '1' TO START GAME.", True, text_colour)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, height / 2)
    screen.blit(text, text_rect)


def game_over_text():
    global death
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_colour_red = (255, 0, 0)
    text_game_over = font.render(f"GAME OVER! YOU DIED {death} TIMES!", True, text_colour_red)
    text_game_over_singular = font.render(f"GAME OVER! YOU DIED {death} TIME!", True, text_colour_red)
    text_game_over_rect = text_game_over.get_rect()
    text_game_over_rect.center = (width / 2, 265)
    if death == 1:
        screen.blit(text_game_over_singular, text_game_over_rect)
    else:
        screen.blit(text_game_over, text_game_over_rect)


def death_counter():
    global death
    death = death + 1
    if death == 1:
        print(f"You died {death} time!")
    else:
        print(f"You died {death} times!")


FPS = 75
clock = pygame.time.Clock()

isJump = False


def update():
    pygame.display.update()


x = False
y = False

# Main Game Loop
running = True
start = False
while running:
    clock.tick(FPS)
    keys_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if keys_pressed[pygame.K_ESCAPE]:
            running = False
            start = False
        elif event.type == QUIT:
            running = False
            start = False
        elif keys_pressed[pygame.K_1]:
            start = True

    # Start BG
    screen.blit(start_bg, (0, 0))

    # "Start Game" Text
    # screen.blit(text, textRect)

    if start is False:
        # Pos (x, y) for objects
        pos()
        # Player HP Reset
        player_health = 300
        start_game_text()
        if death > 0:
            game_over_text()

    if start is True:
        # Movement
        if keys_pressed[pygame.K_a] and character_rect.x > 0:
            character_rect.x -= vel
        elif keys_pressed[pygame.K_d] and character_rect.x < 735:
            character_rect.x += vel

        # Jump Mechanics
        if keys_pressed[pygame.K_SPACE] and isJump is False:
            isJump = True
        if isJump is True:
            character_rect.y -= vel_y * 2
            vel_y += -1
            if vel_y < -10:
                isJump = False
                vel_y = 10

        # Obstacle Movement
        if 0 < obstacle_rect.x < 800 and x is False:
            obstacle_rect.x -= vel
            if obstacle_rect.x == 0:
                x = True
            elif obstacle_rect.x == 750:
                obstacle_rect.x -= vel
        if x is True:
            obstacle_rect.x += vel
            if obstacle_rect.x == 750:
                x = False

        # Update Display
        screen.blit(background, (0, 0))
        screen.blit(character, character_rect)
        screen.blit(obstacle, obstacle_rect)

        # Hit Detection + HP Bar Interaction
        pygame.draw.rect(screen, RED, (hp_x, hp_y, 300, hp_width))
        pygame.draw.rect(screen, GREEN, (hp_x, hp_y, player_health, hp_width))
        if character_rect.colliderect(obstacle_rect):
            hit += 1
            player_health -= dmg
            print(f"""You were hit {hit} times! 
HP left: {player_health}""")
            if player_health == 0:
                print("""Game over!
You DIED!""")
                start = False
                screen.blit(start_bg, (0, 0))
                death_counter()

    update()
