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
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('assets/monster_2/tile000.png').convert_alpha()  # Tamanho do monstro
            self.rect = self.image.get_rect(topleft=(x, y))
            self.speed = 2  # Velocidade do monstro

        def update(self, player_pos):
            # Move em direção ao jogador
            if self.rect.x < player_pos[1] * 48:
                self.rect.x += self.speed
            elif self.rect.x > player_pos[1] * 48:
                self.rect.x -= self.speed

            if self.rect.y < player_pos[0] * 48:
                self.rect.y += self.speed
            elif self.rect.y > player_pos[0] * 48:
                self.rect.y -= self.speed

    # Player
    player_pos = [7, 6]  # Começa na posição (1, 1)
    TILE_SIZE = 48
    player_vida = 3

    # bullet
    all_bullets = pygame.sprite.Group()
    all_monsters = pygame.sprite.Group()

    for i in range(5):  # Número de monstros
        monster = Monster(1 * TILE_SIZE, 5 * TILE_SIZE + i * 50)  # Colocar monstros em posições diferentes
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

        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if can_move(player_pos[0], player_pos[1] - 1):
                player_pos[1] -= 1
        elif keys[pygame.K_RIGHT]:
            if can_move(player_pos[0], player_pos[1] + 1):
                player_pos[1] += 1
        elif keys[pygame.K_UP]:
            if can_move(player_pos[0] - 1, player_pos[1]):
                player_pos[0] -= 1
        elif keys[pygame.K_DOWN]:
            if can_move(player_pos[0] + 1, player_pos[1]):
                player_pos[0] += 1
        if keys[pygame.K_z]:
            bullet = Bullet(rect_sprite.centerx, rect_sprite.centery)  # Cria uma nova bala
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

        # Load Map
        screen.blit(bg, (0, 0))
        draw_player()

        all_bullets.draw(screen)
        all_monsters.draw(screen)

        all_bullets.update()
        all_monsters.update(player_pos)


        for bullet in all_bullets:
            hit_monsters = pygame.sprite.spritecollide(bullet, all_monsters, True)
            if hit_monsters:
                bullet.kill()
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