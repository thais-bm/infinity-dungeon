import random
import pygame
import sys
import phase_2, phase_3, phase_5, phase_6

pygame.mixer.init()
move_fx = pygame.mixer.Sound("assets/audio/Move1.ogg")
evasion = pygame.mixer.Sound("assets/audio/Evasion.ogg")
attack = pygame.mixer.Sound("assets/audio/Attack.ogg")
hit = pygame.mixer.Sound("assets/audio/Slash.ogg")


def iniciar(life):
    # Matriz
    maze = [
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
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
            self.image = pygame.image.load("assets/magic.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 20
            self.direction = direction

        def update(self):
            if self.direction == 'Up':
                self.image = pygame.image.load('assets/bullet.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.image = pygame.transform.rotate(self.image, 180)
                self.rect.y -= self.speed
                self.rect.x -= 1
            elif self.direction == 'Down':
                self.image = pygame.image.load('assets/bullet.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.image = pygame.transform.rotate(self.image, 0)
                self.rect.y += self.speed
                self.rect.x -= 1
            elif self.direction == 'Left':
                self.image = pygame.image.load('assets/bullet.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.image = pygame.transform.rotate(self.image, -90)
                self.rect.x -= self.speed
                self.rect.x -= 1
            elif self.direction == 'Right':
                self.image = pygame.image.load('assets/bullet.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect.x += self.speed
                self.rect.x -= 1
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
            self.life = life
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
                pygame.mixer.Sound.play(attack)

        def take_damage(self):
            if not self.invulnerable:
                self.life -= 1
                self.invulnerable = True
                self.image = pygame.image.load(f'assets/player_damaged/tile001.png').convert_alpha()  # just blink
                pygame.mixer.Sound.play(evasion)
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

    # hardcoded (for now)
    monster = Monster(2, 6)
    all_monsters.add(monster)
    monster = Monster(7, 2)
    all_monsters.add(monster)
    monster = Monster(11, 6)
    all_monsters.add(monster)


    # Menu loop
    game_loop = True
    music = pygame.mixer.Sound("assets/audio/music.ogg")
    pygame.mixer.Sound.play(music, loops=-1)

    # Map
    bg = pygame.image.load('assets/assets_wall/Map003.png').convert()

    def show_stats():
        stats_bg = pygame.Surface((624, 100))
        stats_bg.fill(COLOR_BLACK)

        font = pygame.font.Font('assets/SegaArcadeFont-Regular.ttf', 30)

        if player.invulnerable:
            vunerable = 'Sim'
        else:
            vunerable = 'Nao'

        life = font.render(f'VIDA: {player.life}', True, COLOR_WHITE)
        power = font.render(f'Invencivel: {vunerable}',True, COLOR_WHITE)

        life_rect = life.get_rect(topleft=(100, 630))
        power_rect = power.get_rect(topleft=(100, 660))
        screen.blit(stats_bg, (0, 624))
        screen.blit(life, life_rect)
        screen.blit(power, power_rect)


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
            pygame.mixer.Sound.play(move_fx)
            phase_6.iniciar(player.life)
        if player.position[0] > 12:  # Bottom
            player.position[0] = 0
            pygame.mixer.Sound.play(move_fx)
            phase_3.iniciar(player.life)
            pygame.quit()
        if player.position[1] < 0:  # Left
            player.position[1] = 12
            pygame.mixer.Sound.play(move_fx)
            phase_5.iniciar(player.life)
            pygame.quit()
        if player.position[1] > 12:  # Right
            pygame.mixer.Sound.play(move_fx)
            phase_2.iniciar(player.life)
            pygame.quit()

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
                pygame.mixer.Sound.play(hit)
        # Monster-Player collision
        for monster in all_monsters:
            if player.rect.colliderect(monster.rect):
                # Ideal -> invunerabilidade
                player.take_damage()

        show_stats()

        if player.life <= 0:
            pygame.mixer.stop()
            bg_img = pygame.image.load('assets/game_over.png')
            gameover = pygame.mixer.Sound("assets/audio/Gameover.ogg")
            pygame.mixer.Sound.play(gameover)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            break

                screen.blit(bg_img, (0, 0))
                pygame.display.flip()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    break
            pygame.quit()
            sys.exit()


        pygame.display.update()
        pygame.display.flip()

        pygame.time.Clock().tick(10)

    pygame.quit()
    sys.exit()

#iniciar()