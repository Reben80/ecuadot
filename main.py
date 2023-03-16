import pygame
import numpy as np
import os

# Set up Pygame
pygame.init()
pygame.mixer.init()
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Define the size of the window
WINDOW_SIZE = (800, 800)

# Set up the Pygame window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Ecuadot Game")

# Define some colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define the size of the grid
n = 5

# Define the size of the cells
cell_size = int(WINDOW_SIZE[0] / n)

# Define the font for displaying text
font = pygame.font.SysFont(None, 30)

# Create a bumpy array of size n by n with all elements initialized to zero
grid = np.zeros((n, n), dtype=int)

# Define the current player
current_player = 1

# Load the sound effect files
click_sound = pygame.mixer.Sound('/Users/Rebin/PycharmProjects/pythonProject17/sound/click_sound.wav')
lose_sound = pygame.mixer.Sound('/Users/Rebin/PycharmProjects/pythonProject17/sound/lose_sound.wav')

# Define a function to draw the grid
def draw_grid():
    for i in range(n):
        for j in range(n):
            # Determine the position of the cell
            x = j * cell_size
            y = i * cell_size

            # Determine the color of the cell
            if (i + j) % 2 == 0:
                color = BLACK
            else:
                color = WHITE

            # Draw the cell
            pygame.draw.rect(screen, color, [x, y, cell_size, cell_size], 0)

            # Draw a circle in the cell
            if grid[i, j] > 0:
                pygame.draw.circle(screen, RED, [x + int(cell_size / 2), y + int(cell_size / 2)], int(cell_size / 4))

    # Update the screen
    pygame.display.update()
# Define a function to calculate distances between non-zero elements in the grid
def calculate_distances():
    if np.count_nonzero(grid) > 1:
        positions = np.transpose(np.nonzero(grid))
        distances = []
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                dist = np.sqrt((positions[i][0] - positions[j][0]) ** 2 + (positions[i][1] - positions[j][1]) ** 2)
                distances.append(dist)
        unique_distances = np.unique(distances)

        if len(unique_distances) != len(distances):
            # A repeated distance has been found, end the game
            winner = 2 if current_player == 1 else 1
            print(f"Player {winner} has lost! Game over.")
            lose_sound.play()
            winner_color = RED if winner == 1 else WHITE
            loser_color = WHITE if winner == 1 else RED

            # Change the color of the cells to indicate the winner
            for i in range(n):
                for j in range(n):
                    if grid[i, j] == winner:
                        color = winner_color
                    else:
                        color = BLACK
                    pygame.draw.rect(screen, color, [j * cell_size, i * cell_size, cell_size, cell_size], 0)
                    if grid[i, j] > 0:
                        pygame.draw.circle(screen, BLUE,
                                           [j * cell_size + int(cell_size / 2), i * cell_size + int(cell_size / 2)],
                                           int(cell_size / 4))

            # Update the screen
            pygame.display.update()
            return True

    return False

# Game loop
game_over = False
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            x, y = pygame.mouse.get_pos()

            # Determine the row and column of the clicked cell
            row = int(y / cell_size)
            col = int(x / cell_size)

            # Place a dot in the cell if it is empty
            if grid[row, col] == 0:
                grid[row, col] = current_player
                click_sound.play()

                # Calculate distances and switch players
                game_over = calculate_distances()
                current_player = 2 if current_player == 1 else 1

    #    # Draw the grid
    screen.fill(BLACK)
    draw_grid()

    # Update the screen
    pygame.display.update()

# Clean up Pygame
pygame.quit()
