import pygame
import sys
import numpy as np

# Initialize pygame
pygame.init()

# Variables
block_size = 200
num_blocks_x = 3
num_blocks_y = 3
space_above_grid = 30

# Constants
SCREEN_WIDTH = num_blocks_x * block_size
SCREEN_HEIGHT = num_blocks_y * block_size + space_above_grid
BLACK = (82*2.5, 96*2.5, 100*2.5)
UI_TEXT_COLOR = (0, 0, 0)
WHITE = (0, 0, 0)

RED = (2.5 * 100, 2.5 * 17.2, 2.5 * 27.3)
BLUE = (2.5 * 0, 2.5 * 73.3, 2.5 * 83)

# Function to draw grid
def draw_grid(screen, block_size, num_blocks_x, num_blocks_y):
    for x in range(block_size, SCREEN_WIDTH, block_size):
        pygame.draw.line(screen, WHITE, (x, space_above_grid), (x, SCREEN_HEIGHT))
    for y in range(space_above_grid, SCREEN_HEIGHT, block_size):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

# Function to get block coordinates from mouse position
def get_block_from_mouse(mouse_pos):
    block_x = mouse_pos[0] // block_size
    block_y = (mouse_pos[1] - space_above_grid) // block_size
    return block_x, block_y

def winner_detection(letter_grid, player, transpose=False, diagonal=False):
    if diagonal:

        grids = [
            np.fliplr(letter_grid),
            letter_grid
        ]

        for grid in grids:
            num_row = []
            for i in range(0, len(grid)):
                
                elem = grid[i][i]
                if elem == player:
                    num_row.append(1)
                else:
                    num_row.append(0)

            if sum(num_row) == 3:
                return True

        return False

    for row in letter_grid:
        num_row = []
        
        for elem in row:
            if elem == player:
                num_row.append(1)
            else:
                num_row.append(0)

        if sum(num_row) == 3:
            return True

    if transpose:
        if not diagonal:
            return winner_detection(np.transpose(letter_grid), player, transpose=False, diagonal=True)
        return False
    else:
        return winner_detection(np.transpose(letter_grid), player, transpose=True)

def render(screen, letter_grid, player, winner):
    font_player = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 36)

    player_text = player[0]
    
    screen.fill(BLACK)
    draw_grid(screen, block_size, num_blocks_x, num_blocks_y)

    # Draw texts in the space above the grid
    player_text_surface = font.render("Player Turn: %s" % player_text, True, UI_TEXT_COLOR)
    player_text_rect = player_text_surface.get_rect(midleft=(10, space_above_grid // 2))
    screen.blit(player_text_surface, player_text_rect)

    winner_text_surface = font.render("Winner:%s" % str(winner), True, UI_TEXT_COLOR)
    
    winner_text_rect = winner_text_surface.get_rect(midright=(SCREEN_WIDTH - 10, space_above_grid // 2))
    screen.blit(winner_text_surface, winner_text_rect)

    # Draw letters on the grid
    for y, row in enumerate(letter_grid):
        for x, letter in enumerate(row):
            player_color = WHITE
            
            if letter == "x":
                player_color = RED
                
            if letter == "o":
                player_color = BLUE
                
            letter_surface = font_player.render(letter, True, player_color)
            letter_rect = letter_surface.get_rect(center=(x * block_size + block_size // 2,
                                                           y * block_size + space_above_grid + block_size // 2))
            screen.blit(letter_surface, letter_rect)

    pygame.display.flip()

# Main function
def main():
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Grid")

    # Initialize letter grid
    letter_grid = [['' for _ in range(num_blocks_x)] for _ in range(num_blocks_y)]

    players = [
        ["x", RED],
        ["o", BLUE]
    ]
    
    player_turn = 0

    running = True
    winner = None

    total_turns = 9
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                if event.button == 1:
                    player_text = players[player_turn][0]
                    
                    mouse_pos = pygame.mouse.get_pos()
                    block_x, block_y = get_block_from_mouse(mouse_pos)

                    if letter_grid[block_y][block_x] == "":
                        letter_grid[block_y][block_x] = player_text

                        if winner_detection(letter_grid, player_text):
                            winner = player_text

                        player_turn += 1
                        player_turn = player_turn % 2
                        total_turns -= 1

        if total_turns == 0 and winner is None:
            winner = "Draw"

        render(screen, letter_grid, players[player_turn], winner)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
