import pygame
import random

# Initialize PyGame
pygame.init()

# Constants
SCREEN_INFO = pygame.display.Info()
WINDOW_SIZE = int(SCREEN_INFO.current_h * 0.7)  # Set a base window size (can be adjusted)
FPS = 10

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)

# Initialize screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
pygame.display.set_caption('Conway\'s Game of Life')


# Initial grid size prompt
def draw_initial_menu(surface, input_box):
    menu_width = WINDOW_SIZE * 0.5
    menu_height = WINDOW_SIZE * 0.1
    menu_x = (WINDOW_SIZE - menu_width) // 2
    menu_y = (WINDOW_SIZE - menu_height) // 2
    pygame.draw.rect(surface, LIGHT_GRAY, (menu_x, menu_y, menu_width, menu_height))

    font_size = int(WINDOW_SIZE * 0.04)
    font = pygame.font.Font(None, font_size)
    label = "Enter Grid Size:"
    text = font.render(label, True, BLACK)
    surface.blit(text, (menu_x + (menu_width * 0.1), menu_y + (menu_height * 0.4)))
    input_box.update_position(menu_x + (menu_width * 0.6), menu_y + (menu_height * 0.3), menu_width * 0.3,
                              menu_height * 0.45)
    input_box.draw(surface, font_size)

    # Draw "Press ENTER" message at the bottom center
    bottom_message = "Press ENTER"
    bottom_font_size = int(WINDOW_SIZE * 0.03)
    bottom_font = pygame.font.Font(None, bottom_font_size)
    bottom_text = bottom_font.render(bottom_message, True, YELLOW)
    bottom_text_rect = bottom_text.get_rect(center=(WINDOW_SIZE // 2, menu_y + menu_height + bottom_font_size))
    surface.blit(bottom_text, bottom_text_rect)


# InputBox class for text input
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = pygame.font.Font(None, 36).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = YELLOW if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = pygame.font.Font(None, 36).render(self.text, True, self.color)

    def draw(self, screen, font_size):
        self.txt_surface = pygame.font.Font(None, font_size).render(self.text, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update_position(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def get_text(self):
        return self.text


# Function to draw the grid
def draw_grid(surface, grid, cell_size):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            color = GRAY if grid[row][col] == 1 else BLACK
            pygame.draw.rect(surface, color, (col * cell_size, row * cell_size, cell_size, cell_size))


# Function to update the grid based on the rules
def update_grid(grid, rules):
    new_grid = [[0 for _ in range(len(grid))] for _ in range(len(grid))]
    survive_conditions = [int(n) for n in rules["survive"].split()]
    reproduce_conditions = [int(n) for n in rules["reproduce"].split()]

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            live_neighbors = sum(
                grid[(row + i) % len(grid)][(col + j) % len(grid[row])]  # neighboring cell values are taken from the previous frame
                for i in [-1, 0, 1]
                for j in [-1, 0, 1]
                if not (i == 0 and j == 0)
            )
            if grid[row][col] == 1:
                if live_neighbors in survive_conditions:
                    new_grid[row][col] = 1
            else:
                if live_neighbors in reproduce_conditions:
                    new_grid[row][col] = 1
    return new_grid


# Function to draw the pause menu
def draw_pause_menu(surface, input_box):
    menu_width = WINDOW_SIZE * 0.5
    menu_height = WINDOW_SIZE * 0.25
    menu_x = (WINDOW_SIZE - menu_width) // 2
    menu_y = (WINDOW_SIZE - menu_height) // 2
    pygame.draw.rect(surface, LIGHT_GRAY, (menu_x, menu_y, menu_width, menu_height))

    font_size = int(WINDOW_SIZE * 0.035)
    font = pygame.font.Font(None, font_size)
    label = "Enter Rules (reproduce / survive):"
    text = font.render(label, True, BLACK)
    surface.blit(text, (menu_x + (menu_width * 0.1), menu_y + (menu_height * 0.2)))

    input_box.update_position(menu_x + (menu_width * 0.1), menu_y + (menu_height * 0.5), menu_width * 0.8,
                              menu_height * 0.25)
    input_box.draw(surface, font_size)


# Function to draw the message
def draw_message(surface, message):
    font_size = int(WINDOW_SIZE * 0.04)
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, YELLOW)
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, font_size // 2 + 10))
    surface.blit(text, text_rect)


def draw_bottom_message(surface, message):
    font_size = int(WINDOW_SIZE * 0.025)  # Smaller font size
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, YELLOW)
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE - font_size // 2 - 10))
    surface.blit(text, text_rect)


# Main game loop
running = True
paused = False
clock = pygame.time.Clock()

# Input box for initial grid size
initial_input_box = InputBox(WINDOW_SIZE * 0.55, WINDOW_SIZE * 0.375, WINDOW_SIZE * 0.15, WINDOW_SIZE * 0.05)
initial_grid_size_entered = False

while not initial_grid_size_entered:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            initial_grid_size_entered = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            grid_size_text = initial_input_box.get_text()
            if grid_size_text.isdigit():
                grid_size = int(grid_size_text)
                CELL_SIZE = WINDOW_SIZE // grid_size
                initial_grid_size_entered = True
        initial_input_box.handle_event(event)
        if event.type == pygame.VIDEORESIZE:
            WINDOW_SIZE = min(event.w, event.h)  # Maintain a square window
            screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
            initial_input_box.update_position(WINDOW_SIZE * 0.55, WINDOW_SIZE * 0.375, WINDOW_SIZE * 0.15,
                                              WINDOW_SIZE * 0.05)

    screen.fill(GRAY)
    draw_initial_menu(screen, initial_input_box)
    pygame.display.flip()
    clock.tick(FPS)

# Create a 2D grid
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Randomize initial grid
for i in range(grid_size):
    for j in range(grid_size):
        grid[i][j] = random.choices([0, 1], weights=[80, 20])[0]  # 20% chance for the cell to be initially alive

# Game rules (can be changed by user during runtime)
rules = {
    "survive": "2 3",
    "reproduce": "3"
}

# Initialize input box with existing rules
rules_input_box = InputBox(WINDOW_SIZE * 0.1, WINDOW_SIZE * 0.5, WINDOW_SIZE * 0.8, WINDOW_SIZE * 0.1,
                           f"{rules['reproduce']} / {rules['survive']}")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                paused = not paused
                if not paused:
                    # Update rules from input box when unpausing
                    rules_text = rules_input_box.get_text()
                    if ' / ' in rules_text:
                        reproduce_rules, survive_rules = rules_text.split(' / ')
                        rules["reproduce"] = reproduce_rules.strip()
                        rules["survive"] = survive_rules.strip()
        if paused:
            rules_input_box.handle_event(event)
        if event.type == pygame.VIDEORESIZE:
            WINDOW_SIZE = min(event.w, event.h)  # Maintain a square window
            screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
            CELL_SIZE = int(WINDOW_SIZE / grid_size)
            rules_input_box.update_position(WINDOW_SIZE * 0.1, WINDOW_SIZE * 0.5, WINDOW_SIZE * 0.8, WINDOW_SIZE * 0.1)

    if not paused:
        grid = update_grid(grid, rules)

    screen.fill(GRAY)
    draw_grid(screen, grid, CELL_SIZE)
    if not paused:
        draw_message(screen, "Press TAB to pause and change rules")
        draw_bottom_message(screen, "All the windows of the program are resizable")
    else:
        draw_pause_menu(screen, rules_input_box)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
