"""Main script for the A-Maze-ing project."""
import sys
from typing import Dict, List, Tuple
from mazegen.generator import MazeGenerator
from mazegen.renderer import Renderer
from config_parser import (
    parse_config,
    validate_config_dimensions,
)

def convert_path_to_coords(
    start_x: int,
    start_y: int,
    path_str: str
) -> List[Tuple[int, int]]:
    """Convert a string of letters (N, E, S, W) to a list of coordinates."""
    coords = [(start_x, start_y)]
    cx, cy = start_x, start_y
    moves = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}

    for move in path_str:
        if move in moves:
            dx, dy = moves[move]
            cx, cy = cx + dx, cy + dy
            coords.append((cx, cy))
    return coords


def main() -> None:
    """Parse arguments, initialize tools, and run the interactive loop."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    try:
        config = parse_config(sys.argv[1])
        validate_config_dimensions(config)
        width = int(config.get('WIDTH', 10))
        height = int(config.get('HEIGHT', 10))
        perfect = config.get('PERFECT', 'False').strip().lower() == 'true'

        entry_x, entry_y = map(int, config.get('ENTRY', '0,0').split(','))
        exit_x, exit_y = map(
            int, config.get('EXIT', f'{width-1},{height-1}').split(',')
        )
        output_file = config.get('OUTPUT_FILE', 'maze.txt')
    except (ValueError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    renderer = Renderer()
    colors = [
        "white", "red", "green", "blue", "yellow", "cyan", "magenta"
    ]
    color_idx = 0
    show_path = False

    generator = MazeGenerator(width, height, perfect)
    generator.generate()
    path_str = generator.solve(entry_x, entry_y, exit_x, exit_y)
    path_coords = convert_path_to_coords(entry_x, entry_y, path_str)

    generator.save_to_file(
        output_file, entry_x, entry_y, exit_x, exit_y, path_str
    )

    while True:
        print("\n" * 2)
        renderer.display(
            generator.grid,
            (entry_x, entry_y),
            (exit_x, exit_y),
            path_coords,
            show_path
        )

        print("\n=== A-Maze-ing ===")
        print("1. Generate new maze")
        print("2. Show/Hide shortest path")
        print("3. Change wall color")
        print("4. Quit")

        choice = input("Choice? (1-4): ").strip()

        if choice == '1':
            generator = MazeGenerator(width, height, perfect)
            generator.generate()
            path_str = generator.solve(entry_x, entry_y, exit_x, exit_y)
            path_coords = convert_path_to_coords(entry_x, entry_y, path_str)
            generator.save_to_file(
                output_file, entry_x, entry_y, exit_x, exit_y, path_str
            )
        elif choice == '2':
            show_path = not show_path
        elif choice == '3':
            color_idx = (color_idx + 1) % len(colors)
            renderer.wall_color = colors[color_idx]
        elif choice == '4':
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()