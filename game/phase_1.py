import random

import pygame
import sys

"""
TO-DO LIST
O que tá pegando
-> Player anda para as quatro direcoes
-> Não há delay de tiro
-> Colisão player parede funciona, player-monstro, monstro-monstro
-> Surge apenas 3 mosntros de forma hardcoded

Da lista do professor só tem 3 mecanicas adicionadas
-> Visao TOP-DOWN
-> Personagem movimenta nas quatro direcoes
-> Personagem atira (o inimigo nao, mas n sei se os dois precisam atirar)

O que falta:
-> Tiro quebrar blocos (poderia usar isso qnd a saida é uma rachadura na parede)
-> Tiro atravessa bloco e rebate na parede

A parte urgente (?)
-> Deixar tudo isso linkado ao maximo a matriz (pa liberar ctrl_C e ctrl_v)
-> Desbugar o contador de vida
-> TINHA ESQUECIDO: A BALA PRECISA COLIDIR COM A PAREDE E REBATER 
-> E a bala precisa atravessar bloco, isso pode ficar pra alguma das salas

Opcional
-> Animação dos boneco
-> Fade in e Fade Out
-> Levar as classes para o classes/player.py n vai precisar repetir as classes aqui presentes 0913292 vezes
-> Naturalizar a mov dos monstros hihi

O QUE FOI FEITO, só que PRECISA DE TESTES
-> É possivel atirar para os lados, mas é preciso corrigir ao atirar para baixo, a bala não desaparece e fica no fundo
    da tela ao atirar para baixo (EDIT: acho que ta corrigido)
-> Evitar que os monstros comecem a colidir entre si 
-> Adicionar colisão dos monstros com paredes
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
    pygame.display.set_caption("Infinite Dungeon")

    # Colors
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    TILE_SIZE = 48

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 20
            self.direction = direction

        def update(self):
            if self.direction == 'Up':
                self.rect.y -= self.speed
            elif self.direction == 'Down':
                self.rect.y += self.speed
            elif self.direction == 'Left':
                self.rect.x -= self.speed
            elif self.direction == 'Right':
                self.rect.x += self.speed
            if self.rect.bottom <= 0 or self.rect.top >= 624 or self.rect.right <= 0 or self.rect.left >= 624:
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
                    self.image = pygame.image.load('assets/monster_2/tile006.png').convert_alpha()
            elif self.rect.x > player_pos[1] * TILE_SIZE:  # Player is in the right
                if can_move(column - 1, row) and (column - 1, row) not in busy_position:
                    self.rect.x -= self.speed
                    self.image = pygame.image.load('assets/monster_2/tile003.png').convert_alpha()
            if self.rect.y < player_pos[0] * TILE_SIZE:  # Player is downwards
                if can_move(column, row + 1) and (column, row + 1) not in busy_position:
                    self.rect.y += self.speed
                    self.image = pygame.image.load('assets/monster_2/tile000.png').convert_alpha()
            elif self.rect.y > player_pos[0] * TILE_SIZE:  # Player is upwards
                if can_move(column, row - 1) and (column, row - 1) not in busy_position:
                    self.rect.y -= self.speed
                    self.image = pygame.image.load('assets/monster_2/tile009.png').convert_alpha()

    # Under construction
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.life = 3
            self.position = [7, 6]
            self.invulnerable = False
            self.invulnerable_timer = 0
            self.direction = 'Down'  # Up, Down, Left, Right
            self.image = pygame.image.load(f'assets/player_walking/tile00{0}.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = self.position[1] * TILE_SIZE
            self.rect.y = self.position[0] * TILE_SIZE
            self.last_shot_time = pygame.time.get_ticks()
            self.shoot_delay = 700

        def move(self, keys):
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if can_move(self.position[0], self.position[1] - 1):
                    self.position[1] -= 1
                    self.direction = 'Left'
                    self.image = pygame.image.load(f'assets/player_walking/tile003.png').convert_alpha()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if can_move(self.position[0], self.position[1] + 1):
                    self.position[1] += 1
                    self.direction = 'Right'
                    self.image = pygame.image.load(f'assets/player_walking/tile006.png').convert_alpha()
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                if can_move(self.position[0] - 1, self.position[1]):
                    self.position[0] -= 1
                    self.direction = 'Up'
                    self.image = pygame.image.load(f'assets/player_walking/tile009.png').convert_alpha()
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if can_move(self.position[0] + 1, self.position[1]):
                    self.position[0] += 1
                    self.direction = 'Down'
                    self.image = pygame.image.load(f'assets/player_walking/tile000.png').convert_alpha()

        def shoot(self):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.shoot_delay:
                bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
                all_bullets.add(bullet)
                self.last_shot_time = current_time
                print('piu piu')

        def take_damage(self):
            if not self.invulnerable:
                self.life -= 1
                self.invulnerable = True
                self.image = pygame.image.load(f'assets/monster_1/tile000.png').convert_alpha() # So pra piscar
                print('Invencivel')
                self.invulnerable_timer = pygame.time.get_ticks()
                if self.life <= 0:
                    print('game ouver hihi')


        def draw(self, screen):
            screen.blit(self.image, self.rect)


        def update(self):
            if self.invulnerable:
                if pygame.time.get_ticks() - self.invulnerable_timer > 5000:  # 2s of invunerable
                    self.invulnerable = False
                    self.image = pygame.image.load(f'assets/player_walking/tile000.png').convert_alpha()
                    print('Nao ta invencivel')
            self.rect.x = self.position[1] * TILE_SIZE
            self.rect.y = self.position[0] * TILE_SIZE

    # Player
    player = Player()

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
        stats_bg = pygame.Surface((624, 100))
        stats_bg.fill(COLOR_BLACK)
        font = pygame.font.Font('assets/SegaArcadeFont-Regular.ttf', 30)
        life = font.render(f'VIDA: {player.life}', True, COLOR_WHITE)
        life_rect = life.get_rect(bottomleft=(100, 700))
        screen.blit(stats_bg, (0, 624))
        screen.blit(life, life_rect)


    def can_move(x, y):
        return maze[x][y] == 0


    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        # Player Movement
        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_z]:
            player.shoot()

        # Mudanca mapa
        if player.position[0] < 0:  # top
            player.position[0] = 12
        if player.position[0] > 12:  # Bottom
            player.position[0] = 0
        if player.position[1] < 0:  # Left
            player.position[1] = 12
        if player.position[1] > 12:  # Right
            player.position[1] = 0

        # Load Map + player + bullet + monster
        screen.blit(bg, (0, 0))
        player.update()
        player.draw(screen)
        all_bullets.draw(screen)
        all_monsters.draw(screen)
        all_bullets.update()
        all_monsters.update(player.position)

        # Bullet-Monsters Collision
        for bullet in all_bullets:
            hit_monsters = pygame.sprite.spritecollide(bullet, all_monsters, True)
            if hit_monsters:
                bullet.kill()
        # Monster-Player collision
        for monster in all_monsters:
            if player.rect.colliderect(monster.rect):
                # Ideal -> invunerabilidade
                player.take_damage()

        show_stats()

        if player.life <= 0:
            print("Game ouver")
            game_loop = False

        # Debub Monster part
        print('Debug mode')
        for index, monster in enumerate(all_monsters):
            print(f'{index} ---> X: {monster.rect.x // TILE_SIZE} and Y: {monster.rect.y // TILE_SIZE}')

        pygame.display.update()
        pygame.display.flip()

        pygame.time.Clock().tick(10)

    pygame.quit()
    sys.exit()

iniciar()