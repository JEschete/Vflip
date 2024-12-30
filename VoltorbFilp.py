"""
Voltorb Flip - Python Implementation

DESCRIPTION:
Voltorb Flip is a grid-based puzzle card game inspired by the minigame from the Pokémon series.
The objective of the game is to uncover cards in a grid without flipping over a "Voltorb".
Cards can contain multipliers (x2 or x3) or a safe value of x1. Voltorbs end the game if flipped.
Your goal is to maximize your score by uncovering cards with multipliers while avoiding Voltorbs.

This implementation recreates the experience of Voltorb Flip using Python and Pygame. 
Players interact with the grid by left-clicking to reveal a card or right-clicking to mark 
a suspected Voltorb with an exclamation mark ("!"). The game dynamically tracks scores and 
progress, and includes features such as level progression, random level decreases, and 
persistent scoring across sessions.

CREDITS:
The concept for Voltorb Flip comes from the Pokémon series, developed by Game Freak and 
published by Nintendo and The Pokémon Company. This implementation is an independent 
project inspired by the minigame, created for educational purposes.

REQUIREMENTS:
- Python 3.x
- Pygame library

To install Pygame, use the following command:
    pip install pygame

HOW TO PLAY:
1. Objective:
   - Your goal is to uncover cards with multipliers (x2 or x3) to maximize your score.
   - The level is over when all x2 and x3 cards have been revealed. 
   - Avoid flipping over Voltorbs, as they will end the game.

2. Controls:
   - Left-click: Reveal a card.
   - Right-click: Mark/unmark a card as a suspected Voltorb.

3. Scoring:
   - Each card you flip contributes to your current round score.
   - As the score is multiplicative, x1 cards do nothing for your score and do not progress the game. 
   - If you win the level, your current score is added to your total score.
   - Your total score persists across sessions.

4. Level Progression:
   - Levels increase in difficulty as you progress.
   - If you lose a level, there is a chance your level may decrease:
     - Small chance of dropping by 1 or 2 levels.
     - Very small chance of resetting to Level 1.

5. Other Features:
   - Persistent High Score: Tracks your highest total score across sessions.
   - Level Hints: Displays row and column hints to help you strategize.
   - Mark cards: Use the right-click to mark cards as suspected Voltorbs.

6. Game Menu:
   - Spend Points: Use 100 points from your total score to skip a level.
   - Reset Score: Reset your total score to start fresh.

7. Winning and Losing:
   - Winning a level adds your current round score to your total score.
   - Losing ends the round, and your level may decrease based on random chance.

Enjoy playing Voltorb Flip and strive for the highest score!

More details about the game can be found at:
https://bulbapedia.bulbagarden.net/wiki/Voltorb_Flip

"""

import pygame
import random
import sys
import pickle
import os

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 5  # 5x5 grid
CELL_SIZE = 80
CELL_MARGIN = 5
SIDEBAR_WIDTH = 220  # Width of the sidebar for text

# Calculate dynamic screen width
SCREEN_WIDTH = SIDEBAR_WIDTH + (CELL_SIZE + CELL_MARGIN) * 1.25 * BOARD_SIZE
SCREEN_HEIGHT = (CELL_SIZE + CELL_MARGIN) * BOARD_SIZE + 150  # Extra space for column hints and messages

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
SEMI_TRANSPARENT_BG = (255, 255, 255, 200)  # For message backgrounds

# Fonts
title_font = pygame.font.SysFont(None, 40)    # For main titles
score_font = pygame.font.SysFont(None, 28)    # For level and scores
small_font = pygame.font.SysFont(None, 22)    # For smaller text

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Voltorb Flip")

