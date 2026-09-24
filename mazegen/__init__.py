"""
## Reusable Module

The `mazegen` package provides the reusable `MazeGenerator` class.
It can be installed and imported into another Python project
independently of the main A-Maze-ing application.

### Building the Package

The package can be rebuilt from the project sources using:
python3 -m build


This creates the package distributions in the `dist/` directory.

### Installation

Install the pre-built wheel located at the root of the repository:
pip install ./mazegen-1.0.0-py3-none-any.whl

Alternatively, after rebuilding the package from source,
install the newly created wheel:
pip install ./dist/mazegen-1.0.0-py3-none-any.whl

### Basic Usage

Import and instantiate the generator:
from mazegen.generator import MazeGenerator

Generate maze and solve it, write output to file from config.txt path:
generator = MazeGenerator(width = 15, height = 10, perfect = False, seed = 12)


The constructor accepts custom maze dimensions,
the maze mode, and an optional seed.
Using the same parameters and seed makes maze generation reproducible.

## Accessing the Generated Maze

generator.generate()

After calling `generate()`, the generated maze structure
is available through the `grid` attribute:
grid = generator.grid

The grid is represented as a two-dimensional list of integers.
Each integer uses a bitmask to represent the walls of one cell

## Accessing a Solution

The `solve()` method returns the shortest path
between the selected entry and exit coordinates:
solution = generator.solve(0, 0, 14, 9)

The returned solution is a string containing the directions
`N`, `E`, `S`, and `W`.

This allows another Python project to generate a maze,
access its internal grid representation,
and obtain a solution without using the main A-Maze-ing application.
"""
