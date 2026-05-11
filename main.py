import pygame
import sys

# ==========================================
# 1. INITIALIZATION & CONSTANTS
# ==========================================
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
TILE_SIZE = 40
FPS = 80

# Colors (Students can change these!)
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
        # To use an image later: self.image = pygame.image.load("player.png")
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        # Save starting position for when the player dies
        self.start_x = x * TILE_SIZE + 5
        self.start_y = y * TILE_SIZE + 5
        self.rect.x = self.start_x
        self.rect.y = self.start_y

        self.speed = 5
        self.facing = "E" # Helps bullets know which way to go

    def update(self, walls):
        # Save old position in case we hit a wall
        old_x = self.rect.x
        old_y = self.rect.y

        keys = pygame.key.get_pressed()

        # ==========================================
        # STUDENT TODO 1: PLAYER MOVEMENT
        
        # ==========================================
def update(self, walls):
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
for wall in walls:
    if self.rect.colliderect(wall.rect):
        self.rect.x = old_x
        self.rect.y = old_y

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
        # Simple enemy movement: wobble back and forth
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

        # Kill bullet if it goes off screen to save memory
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# ==========================================
# 3. LEVEL DESIGN (Highly Customizable)
# ==========================================
# W = Wall, P = Player Start, E = Enemy, G = Goal, Space = Empty
level_map = [
    "WP WWWWW   W   W  GW",
    "W  W       W   W   W",
    "W  W       W   W   W",
    "W  WWWWW   WWWWW   W",
    "W      W   W   W   W",
    "W      W   W   W   W",
    "WWWWWWW    W   W   W",
    "W                E W",
    "W                  W",
    "W                  W",
    "WWWWWWWWWWWWWWWWWWWW",
]


# Sprite Groups
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
goals = pygame.sprite.Group()

player = None

# Parse the level map
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
# 4. MAIN GAME LOOP
# ==========================================
running = True
while running:
    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # ==========================================
                # STUDENT TODO 2: SHOOTING
                # ==========================================
                # When SPACE is pressed, create a Bullet object.
                # Pass it the player's center x, center y, and facing direction.
                # Add the new bullet to 'all_sprites' and 'bullets' groups.

                bullet = Bullet(player.rect.centerx, player.rect.centery, player.facing)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # --- Updates ---
    # Update player (passing walls for collision check)
    player.update(walls)

    # Update other sprites
    enemies.update()
    bullets.update()

    # ==========================================
    # STUDENT TODO 3: BULLET VS ENEMY COLLISION
if pygame.sprite.groupcollide(bullets, enemies, True, True):
    player.rect.x = player.start_x
    player.rect.y = player.start_y
    
    # ==========================================
    # STUDENT TODO 4: PLAYER VS ENEMY COLLISION
if pygame.sprite.spritecollide(player, enemies, False):
    player.rect.x = player.start_x
    player.rect.y = player.start_y
    # STUDENT TODO 5: WIN CONDITION (PLAYER VS GOAL)
if pygame.sprite.spritecollide(player, goals, False):    
    print("YOU WIN!")    
    running = False

    # --- Drawing ---
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