# Level configurations
LEVEL_CONFIGURATIONS = {
    1: [
        {'2s': 3, '3s': 1, 'Voltorbs': 6},
        {'2s': 0, '3s': 3, 'Voltorbs': 6},
        {'2s': 5, '3s': 0, 'Voltorbs': 6},
        {'2s': 2, '3s': 2, 'Voltorbs': 6},
        {'2s': 4, '3s': 1, 'Voltorbs': 6},
    ],
    2: [
        {'2s': 1, '3s': 3, 'Voltorbs': 7},
        {'2s': 6, '3s': 0, 'Voltorbs': 7},
        {'2s': 3, '3s': 2, 'Voltorbs': 7},
        {'2s': 0, '3s': 4, 'Voltorbs': 7},
        {'2s': 5, '3s': 1, 'Voltorbs': 7},
    ],
    3: [
        {'2s': 2, '3s': 3, 'Voltorbs': 8},
        {'2s': 7, '3s': 0, 'Voltorbs': 8},
        {'2s': 4, '3s': 2, 'Voltorbs': 8},
        {'2s': 1, '3s': 4, 'Voltorbs': 8},
        {'2s': 6, '3s': 1, 'Voltorbs': 8},
    ],
    4: [
        {'2s': 3, '3s': 3, 'Voltorbs': 8},
        {'2s': 0, '3s': 5, 'Voltorbs': 8},
        {'2s': 8, '3s': 0, 'Voltorbs': 10},
        {'2s': 5, '3s': 2, 'Voltorbs': 10},
        {'2s': 2, '3s': 4, 'Voltorbs': 10},
    ],
    5: [
        {'2s': 7, '3s': 1, 'Voltorbs': 10},
        {'2s': 4, '3s': 3, 'Voltorbs': 10},
        {'2s': 1, '3s': 5, 'Voltorbs': 10},
        {'2s': 9, '3s': 0, 'Voltorbs': 10},
        {'2s': 6, '3s': 2, 'Voltorbs': 10},
    ],
    6: [
        {'2s': 3, '3s': 4, 'Voltorbs': 10},
        {'2s': 0, '3s': 6, 'Voltorbs': 10},
        {'2s': 8, '3s': 1, 'Voltorbs': 10},
        {'2s': 5, '3s': 3, 'Voltorbs': 10},
        {'2s': 2, '3s': 5, 'Voltorbs': 10},
    ],
    7: [
        {'2s': 7, '3s': 2, 'Voltorbs': 10},
        {'2s': 4, '3s': 4, 'Voltorbs': 10},
        {'2s': 1, '3s': 6, 'Voltorbs': 13},
        {'2s': 9, '3s': 1, 'Voltorbs': 13},
        {'2s': 6, '3s': 3, 'Voltorbs': 10},
    ],
    8: [
        {'2s': 0, '3s': 7, 'Voltorbs': 10},
        {'2s': 8, '3s': 2, 'Voltorbs': 10},
        {'2s': 5, '3s': 4, 'Voltorbs': 10},
        {'2s': 2, '3s': 6, 'Voltorbs': 10},
        {'2s': 7, '3s': 3, 'Voltorbs': 10},
    ],
}

class Cell:
    def __init__(self, value, is_voltorb):
        self.value = value
        self.is_voltorb = is_voltorb
        self.flipped = False
        self.marked = False  # For '!' marks

