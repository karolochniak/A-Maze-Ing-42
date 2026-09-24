*This project has been created as part of the 42 curriculum by kochniak, jwira.*



# A_Maze_Ing
## Description
A-Maze-ing is a terminal-based maze generator and solver written in Python 3.10. The program reads a configuration file to set up maze parameters, generates a maze using Depth-First Search (DFS), embeds a visual pattern (default: "42") in the center of the maze, solves it using Breadth-First Search (BFS), and renders it in the terminal with ANSI colors and block characters.

The project also provides a reusable Python package, mazegen, which exposes the MazeGenerator class for use in any Python project.

Key features:

- Maze generation with DFS "recursive backtracker"
- Embedded text pattern in the maze center (default "42")
- BFS pathfinding to find the shortest solution
- Perfect and non-perfect maze modes (a single-path maze or a more open, Pac-Man-like board)
- Reproducible mazes via seed
- Interactive menu to regenerate, change colors and shows or hide the shortest path.
- Reusable mazegen package installable via pip
## Instructions
### Requirements
- Python 3.10 or newer
- pip
- flake8
- mypy
### Setup and Run 
```bash
# Step 1 — Install the development dependencies:
make install

# Step 2 — Run the program using default configuration file:
make run
```
### Other Commands

```bash
make debug        # Run the program in debug mode with pdb
make lint         # Run flake8 and mypy checks
make clean        # Remove __pycache__ and .mypy_cache
```
### Configuration File

The program requires a configuration file as its only argument:
```bash
python3 a_maze_ing.py config.txt
```
**Config file format** (key=value)
```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42

Lines beggining with # are treated as comments.
```
| Key         | Type    | Required | Description                                      |
|-------------|---------|----------|--------------------------------------------------|
| WIDTH       | int     | Yes      | Number of columns in the maze (> 0)             |
| HEIGHT      | int     | Yes      | Number of rows in the maze (> 0)                |
| ENTRY       | x,y     | Yes      | Entry cell coordinates                          |
| EXIT        | x,y     | Yes      | Exit cell coordinates                           |
| OUTPUT_FILE | string  | Yes      | Path to the output file                         |
| PERFECT     | bool    | Yes      | True = no loops, False = non-perfect maze         |
| SEED        | int     | No       | Random seed for reproducibility                 |


## Maze Generation Algorithm
### Depth-First Search (DFS) — Recursive Backtracker
The DFS algorithm works as follows:
- Step 1. Start from a random unmasked, non-hollow cell
- Step 2. Mark it as visited and push it to a stack
- Step 3. Randomly pick an unvisited neighbor, break the wall, and move to it
- Step 4. If no unvisited neighbors exist, backtrack by popping the stack
- Step 5. Repeat until the stack is empty

**Why DFS?**
- Produces long, winding corridors — visually interesting and challenging mazes
- Simple to implement iteratively with a stack
- Guarantees all reachable cells are visited

## Maze Solving Algorithm

### Breadth-First Search (BFS)
The BFS alorithm works as follows:
- Step 1: Start from the entry cell, mark it as visited, add it to the queue, set its parent (previous cell in the path) to be None.
- Step 2: Add unvisited neighbours that are open to the current cell to the queue and set their parents to the current cell.
- Step 3: Remove the current cell from the queue and set the next one as the current cell.
- Step 4: Repeat Step 2 - 3 until the exit cell is found
- Step 5: Reconstruction the sulution from the exit cell using the stored parent information.

**Why BFS?**
- Guarantees one the shortest path from start point to exit point
- Only needs to travel the graph one to find the shortest path.
- It is time-efficient and easy to implement





## Reusable Module

The `mazegen` package provides the reusable `MazeGenerator` class. It can be installed and imported into another Python project independently of the main A-Maze-ing application.

### Building the Package

The package can be rebuilt from the project sources using:
```bash
python3 -m build
```

This creates the package distributions in the `dist/` directory.

### Installation

Install the pre-built wheel located at the root of the repository:
```bash
pip install ./mazegen-1.0.0-py3-none-any.whl
```
Alternatively, after rebuilding the package from source, install the newly created wheel:

```bash
pip install ./dist/mazegen-1.0.0-py3-none-any.whl
```

### Basic Usage

Import and instantiate the generator:

```python
from mazegen.generator import MazeGenerator

# Generate maze and solve it, write output to file from config.txt path
generator = MazeGenerator(width = 15, height = 10, perfect = False, seed = 12)
```

The constructor accepts custom maze dimensions, the maze mode, and an optional seed. Using the same parameters and seed makes maze generation reproducible.

## Accessing the Generated Maze

```python
generator.generate()
```

After calling `generate()`, the generated maze structure is available through the `grid` attribute:

```python
grid = generator.grid
```
The grid is represented as a two-dimensional list of integers. Each integer uses a bitmask to represent the walls of one cell

## Accessing a Solution

The `solve()` method returns the shortest path between the selected entry and exit coordinates:

```python
solution = generator.solve(0, 0, 14, 9)
```

The returned solution is a string containing the directions
`N`, `E`, `S`, and `W`.

This allows another Python project to generate a maze, access its internal grid representation, and obtain a solution without using the main A-Maze-ing application.

## Grid Format

`generator.grid` is a 2D list of integers where each cell encodes its walls as a 4-bit bitmask:

| Bit | Value | Wall  |
|-----|-------|-------|
| 0   | 1     | North |
| 1   | 2     | East  |
| 2   | 4     | South |
| 3   | 8     | West  |

A cell with value `15` (all bits set) has all four walls intact. A cell with value `0` has no walls.

## Team and Project Management

### Team Members

| Member       | Role                                                                 |
|--------------|----------------------------------------------------------------------|
| kochniak     | Maze generation algorithms (DFS), BFS pathfinding, pattern "42 "embedding, hollow cells |
| jwira  | Terminal renderer, animation system, config parser, interactive menu, project packaging, package structure|

### Planning

**Initial plan:**
- Month 1: Discuss the project requirements, identify our strengths and weaknesses, understand the project structure, and divide the implementation tasks between the two team members.
- Month 2: Implementing the DFS and BFS algorithm, the visual representation of generated maze, packaging,and README file.

**How it evolved:**
The DFS algorithm took longer than expected. Animation and the interactive menu also required several iterations to fix edge cases (nested loops, grid sync issues). Packaging was added at the end and required refactoring imports and restructuring the codebase.

### What Worked Well

- The bitmask grid representation made wall operations clean and efficient
- The callback system for animation kept DFS decoupled from the renderer
- Using `seed` made debugging reproducible — we could replay exact mazes
- Separating `MazeGenerator` from `Renderer` made the generator reusable as a package.

### What Could Be Improved
- Visual implementations could be more redable and made by graphical library such as MLX
- Using instead DFS (Kruskal's or Wilson's) algorithms

### Tools Used

- **Python 3.10** — main language
- **flake8** — code style linting
- **mypy** — static type checking
- **setuptools + build** — package building
- **pdb** — debugging
---

## Resources

- [Recursive backtracker (DFS) — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [BFS pathfinding — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)

### AI Usage

Gemini was used as a development assistant throughout this project.
Specifically for:
- Helping to understand concepts
- Assisting with architectural decisions
- Improving the overall structure of the code
- Hepling with project packaging