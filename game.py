import pygame
import sys
import random

pygame.init()

# Set up the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Evolutionary Falling Objects Game")

# Set up the player rectangle
player_color = (0, 128, 255)  # RGB color
player_width, player_height = 50, 50
player_x, player_y = (width - player_width) // 2, height - player_height - 20

# Set up falling object
object_width, object_height = 30, 30
object_speed = 5
object_x, object_y = random.randint(0, width - object_width), 0

# Initialize score, stage, and lives
score = 0
stage = 1
lives = 3
font = pygame.font.Font(None, 36)

# Set up player name input
player_name = ""
input_active = True
font_small = pygame.font.Font(None, 24)

# Function to display game over message
def show_game_over():
    game_over_text = font.render(f"Game Over {player_name}- Press 'R' to Try Again", True, (255, 0, 0))
    screen.blit(game_over_text, ((width - game_over_text.get_width()) // 2, (height - game_over_text.get_height()) // 2))

# Function to display score, stage, and lives
def show_game_stats():
    stats_text = font.render(f"Score: {score} | Stage: {stage} | Lives: {lives}", True, (0, 0, 0))
    screen.blit(stats_text, (10, 10))

# Function to display player name
def show_player_name():
    player_name_text = font_small.render(f"Player: {player_name}", True, (0, 0, 0))
    screen.blit(player_name_text, (width - player_name_text.get_width() - 10, 10))

# Function to handle player name input
def handle_name_input(event):
    global player_name, input_active

    if event.key == pygame.K_RETURN:
        input_active = False
    elif event.key == pygame.K_BACKSPACE:
        player_name = player_name[:-1]
    elif event.unicode.isalnum() or event.unicode.isspace():
        player_name += event.unicode

# Name input loop
while input_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            handle_name_input(event)

    screen.fill((255, 255, 255))

    name_input_text = font_small.render(f"Enter Your Name: {player_name}", True, (0, 0, 0))
    screen.blit(name_input_text, ((width - name_input_text.get_width()) // 2, (height - name_input_text.get_height()) // 2))

    pygame.display.flip()

# Game loop
clock = pygame.time.Clock()
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the game when 'R' is pressed
                player_name = ""
                score = 0
                stage = 1
                lives = 3
                object_speed = 5
                object_y = 0
                object_x = random.randint(0, width - object_width)
                game_over = False
            elif event.key == pygame.K_BACKSPACE:
                # Handle backspace to delete characters in the player name input
                player_name = player_name[:-1]
            elif input_active:
                # Handle key input for player name
                handle_name_input(event)

    if not game_over:
        # Game logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += 5

        object_y += object_speed

        if (
            player_x < object_x + object_width
            and player_x + player_width > object_x
            and player_y < object_y + object_height
            and player_y + player_height > object_y
        ):
            score += 1

            if score == 20:
                stage = 2
                object_speed += 2
            elif score == 50:
                stage = 3
                object_speed += 2

            object_y = 0
            object_x = random.randint(0, width - object_width)

        if object_y > height:
            lives -= 1

            if lives == 0:
                show_game_over()
                game_over = True

                object_y = 0
                object_x = random.randint(0, width - object_width)

    screen.fill((255, 255, 255))

    if not game_over:
        pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

        if stage == 1:
            object_color = (255, 0, 0)
        elif stage == 2:
            object_color = (0, 255, 0)
        elif stage == 3:
            object_color = (0, 0, 255)

        pygame.draw.rect(screen, object_color, (object_x, object_y, object_width, object_height))

        show_game_stats()
        show_player_name()

        pygame.display.flip()
    else:
        show_game_over()
        pygame.display.flip()

    clock.tick(60)