class Board:
    def __init__(self, level, total_score):
        self.level = level
        self.board = self.generate_board()
        self.row_hints, self.col_hints = self.calculate_hints()
        self.score = 1  # Current round score
        self.total_score = total_score
        self.game_over = False
        self.win = False

    def generate_board(self):
        # The level configurations are assumed to be provided
        configurations = LEVEL_CONFIGURATIONS.get(
            self.level, LEVEL_CONFIGURATIONS[max(LEVEL_CONFIGURATIONS.keys())]
        )
        config = random.choice(configurations)
        num_2s = config['2s']
        num_3s = config['3s']
        num_voltorbs = config['Voltorbs']

        cells = []

        # Add Voltorbs
        for _ in range(num_voltorbs):
            cells.append(Cell(0, True))

        # Add ×2 cells
        for _ in range(num_2s):
            cells.append(Cell(2, False))

        # Add ×3 cells
        for _ in range(num_3s):
            cells.append(Cell(3, False))

        # Add ×1 cells
        total_cells = BOARD_SIZE * BOARD_SIZE
        num_1s = total_cells - num_voltorbs - num_2s - num_3s
        for _ in range(num_1s):
            cells.append(Cell(1, False))

        random.shuffle(cells)
        board = [cells[i * BOARD_SIZE:(i + 1) * BOARD_SIZE] for i in range(BOARD_SIZE)]
        return board

    def calculate_hints(self):
        row_hints = []
        col_hints = []

        for i in range(BOARD_SIZE):
            row_voltorbs = 0
            row_points = 0
            col_voltorbs = 0
            col_points = 0
            for j in range(BOARD_SIZE):
                # Row calculations
                cell = self.board[i][j]
                if cell.is_voltorb:
                    row_voltorbs += 1
                else:
                    row_points += cell.value

                # Column calculations
                cell = self.board[j][i]
                if cell.is_voltorb:
                    col_voltorbs += 1
                else:
                    col_points += cell.value

            row_hints.append((row_points, row_voltorbs))
            col_hints.append((col_points, col_voltorbs))

        return row_hints, col_hints

    def check_win(self):
        for row in self.board:
            for cell in row:
                if cell.value > 1 and not cell.flipped:
                    return False
        return True

    def flip_cell(self, row, col):
        cell = self.board[row][col]
        if cell.flipped:
            return
        cell.flipped = True
        if cell.is_voltorb:
            self.game_over = True
        else:
            if cell.value > 1:
                self.score *= cell.value
            if self.check_win():
                self.win = True

    def toggle_mark(self, row, col):
        cell = self.board[row][col]
        if not cell.flipped:
            cell.marked = not cell.marked

def calculate_level_decrease(level):
    baseline_chance = 0.1  # 10%
    per_level_increase = 0.05  # 5% per level above 1
    total_decrease_chance = baseline_chance + (level - 1) * per_level_increase
    if total_decrease_chance > 0.9:
        total_decrease_chance = 0.9  # Cap the total chance at 90%

    rand_value = random.random()

    if rand_value < total_decrease_chance:
        # Level will decrease
        # Now decide how much it will decrease
        # Define weights for the types of decrease
        chance_decrease_1 = 0.7  # 70% chance within decrease chance
        chance_decrease_2 = 0.2  # 20% chance
        chance_critical_decrease = 0.1  # 10% chance

        rand_decrease = random.random()

        if rand_decrease < chance_decrease_1:
            # Decrease level by 1
            new_level = max(1, level - 1)
            return new_level, "decreased by 1"
        elif rand_decrease < chance_decrease_1 + chance_decrease_2:
            # Decrease level by 2
            new_level = max(1, level - 2)
            return new_level, "decreased by 2"
        else:
            # Critical decrease to level 1
            new_level = 1
            return new_level, "reset to Level 1"
    else:
        # Level remains the same
        return level, "no change"

