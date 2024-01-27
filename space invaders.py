import pygame
import sys
import random
import os

pygame.init()

WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BULLET_SIZE = 5
FPS = 60

base_path = r'C:\Users\mattp\Desktop\Programs\Space invaders'

player_image_path = os.path.join(base_path, 'kisspng-spacecraft-sprite-spaceshipone-computer-software-space-invaders-5acab8aa1798c3.4611556415232349860967.png')
player_image = pygame.image.load(player_image_path)
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

enemy_image_path = os.path.join(base_path, 'kisspng-super-space-invaders-91-pac-man-space-invaders-png-hd-5a7563fde09737.6949185715176427499199 (1).png')
enemy_image = pygame.image.load(enemy_image_path)
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
player_speed = 7

enemies = []
enemy_speed = 3
enemy_spawn_timer = 0
enemy_spawn_interval = 60

bullets = []
bullet_speed = 30
bullet_spawn_timer = 0
bullet_spawn_interval = 30 

lives = 3

font = pygame.font.Font(None, 36)

def draw_lives():
    lives_text = font.render(f'Lives: {lives}', True, (0, 0, 0))
    screen.blit(lives_text, (WIDTH - 120, 20))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    bullet_spawn_timer += 1
    if keys[pygame.K_SPACE] and bullet_spawn_timer >= bullet_spawn_interval:
        bullet_spawn_timer = 0
        bullet = pygame.Rect(player.centerx - BULLET_SIZE // 2, player.y, BULLET_SIZE, BULLET_SIZE)
        bullets.append(bullet)

    enemy_spawn_timer += 1
    if enemy_spawn_timer == enemy_spawn_interval:
        enemy_spawn_timer = 0
        enemy = pygame.Rect(random.randint(0, WIDTH - ENEMY_SIZE), 0, ENEMY_SIZE, ENEMY_SIZE)
        enemies.append(enemy)

    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            lives -= 1
            if lives == 0:
                pygame.quit()
                sys.exit()

    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    for enemy in enemies:
        if player.colliderect(enemy):
            lives -= 1
            enemies.remove(enemy)
            if lives == 0:
                pygame.quit()
                sys.exit()

        for bullet in bullets:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)

    screen.fill((0, 50, 255))

    screen.blit(player_image, player.topleft)

    for enemy in enemies:
        screen.blit(enemy_image, enemy.topleft)

    for bullet in bullets:
        pygame.draw.circle(screen, (255, 0, 200), bullet.center, BULLET_SIZE)

    draw_lives()

    pygame.display.flip()
    clock.tick(FPS)
