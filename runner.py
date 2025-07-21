import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 1
JUMP_STRENGTH = 20
OBSTACLE_SPEED = 10
PLAYER_SPEED = 5
GROUND_HEIGHT = SCREEN_HEIGHT - 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Subway Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = 100
        self.y = GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.jumping = False
        self.lane = 1  # 0: left, 1: middle, 2: right
        self.lane_positions = [150, SCREEN_WIDTH // 2 - self.width // 2, SCREEN_WIDTH - 150 - self.width]
        
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Check if landed on ground
        if self.y >= GROUND_HEIGHT - self.height:
            self.y = GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.jumping = False
            
        # Update x position based on lane
        target_x = self.lane_positions[self.lane]
        if self.x < target_x:
            self.x = min(self.x + PLAYER_SPEED, target_x)
        elif self.x > target_x:
            self.x = max(self.x - PLAYER_SPEED, target_x)
    
    def jump(self):
        if not self.jumping:
            self.vel_y = -JUMP_STRENGTH
            self.jumping = True
    
    def change_lane(self, direction):
        if direction == "left" and self.lane > 0:
            self.lane -= 1
        elif direction == "right" and self.lane < 2:
            self.lane += 1
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        # Draw a simple head
        pygame.draw.circle(screen, (255, 200, 150), (self.x + self.width // 2, self.y + 20), 15)

class Obstacle:
    def __init__(self, lane):
        self.width = 40
        self.height = 60
        self.lane = lane
        self.x = 0
        self.y = GROUND_HEIGHT - self.height
        self.lane_positions = [150, SCREEN_WIDTH // 2 - self.width // 2, SCREEN_WIDTH - 150 - self.width]
        self.passed = False  # Added this attribute
        self.reset()
        
    def reset(self):
        self.lane = random.randint(0, 2)
        self.x = SCREEN_WIDTH
        self.y = GROUND_HEIGHT - self.height
        self.passed = False  # Reset this when obstacle resets
        
    def update(self):
        self.x -= OBSTACLE_SPEED
        if self.x < -self.width:
            self.reset()
            
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        
    def collides_with(self, player):
        if (player.x < self.x + self.width and
            player.x + player.width > self.x and
            player.y < self.y + self.height and
            player.y + player.height > self.y):
            return True
        return False

def draw_ground():
    pygame.draw.rect(screen, GRAY, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

def draw_lanes():
    lane_width = SCREEN_WIDTH // 3
    pygame.draw.line(screen, WHITE, (lane_width, 0), (lane_width, SCREEN_HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (lane_width * 2, 0), (lane_width * 2, SCREEN_HEIGHT), 2)

def game_loop():
    player = Player()
    obstacles = [Obstacle(random.randint(0, 2)) for _ in range(3)]
    score = 0
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    elif event.key == pygame.K_LEFT:
                        player.change_lane("left")
                    elif event.key == pygame.K_RIGHT:
                        player.change_lane("right")
                else:
                    if event.key == pygame.K_r:
                        return  # Restart game
        
        if not game_over:
            # Update game objects
            player.update()
            for obstacle in obstacles:
                obstacle.update()
                
                # Check for collisions
                if obstacle.collides_with(player):
                    game_over = True
                
                # Score points when passing obstacles
                if obstacle.x + obstacle.width < player.x and not obstacle.passed:
                    score += 1
                    obstacle.passed = True
            
            # Increase difficulty
            if score > 0 and score % 5 == 0:
                global OBSTACLE_SPEED
                OBSTACLE_SPEED = 10 + score // 5
        
        # Draw everything
        screen.fill(BLACK)
        draw_lanes()
        draw_ground()
        player.draw()
        for obstacle in obstacles:
            obstacle.draw()
        
        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(60)

# Main game loop
while True:
    game_loop()