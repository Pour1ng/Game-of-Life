"""SYST 230 HW1: Game of Life
Author: Joshua R. Obee
Purpose: This program follows the rules of "Conway's Game of Life".
"1. Any alive cell that is touching less than two alive neighbors dies.
2. Any alive cell touching four or more alive neighbors dies.
3. Any alive cell touching two or three alive neighbors does nothing.
4. Any dead cell touching exactly three alive neighbors becomes alive."
(Black space is alive; White space is dead)
"""

import turtle as t
from copy import deepcopy

CELL_SIZE = 50
NUM_ROWS, NUM_COLS = 10, 10
GENERATION = 0
SHAPE_COUNT = 0

def draw_grid(grid: list[list]):
    """Uses turtle to draw a 10x10 grid, with cell size 50
    Cells are colored or plain based on the cell state (i.e. alive or dead)
    given in the grid parameter (i.e. a nested list)"""
    global GENERATION, SHAPE_COUNT  
    t.clear()
    t.tracer(0)

    coords = (-250, 250), (250, 250), (250, -250), (-250, -250)
    t.pu()
    t.goto(coords[0])
    t.pd()

    for i in coords + (coords[0],):
        t.goto(i)

    x, y = coords[0][0], coords[0][1]
    
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if grid[row][col] == 1:  # Alive cell
                t.fillcolor("black")
            else:  # Dead cell
                t.fillcolor("white")

            t.pu()
            t.goto(x + col * CELL_SIZE, y - row * CELL_SIZE)  # Adjusted y-coordinate here
            t.pd()
            t.begin_fill()
            
            for _ in range(4):
                t.forward(CELL_SIZE)
                t.right(90)
            
            t.end_fill()

    t.pu()
    t.goto(0, 0)
    t.update()
    t.pu()

    t.goto(0, 300) # Goes to coordinates to type header
    t.pd()
    t.write(f"SHAPE={SHAPE_COUNT % 4 + 1}  GENERATIONS={GENERATION + 1}",
             align="center", font=("Arial", 20, "bold")) # Types header


def count_neighbors(r: int, c: int, grid: list[list]) -> int:
    """Given row and column indices (i.e. r and c) and the CA's state (i.e. grid)
    Returns a count of living neighbors of the cell referenced by the given
    indices in the grid i.e. cell at grid[r][c]
    NB: Boundary cells will have fewer than 8 neighbors"""
    count = 0
    for i in range(max(0, r - 1), min(NUM_ROWS, r + 2)):
        for j in range(max(0, c - 1), min(NUM_COLS, c + 2)):
            if not (i == r and j == c) and grid[i][j] == 1:
                count += 1
    return count

def apply_rules(grid: list[list]) -> list:
    """Given the current state of the CA (i.e. grid) applies
    the rules of the Game of life to each cell in the grid,
    by invoking the count_neighbors function and returns a
    new grid with state values for the next generation
    HINT: Copy grid into a new_grid (USE deepcopy from the copy module),
    make changes to new_grid based on the old grid and return new_grid"""
    global SHAPE_COUNT, GENERATION
    new_grid = deepcopy(grid)
    
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            neighbors = count_neighbors(row, col, grid)
            
            if grid[row][col] == 1:  # Alive cell
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0  # Cell dies
            else:  # Dead cell
                if neighbors == 3:
                    new_grid[row][col] = 1  # Cell becomes alive

    if grid != new_grid:
        SHAPE_COUNT += 1 # Increment SHAPE_COUNT count
    GENERATION += 1  # Increment GENERATION count
    return new_grid

def add_pattern(grid: list[list], *living: tuple[int, int]):
    """Given the state of the CA, (i.e. grid) and a list of
    coordinates specifying indices for living cells set cells in grid
    referenced by indices to alive"""
    for cell in living:
        row, col = cell
        grid[row][col] = 1

def main():
    """Program execution start point:
    Initialize 10x10 CA grid with zeros i.e. all dead
    Invoke add_pattern function passing grid, and living cell indices
    Example: Assuming the bottom left cell is referenced by (0, 0) then
    for Glider pattern living indices -> (7, 1), (6, 2), (6, 3), (7, 3), (8, 3)
    Iteratively:
    Invoke draw_grid passing grid
    Invoke apply_rules passing current grid and store return value in the grid variable"""
    
    grid = [[0] * NUM_COLS for _ in range(NUM_ROWS)]

    # Add Glider pattern
    add_pattern(grid, (-8, 1), (-7, 2), (-7, 3), (-8, 3), (-9, 3))

    # Display 5 generations
    for generation in range(5):
        t.hideturtle()
        draw_grid(grid)
        user_input = t.textinput("Continue?", "Type 'advance' or 'a' to proceed to the next generation:")

        # Start the event loop based on user input
        while user_input.lower() not in ["advance", "a"]:
            user_input = t.textinput("Continue?", "Unknown input. Please type 'advance' or 'a' to proceed.")
        grid = apply_rules(grid)
        
        t.update()

if __name__ == '__main__':
    t.title("Conway's Game of Life: Glider")
    main()
    t.mainloop()
    t.exitonclick()
