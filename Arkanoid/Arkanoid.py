import sys

import pygame
import random

#Main
game_over = False
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Arkanoid')
lives = 5
score = 0
blocks = []
block_images = []
WIDTH, HEIGHT = 800, 600




#Sounds
glass_sound = pygame.mixer.Sound("sound/glass.mp3")
glass_sound.set_volume(0.1)

#Music
pygame.mixer.music.load("sound/music.mp3")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)



def level():
    glass_img = pygame.image.load("img/glass.png").convert_alpha()

    for row in range(3):
        for col in range(5):
            platform = pygame.Rect(col * 98 + 155, row * 70 + 90, 93, 40)
            blocks.append(platform)

            # Создаем изображение под размер платформы и сохраняем в отдельный список
            scaled_img = pygame.transform.scale(glass_img, (platform.width, platform.height))
            block_images.append(scaled_img)  # нужен отдельный список

level()

#Img
background = pygame.image.load("img/bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

live1 = pygame.image.load("img/heart.png")
live1 = pygame.transform.scale(live1, (50, 50 ))

live2 = pygame.image.load("img/heart.png")
live2 = pygame.transform.scale(live2, (50, 50 ))

live3 = pygame.image.load("img/heart.png")
live3 = pygame.transform.scale(live3, (50, 50 ))

live4 = pygame.image.load("img/heart.png")
live4 = pygame.transform.scale(live4, (50, 50 ))

live5 = pygame.image.load("img/heart.png")
live5 = pygame.transform.scale(live5, (50, 50 ))

#lives disaparing
def show_lives():
    global lives
    if lives == 5:
        screen.blit(live1, (40, 50))
        screen.blit(live2, (40, 150))
        screen.blit(live3, (40, 250))
        screen.blit(live4, (40, 350))
        screen.blit(live5, (40, 450))

    if lives == 4:
        screen.blit(live1, (40, 50))
        screen.blit(live2, (40, 150))
        screen.blit(live3, (40, 250))
        screen.blit(live4, (40, 350))

    if lives == 3:
        screen.blit(live1, (40, 50))
        screen.blit(live2, (40, 150))
        screen.blit(live3, (40, 250))

    if lives == 2:
        screen.blit(live1, (40, 50))
        screen.blit(live2, (40, 150))

    if lives == 1:
        screen.blit(live1, (40, 50))

    if lives == 0:
        game_over = True



#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)


# x, y

#player
player_x = 40
player_y = 550
player_speed = 10

#ball
ball_x = 40
ball_y = 500
ball_speed_x = 7
ball_speed_y = 10
ball_radius = 15



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Img
    screen.blit(background, (0, 0))

    #Show lives
    show_lives()


    # Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed




    #Hit box
    ball_rect = pygame.Rect(ball_x, ball_y, 15, 15)
    player_rect = pygame.Rect(player_x, 550, 150, 50)


    # Collision player
    if ball_rect.colliderect(player_rect):
        ball_speed_y = -ball_speed_y
        ball_speed_x = -ball_speed_x


    #Remove blocks
    for block in blocks[:]:
        if ball_rect.colliderect(block):
            idx = blocks.index(block)
            block_images.pop(idx)
            blocks.remove(block)
            ball_speed_y =- ball_speed_y
            score += 1
            glass_sound.play()
            break

        # Font GameOver
        #game over text
        if lives < 0:
            game_over = True


    #Game over text
    if game_over == True:
        font2 = pygame.font.Font(None, 60)
        text_over = font2.render(f"Game Over \n press r to restart", True, RED)
        screen.blit(text_over, (70, 300))

        #Restart
        if keys[pygame.K_r]:
            game_over = False
            score = 0
            lives = 5
            level()

    #Score font
    font = pygame.font.Font(None, 36)
    text = font.render(f"Your score: {score}", True, RED)


    #Ball move
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    #Lives - 1
    if ball_y >= 600:
        lives -= 1

    #Bounce of up/down
    if ball_y <= 0 or ball_y >= 600:
        ball_speed_y =- ball_speed_y

    #Bounce of left/right
    if ball_x <= 0 or ball_x >= 800:
        ball_speed_x =- ball_speed_x


    #Borders
    if player_y < 0: player_y = 0
    if player_y > 450: player_y = 450
    if player_x < 0: player_x = 0
    if player_x > 650: player_x = 650


    #Draw
    pygame.draw.rect(screen, WHITE, (player_x, 550, 150, 50))
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)


    for i, block in enumerate(blocks):
        screen.blit(block_images[i], block)


    #Blocks show
    #for block in blocks:
    #    screen.blit(glass, block)


    #Font draw
    screen.blit(text, (500, 25))

    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(60)