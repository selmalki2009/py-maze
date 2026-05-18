import pygame
import sys

# ==========================================
# 1. INITIALIZATION & CONSTANTS
# ==========================================
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
FPS = 80

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 128)
RED = (255, 36, 0)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Explorer - Salma's Edition")
clock = pygame.time.Clock()

# ==========================================
# 2. SPRITE CLASSES
# ==========================================
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        # Save starting position
        self.start_x = x * TILE_SIZE + 5
        self.start_y = y * TILE_SIZE + 5

        self.rect.x = self.start_x
        self.rect.y = self.start_y

        self.speed = 5
        self.facing = "E"  # E, W, N, S

    def update(self, walls):
        # Save old position
        old_x = self.rect.x
        old_y = self.rect.y

        keys = pygame.key.get_pressed()

        # Player movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.facing = "W"

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.facing = "E"

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.facing = "N"

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.facing = "S"

        # Wall collision
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x = old_x
                self.rect.y = old_y
                break


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.rect.x = x * TILE_SIZE + 5
        self.rect.y = y * TILE_SIZE + 5

        self.move_timer = 0
        self.direction = 1

    def update(self):
        # Simple vertical movement
        self.move_timer += 1

        if self.move_timer > 30:
            self.direction *= -1
            self.move_timer = 0

        self.rect.y += self.direction * 2


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

        self.speed = 10
        self.direction = direction

    def update(self):
        if self.direction == "E":
            self.rect.x += self.speed
        elif self.direction == "W":
            self.rect.x -= self.speed
        elif self.direction == "N":
            self.rect.y -= self.speed
        elif self.direction == "S":
            self.rect.y += self.speed

        # Remove bullet if off-screen
        if (
            self.rect.right < 0
            or self.rect.left > WIDTH
            or self.rect.bottom < 0
            or self.rect.top > HEIGHT
        ):
            self.kill()


# ==========================================
# 3. LEVEL DESIGN
# ==========================================
# W = Wall, P = Player, E = Enemy, G = Goal
level_map = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WP                EW",
    "W  WWWWW   WWWWWWWEW",
    "W  W       W   W   W",
    "W  W       W       W",
    "W  WWWWWEEEWWWWW   W",
    "W      W   W   W   W",
    "W      W   W E W   W",
    "W  WWWWW   W   W   W",
    "W  E           E   W",
    "W W            W  GW",
    "WWWWWWWWWWWWWWWWWWWW",
]


# ==========================================
# 4. SPRITE GROUPS
# ==========================================
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
goals = pygame.sprite.Group()

player = None

# Parse level
for row_index, row in enumerate(level_map):
    for col_index, char in enumerate(row):
        if char == "W":
            wall = Wall(col_index, row_index)
            all_sprites.add(wall)
            walls.add(wall)

        elif char == "P":
            player = Player(col_index, row_index)
            all_sprites.add(player)

        elif char == "E":
            enemy = Enemy(col_index, row_index)
            all_sprites.add(enemy)
            enemies.add(enemy)

        elif char == "G":
            goal = Goal(col_index, row_index)
            all_sprites.add(goal)
            goals.add(goal)


# ==========================================
# 5. MAIN GAME LOOP
# ==========================================
running = True

while running:
    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(
                    player.rect.centerx,
                    player.rect.centery,
                    player.facing
                )
                all_sprites.add(bullet)
                bullets.add(bullet)

    #  UPDATE
    player.update(walls)
    enemies.update()
    bullets.update()

    # Bullet vs Enemy collision
    pygame.sprite.groupcollide(bullets, enemies, True, True)

    # Player vs Enemy collision
    if pygame.sprite.spritecollide(player, enemies, False):
        player.rect.x = player.start_x
        player.rect.y = player.start_y

    # Player vs Goal collision
    if pygame.sprite.spritecollide(player, goals, False):
        print("YOU WIN!")
        running = False

    # DRAW
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

# ==========================================
# 6. QUIT GAME
# ==========================================
pygame.quit()
sys.exit()