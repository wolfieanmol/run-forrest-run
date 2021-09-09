import random

import pygame
from pygame.locals import *
import sys
import os

from PersistanceLayer.db_handler import DbHandler
from PersistanceLayer.redis_leaderboard import Leaderboard
from client.sprites import Apple, Player
from client.websocket_client import WebsocketLeaderboard, WebsocketRank, WebsocketUpdateScore

db = DbHandler()
leaderboard = Leaderboard()

W, H = 1200, 800
HW, HH = W / 2, H / 2
AREA = W * H

rank = ""
score = 0
top_leaderboard = {}

os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"


def move_background(screen, bg, x):
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < W:
        screen.blit(bg, (rel_x, 0))
    x -= 1
    return x


def add_apple(apples, all_sprites):
    for apple in apples:
        if apple.rect.x == 1200:
            return

    new_apple = Apple()
    apples.add(new_apple)
    all_sprites.add(new_apple)


def initialize_screen(username):
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(f"client - {username}")

    bg = pygame.image.load("assets/forest2.jpg").convert()
    x = 0
    screen.blit(bg, (x, 0))
    return screen, bg, x


def initialize_assets():
    player = Player()

    apples = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    return player, apples, all_sprites


def display_score(websocket_rank_client):
    global score
    white = (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', 20)
    rank = websocket_rank_client.rank
    if websocket_rank_client.score and score == 0:
        score = websocket_rank_client.score
    text = font.render(f'Rank: {rank} Score: {score}', True, white)
    textRect = text.get_rect()
    textRect.center = (100, 50)

    return text, textRect


def display_top_leaderboards(websocket_leaderboard_client):
    font = pygame.font.Font('freesansbold.ttf', 20)

    top_leaderboard_texts = []
    y = 50
    top_leaderboard = websocket_leaderboard_client.top_leaderboard
    for user_id, user_score in top_leaderboard.items():
        text = font.render(f"{user_id}: {user_score[1]}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (1000, y)
        top_leaderboard_texts.append((text, text_rect))
        y += 20

    return top_leaderboard_texts


def increase_score(websocket_update_score_client, user_id):
    global score
    score += 10
    websocket_update_score_client.send_message(user_id)
    db.insert_user_point(user_id, 10)


def is_collided(player, apple):
    if apple.rect.x == 100:
        return True
    return False


def handle_collision(player, apples, websocket_update_score_client, user_id):
    col = pygame.sprite.spritecollideany(player, apples, collided=is_collided)
    if col:
        col.kill()
        increase_score(websocket_update_score_client, user_id)


def game_loop(websocket_leaderboard_client, websocket_rank_client, websocket_update_score_client, username):
    pygame.init()
    CLOCK = pygame.time.Clock()
    FPS = 120

    screen, bg, x = initialize_screen(username)
    player, apples, all_sprites = initialize_assets()

    # adding event that creates apple objects
    ADD_APPLE = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_APPLE, random.randint(1000, 1500))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == ADD_APPLE:
                add_apple(apples, all_sprites)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            x = move_background(screen, bg, x)
        else:
            screen.blit(bg, (x, 0))

        player.update(pressed_keys)
        apples.update(pressed_keys, apples, all_sprites)
        # pygame.display.update( )
        text, text_rect = display_score(websocket_rank_client)
        top_leaderboard_texts = display_top_leaderboards(websocket_leaderboard_client)

        screen.blit(text, text_rect)
        for text, text_rect in top_leaderboard_texts:
            screen.blit(text, text_rect)

        for entity in all_sprites:
            try:
                screen.blit(entity.surf, entity.rect)
            except AttributeError:
                screen.blit(entity.curr_image, entity.rect)

        handle_collision(player, apples, websocket_update_score_client, user_id)

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    user_id = input("enter your username: ")

    websocket_update_score_client = WebsocketUpdateScore()
    websocket_leaderboard_client = WebsocketLeaderboard()
    websocket_rank_client = WebsocketRank(username=user_id)

    game_loop(websocket_leaderboard_client, websocket_rank_client, websocket_update_score_client, user_id)
