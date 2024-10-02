import random

import pygame
import sys

"""
TO-DO LIST
A parte urgente (?)
-> Evitar que os monstros comecem a colidir entre si
-> Adicionar colisão dos monstros com paredes
-> Dar um jeito de atirar pros lados
-> Deixar tudo isso linkado ao maximo a matriz (pa liberar ctrl_C e ctrl_v)
-> Desbugar o contador de vida

Opcional
-> Animação dos boneco
-> Fade in e Fade Out
-> Levar as classes para o classes/player.py n vai precisar repetir as classes aqui presentes 0913292 vezes
-> Naturalizar a mov dos monstros hihi
"""


def iniciar():
    # Matriz
    maze = [
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    ]

    # Pygame Setup
    pygame.init()
    SCREEN_WIDTH = 624
    SCREEN_HEIGHT = 724
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tower Of God")

    # Colors
    COLOR_WHITE = (255, 255, 255)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 20

        def update(self):
            self.rect.y -= self.speed
            if self.rect.bottom < 0:
                self.kill()
            for lane in range(len(maze)):
                for col in range(len(maze[lane])):
                    if maze[lane][col] == 1:
                        wall_rect = pygame.Rect(col * TILE_SIZE, lane * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if self.rect.colliderect(wall_rect):
                            self.kill()

    class Monster(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            pygame.sprite.Sprite.__init__(self)
            self.position = [pos_x, pos_y]
            self.image = pygame.image.load('assets/monster_2/tile000.png').convert_alpha()  # Tamanho do monstro
            self.rect = self.image.get_rect(topleft=(self.position[0] * TILE_SIZE, self.position[1] * TILE_SIZE))
            self.speed = 5

        def update(self, player_pos):
            # Monster actual position in the 'Maze'
            row = int(self.rect.y // TILE_SIZE)  # Y - lane
            column = int(self.rect.x // TILE_SIZE)  # X - column



            # Get other monsters position and add in a list
            busy_position = set()
            for monster in all_monsters:
                if monster != self:
                    other_row = int(monster.rect.y // TILE_SIZE)
                    other_column = int(monster.rect.x // TILE_SIZE)
                    busy_position.add((other_column, other_row))

            # Monsters mov
            # Collision with walls and other monsters
            if self.rect.x < player_pos[1] * TILE_SIZE:  # Player is in the left
                if can_move(column + 1, row) and (column + 1, row) not in busy_position:
                    self.rect.x += self.speed
            elif self.rect.x > player_pos[1] * TILE_SIZE:  # Player is in the right
                if can_move(column - 1, row) and (column - 1, row) not in busy_position:
                    self.rect.x -= self.speed

            if self.rect.y < player_pos[0] * TILE_SIZE:  # Player is downwards
                if can_move(column, row + 1) and (column, row + 1) not in busy_position:
                    self.rect.y += self.speed
            elif self.rect.y > player_pos[0] * TILE_SIZE:  # Player is upwards
                if can_move(column, row - 1) and (column, row - 1) not in busy_position:
                    self.rect.y -= self.speed

    # Under construction
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.life = 3
            self.position = [7, 6]
            self.direction = 'Down'  # Up, Down, Left, Right
            self.sprites = []
            self.image = pygame.image.load(f'assets/player_walking/tile00{0}.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = self.position[1] * TILE_SIZE
            self.rect.y = self.position[0] * TILE_SIZE

    # Player
    player_pos = [7, 6]  # Começa na posição (1, 1)
    TILE_SIZE = 48
    player_vida = 9999

    # bullet
    all_bullets = pygame.sprite.Group()
    all_monsters = pygame.sprite.Group()

    # Fiz hardcoded até saber o que fazer
    monster = Monster(2, 7)
    all_monsters.add(monster)
    monster = Monster(6, 2)
    all_monsters.add(monster)
    monster = Monster(5, 3)
    all_monsters.add(monster)

    # Menu loop
    game_loop = True

    # Map
    bg = pygame.image.load('assets/assets_wall/Map003.png').convert()

    def show_stats():
        font = pygame.font.Font('assets/SegaArcadeFont-Regular.ttf', 50)
        life = font.render('VIDA: ', True, COLOR_WHITE)
        life_number = font.render(str(player_vida), True, COLOR_WHITE)
        life_rect = life.get_rect(bottomleft=(100, 700))
        life_number_rect = life_number.get_rect(bottomleft=(200, 700))
        screen.blit(life, life_rect)
        screen.blit(life_number, life_number_rect)


    def can_move(x, y):
        return maze[x][y] == 0


    def draw_player():
        sprite = pygame.image.load(f'assets/player_walking/tile00{0}.png').convert_alpha()
        rect_sprite = sprite.get_rect()
        rect_sprite.x = player_pos[1] * TILE_SIZE
        rect_sprite.y = player_pos[0] * TILE_SIZE
        screen.blit(sprite, rect_sprite)

        return rect_sprite


    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        rect_sprite = draw_player()

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if can_move(player_pos[0], player_pos[1] - 1):
                player_pos[1] -= 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if can_move(player_pos[0], player_pos[1] + 1):
                player_pos[1] += 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if can_move(player_pos[0] - 1, player_pos[1]):
                player_pos[0] -= 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if can_move(player_pos[0] + 1, player_pos[1]):
                player_pos[0] += 1
        if keys[pygame.K_z]:
            bullet = Bullet(rect_sprite.centerx, rect_sprite.centery)  # Create a Bullet
            all_bullets.add(bullet)
            print('piu piu')

        # Mudanca mapa
        if player_pos[0] < 0:  # top
            player_pos[0] = 12
        if player_pos[0] > 12:  # Bottom
            player_pos[0] = 0
        if player_pos[1] < 0:  # Left
            player_pos[1] = 12
        if player_pos[1] > 12:  # Right
            player_pos[1] = 0

        # Load Map + pplayer + bullet + monster
        screen.blit(bg, (0, 0))
        draw_player()

        all_bullets.draw(screen)
        all_monsters.draw(screen)

        print('Debug mode')
        for index, monster in enumerate(all_monsters):
            print(f'{index} ---> X: {monster.rect.x//TILE_SIZE} and Y: {monster.rect.y//TILE_SIZE}')

        # Updating position for monsters and bullets
        all_bullets.update()
        all_monsters.update(player_pos)

        # Bullet-Monsters Collision
        for bullet in all_bullets:
            hit_monsters = pygame.sprite.spritecollide(bullet, all_monsters, True)
            if hit_monsters:
                bullet.kill()

        # Monster-Player collision
        for monster in all_monsters:
            if rect_sprite.colliderect(monster.rect):
                monster.rect.x = (player_pos[0] + (1 * TILE_SIZE))
                player_vida -= 1

        show_stats()

        if player_vida <= 0:
            print("Game ouver")
            game_loop = False

        pygame.display.update()
        pygame.display.flip()

        pygame.time.Clock().tick(10)

    pygame.quit()
    sys.exit()

iniciar()