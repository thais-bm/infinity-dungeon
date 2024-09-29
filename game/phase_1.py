import pygame
import sys


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

    # Player
    player_pos = [7, 6]  # Começa na posição (1, 1)
    TILE_SIZE = 48

    # Colors
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    TRANSPARECE = (0, 0, 0, 0)

    # Pygame Setup
    pygame.init()
    SCREEN_WIDTH = 624
    SCREEN_HEIGHT = 624
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tower Of God")

    # Menu loop
    game_loop = True
    game_clock = pygame.time.Clock()

    # Map
    bg = pygame.image.load('assets/assets_wall/Map003.png').convert()


    # draw walls
    def draw_maze():
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if maze[row][col] == 1:
                    transparent_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    transparent_surface.fill(TRANSPARECE)
                    screen.blit(transparent_surface, (col * TILE_SIZE, row * TILE_SIZE))


    def can_move(x, y):
        return maze[x][y] == 0


    def draw_player():
        sprite = pygame.image.load(f'assets/player_walking/tile00{0}.png').convert_alpha()
        rect_sprite = sprite.get_rect()
        rect_sprite.x = player_pos[1] * TILE_SIZE
        rect_sprite.y = player_pos[0] * TILE_SIZE
        screen.blit(sprite, rect_sprite)


    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if can_move(player_pos[0], player_pos[1] - 1):
                player_pos[1] -= 1
        if keys[pygame.K_RIGHT]:
            if can_move(player_pos[0], player_pos[1] + 1):
                player_pos[1] += 1
        if keys[pygame.K_UP]:
            if can_move(player_pos[0] - 1, player_pos[1]):
                player_pos[0] -= 1
        if keys[pygame.K_DOWN]:
            if can_move(player_pos[0] + 1, player_pos[1]):
                player_pos[0] += 1

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
        draw_maze()
        draw_player()

        pygame.display.update()
        pygame.display.flip()

        pygame.time.Clock().tick(10)

    pygame.quit()
    sys.exit()
