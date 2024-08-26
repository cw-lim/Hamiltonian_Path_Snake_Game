import pygame
import random
from moviepy.editor import ImageSequenceClip
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 10  # Grid size to match the path_grid dimensions
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hamiltonian Path Snake Game')

# Convert the path grid to a list of coordinates
def convert_path_to_coordinates(path_grid):
    value_to_coord = {}
    coordinates = []
    for row in range(len(path_grid)):
        for col in range(len(path_grid[row])):
            value_to_coord[path_grid[row][col]] = (row, col)
    # Create path list based on ordered values from the path grid
    ordered_values = sorted(value_to_coord.keys())
    for value in ordered_values:
        coordinates.append(value_to_coord[value])
    return coordinates

# Define the Hamiltonian path grid
path_grid = [
    [1, 2, 3, 4, 29, 30, 55, 56, 57, 58],
    [100, 99, 6, 5, 28, 31, 54, 53, 60, 59],
    [97, 98, 7, 8, 27, 32, 51, 52, 61, 62],
    [96, 95, 10, 9, 26, 33, 50, 49, 64, 63],
    [93, 94, 11, 12, 25, 34, 47, 48, 65, 66],
    [92, 91, 14, 13, 24, 35, 46, 45, 68, 67],
    [89, 90, 15, 16, 23, 36, 43, 44, 69, 70],
    [88, 87, 18, 17, 22, 37, 42, 41, 72, 71],
    [85, 86, 19, 20, 21, 38, 39, 40, 73, 74],
    [84, 83, 82, 81, 80, 79, 78, 77, 76, 75]
]

# Convert path grid to coordinates
path_coordinates = convert_path_to_coordinates(path_grid)
cycle_length = len(path_coordinates)

# Initialize the snake
snake_pos = 0
snake_body = [path_coordinates[snake_pos]]
snake_direction = (1, 0)  # Initially moving right

# Place food
def place_food():
    global food_pos
    possible_positions = [pos for pos in path_coordinates if pos not in snake_body]
    if possible_positions:
        food_pos = random.choice(possible_positions)
    else:
        food_pos = path_coordinates[0]

place_food()

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_snake():
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_food():
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[1] * CELL_SIZE, food_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def move_snake():
    global snake_pos, snake_body, food_pos

    # Move the snake
    snake_pos = (snake_pos + 1) % cycle_length
    new_head = path_coordinates[snake_pos]

    # Debugging: Print snake head and body
    print(f"New head: {new_head}")
    print(f"Snake body: {snake_body}")

    # Check if snake has collided with itself
    if new_head in snake_body:
        return False

    snake_body.insert(0, new_head)

    # Check if snake has eaten the food
    if new_head == food_pos:
        place_food()  # Place new food
    else:
        snake_body.pop()

    return True

def capture_frame():
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    # Transpose dimensions for moviepy
    return np.transpose(frame, (1, 0, 2))

def main():
    clock = pygame.time.Clock()
    running = True
    frames = []

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_snake()
        draw_food()
        pygame.display.flip()

        # Capture the frame
        frames.append(capture_frame())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not move_snake():
            print("Game Over!")
            running = False

        clock.tick(30)  # Adjust speed for smoother gameplay

    # Save the frames as a video
    try:
        clip = ImageSequenceClip(frames, fps=10)
        clip.write_videofile("snake_game.mp4", codec="libx264")
        clip.close()  # Ensure the video file is finalized
    except Exception as e:
        print(f"An error occurred while saving the video: {e}")

    pygame.quit()
    sys.exit()  # Ensure clean exit

if __name__ == "__main__":
    main()