def draw_board(screen, board, high_score, level_decrease_message=""):
    # Adjusted margins to account for the sidebar
    x_margin = SIDEBAR_WIDTH + ((SCREEN_WIDTH - SIDEBAR_WIDTH - (CELL_SIZE + CELL_MARGIN) * BOARD_SIZE) // 2)
    y_margin = 50  # Starting from 50 pixels down to leave space for top texts

    # Draw cells
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell = board.board[row][col]
            cell_rect = pygame.Rect(
                x_margin + col * (CELL_SIZE + CELL_MARGIN),
                y_margin + row * (CELL_SIZE + CELL_MARGIN),
                CELL_SIZE,
                CELL_SIZE,
            )
            if cell.flipped:
                if cell.is_voltorb:
                    pygame.draw.rect(screen, RED, cell_rect)
                    text = score_font.render("V", True, BLACK)
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, LIGHT_GRAY, cell_rect)
                    text = score_font.render(str(cell.value), True, BLACK)
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, GRAY, cell_rect)
                if cell.marked:
                    text = score_font.render("!", True, BLACK)
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
            pygame.draw.rect(screen, BLACK, cell_rect, 1)

    # Draw row hints
    for row in range(BOARD_SIZE):
        points, voltorbs = board.row_hints[row]
        hint_text = small_font.render(f"{points}/{voltorbs}", True, BLACK)
        hint_rect = hint_text.get_rect()
        hint_rect.midleft = (
            x_margin + BOARD_SIZE * (CELL_SIZE + CELL_MARGIN) + 10,
            y_margin + row * (CELL_SIZE + CELL_MARGIN) + CELL_SIZE // 2,
        )
        screen.blit(hint_text, hint_rect)

    # Draw column hints
    for col in range(BOARD_SIZE):
        points, voltorbs = board.col_hints[col]
        hint_text = small_font.render(f"{points}/{voltorbs}", True, BLACK)
        hint_rect = hint_text.get_rect()
        hint_rect.midtop = (
            x_margin + col * (CELL_SIZE + CELL_MARGIN) + CELL_SIZE // 2,
            y_margin + BOARD_SIZE * (CELL_SIZE + CELL_MARGIN) + 10,
        )
        screen.blit(hint_text, hint_rect)

    # Sidebar positioning
    sidebar_x = 10  # Padding from the left edge
    sidebar_y = 50  # Starting y position
    line_height = 40  # Space between lines

    # Level Text
    level_text = score_font.render(f"Level: {board.level}", True, BLACK)
    level_rect = level_text.get_rect(topleft=(sidebar_x, sidebar_y))
    screen.blit(level_text, level_rect)

    # Current Points Text
    score_text = score_font.render(f"Current Points: {board.score}", True, BLACK)
    score_rect = score_text.get_rect(topleft=(sidebar_x, sidebar_y + line_height))
    screen.blit(score_text, score_rect)

    # Total Score Text
    total_score_text = score_font.render(f"Total Score: {board.total_score}", True, BLACK)
    total_score_rect = total_score_text.get_rect(topleft=(sidebar_x, sidebar_y + 2 * line_height))
    screen.blit(total_score_text, total_score_rect)

    # High Score Text
    high_score_text = score_font.render(f"High Score: {high_score}", True, BLACK)
    high_score_rect = high_score_text.get_rect(topleft=(sidebar_x, sidebar_y + 3 * line_height))
    screen.blit(high_score_text, high_score_rect)

    # Game over or win messages with background for better readability
    if board.game_over:
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(SEMI_TRANSPARENT_BG)
        screen.blit(overlay, (0, 0))

        game_over_text = title_font.render("Game Over!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(game_over_text, game_over_rect)

        # Display level decrease message if any
        if level_decrease_message:
            decrease_text = score_font.render(level_decrease_message, True, BLACK)
            decrease_rect = decrease_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(decrease_text, decrease_rect)

        restart_text = small_font.render("Press Enter to continue", True, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(restart_text, restart_rect)

    if board.win:
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(SEMI_TRANSPARENT_BG)
        screen.blit(overlay, (0, 0))

        win_text = title_font.render("Level Cleared!", True, BLACK)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(win_text, win_rect)

        next_level_text = small_font.render("Press Enter to continue", True, BLACK)
        next_level_rect = next_level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(next_level_text, next_level_rect)

def save_score(total_score, high_score):
    with open('score.dat', 'wb') as f:
        pickle.dump({'total_score': total_score, 'high_score': high_score}, f)

def load_score():
    if os.path.exists('score.dat'):
        with open('score.dat', 'rb') as f:
            data = pickle.load(f)
            if isinstance(data, dict):
                total_score = data.get('total_score', 0)
                high_score = data.get('high_score', 0)
            else:
                # Data is an int (from previous version), so use it as total_score
                total_score = data
                high_score = 0  # Set high_score to zero or any default value
            return total_score, high_score
    else:
        return 0, 0

def main():
    total_score, high_score = load_score()
    level = 1
    board = Board(level, total_score)
    clock = pygame.time.Clock()
    running = True
    show_level_menu = True  # To choose level or spend points
    level_decrease_message = ""

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(board.total_score, high_score)
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not board.game_over and not board.win and not show_level_menu:
                    mouse_pos = pygame.mouse.get_pos()
                    # Calculate which cell was clicked
                    x_margin = SIDEBAR_WIDTH + ((SCREEN_WIDTH - SIDEBAR_WIDTH - (CELL_SIZE + CELL_MARGIN) * BOARD_SIZE) // 2)
                    y_margin = 50  # Starting from 50 pixels down

                    for row in range(BOARD_SIZE):
                        for col in range(BOARD_SIZE):
                            cell_rect = pygame.Rect(
                                x_margin + col * (CELL_SIZE + CELL_MARGIN),
                                y_margin + row * (CELL_SIZE + CELL_MARGIN),
                                CELL_SIZE,
                                CELL_SIZE,
                            )
                            if cell_rect.collidepoint(mouse_pos):
                                if event.button == 1:  # Left click
                                    board.flip_cell(row, col)
                                elif event.button == 3:  # Right click
                                    board.toggle_mark(row, col)
                                break

            elif event.type == pygame.KEYDOWN:
                # Accept both Enter keys
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if show_level_menu:
                        show_level_menu = False
                        level_decrease_message = ""
                    elif board.win:
                        # Add current round score to total score
                        board.total_score += board.score
                        if board.total_score > high_score:
                            high_score = board.total_score
                        save_score(board.total_score, high_score)
                        level = board.level + 1
                        board = Board(level, board.total_score)
                        show_level_menu = True
                    elif board.game_over:
                        # Lose current round score
                        # Apply level decrease logic
                        new_level, decrease_message = calculate_level_decrease(level)
                        level_decrease_message = f"Your level has {decrease_message}."
                        level = new_level
                        if board.total_score > high_score:
                            high_score = board.total_score
                        save_score(board.total_score, high_score)
                        board = Board(level, board.total_score)
                        show_level_menu = True
                elif event.key == pygame.K_s and show_level_menu:
                    # Spend points to increase level
                    if board.total_score >= 100:
                        board.total_score -= 100
                        level += 1
                        board = Board(level, board.total_score)
                        save_score(board.total_score, high_score)
                elif event.key == pygame.K_r and show_level_menu:
                    # Reset total score
                    board.total_score = 0
                    save_score(board.total_score, high_score)

        # Draw everything
        screen.fill(WHITE)
        if show_level_menu:
            # Display level and options to spend points
            # Center x position for menu text (adjusted for sidebar)
            menu_center_x = SIDEBAR_WIDTH + ((SCREEN_WIDTH - SIDEBAR_WIDTH) // 2)

            # Semi-transparent background for menu
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(SEMI_TRANSPARENT_BG)
            screen.blit(overlay, (0, 0))

            menu_text = title_font.render(f"Current Level: {level}", True, BLACK)
            menu_rect = menu_text.get_rect(center=(menu_center_x, SCREEN_HEIGHT // 2 - 120))
            screen.blit(menu_text, menu_rect)

            points_text = title_font.render(f"Total Score: {board.total_score}", True, BLACK)
            points_rect = points_text.get_rect(center=(menu_center_x, SCREEN_HEIGHT // 2 - 80))
            screen.blit(points_text, points_rect)

            high_score_text = title_font.render(f"High Score: {high_score}", True, BLACK)
            high_score_rect = high_score_text.get_rect(center=(menu_center_x, SCREEN_HEIGHT // 2 - 40))
            screen.blit(high_score_text, high_score_rect)

            instructions = [
                "Press Enter to start the game",
                "Press 'S' to spend 100 points to increase level",
                "Press 'R' to reset total score",
                "Left-click to reveal a cell",
                "Right-click to mark/unmark a cell",
            ]

            for i, line in enumerate(instructions):
                instr_text = small_font.render(line, True, BLACK)
                instr_rect = instr_text.get_rect(center=(menu_center_x, SCREEN_HEIGHT // 2 + i * 30))
                screen.blit(instr_text, instr_rect)
        else:
            draw_board(screen, board, high_score, level_decrease_message)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
