import random
from collections import deque
from typing import List, Tuple


class MazeGenerator:
    """Class that generates and manages the maze structure."""

    def __init__(self, width: int, height: int, perfect: bool = False) -> None:
        """Initializes the maze object with the given dimensions.

        Args:
            width (int): Width of the maze (number of cells).
            height (int): Height of the maze (number of cells).
            perfect (bool, optional): Flag indicating whether the maze should
                be perfect. Defaults to False (Pac-Man mode).
        """
        self.width = width
        self.height = height
        self.perfect = perfect
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.reserved_cells: set[Tuple[int, int]] = set()

    def _carve_passages(self, start_x: int, start_y: int) -> None:
        """Carves paths in the maze using the DFS algorithm.

        Args:
            start_x (int): X coordinate of the starting point.
            start_y (int): Y coordinate of the starting point.
        """
        directions = {
            'N': (0, -1, 1, 4),
            'S': (0, 1, 4, 1),
            'E': (1, 0, 2, 8),
            'W': (-1, 0, 8, 2)
        }

        stack: List[Tuple[int, int]] = [(start_x, start_y)]
        visited = set()
        visited.add((start_x, start_y))

        while stack:
            cx, cy = stack[-1]
            unvisited_neighbors = []

            for dir_nam, (dx, dy, wall_here, wall_there) in directions.items():
                nx, ny = cx + dx, cy + dy
                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and (nx, ny) not in visited
                    and (nx, ny) not in self.reserved_cells
                ):
                    unvisited_neighbors.append((nx, ny, wall_here, wall_there))

            if unvisited_neighbors:
                nx, ny, wall_here, wall_there = random.choice(
                    unvisited_neighbors
                )
                self.grid[cy][cx] &= ~wall_here
                self.grid[ny][nx] &= ~wall_there
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def generate(self) -> None:
        """Main function that starts the generation process.

        Sequentially: adds the '42' pattern, carves corridors using the
        DFS algorithm, and finally removes dead ends if the maze is
        not perfect.
        """
        self._add_pattern_42()
        self._carve_passages(0, 0)

        if not self.perfect:
            self._make_playable()

    def display_debug(self) -> None:
        """Prints the generated grid in hexadecimal format."""
        for row in self.grid:
            print("".join(f"{c:x}" for r_cell in row for c in [r_cell]))

    def save_to_file(
        self,
        filename: str,
        entry_x: int,
        entry_y: int,
        exit_x: int,
        exit_y: int,
        path: str
    ) -> None:
        """Saves the maze to a file according to the project requirements.

        Args:
            filename (str): Path to the output file.
            entry_x (int): Entry X coordinate.
            entry_y (int): Entry Y coordinate.
            exit_x (int): Exit X coordinate.
            exit_y (int): Exit Y coordinate.
            path (str): Shortest path to the exit as a string of letters.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for row in self.grid:
                    f.write("".join(f"{cell:x}" for cell in row) + "\n")
                f.write("\n")
                f.write(f"{entry_x},{entry_y}\n")
                f.write(f"{exit_x},{exit_y}\n")
                f.write(f"{path}\n")
        except IOError as error:
            print(f"Error saving to file {filename}: {error}")

    def solve(self, start_x: int, start_y: int, exit_x: int, exit_y: int
              ) -> str:
        """Finds the shortest path from entry to exit (BFS).

        Args:
            start_x (int): Entry X coordinate.
            start_y (int): Entry Y coordinate.
            exit_x (int): Exit X coordinate.
            exit_y (int): Exit Y coordinate.

        Returns:
            str: A string of characters representing the path (N, E, S, W).
                Returns an empty string if the exit is unreachable.
        """
        directions = {
            'N': (0, -1, 1),
            'E': (1, 0, 2),
            'S': (0, 1, 4),
            'W': (-1, 0, 8)
        }

        queue = deque([(start_x, start_y, "")])
        visited = set()
        visited.add((start_x, start_y))

        while queue:
            cx, cy, path = queue.popleft()

            if cx == exit_x and cy == exit_y:
                return path

            cell_walls = self.grid[cy][cx]

            for dir_letter, (dx, dy, wall_bit) in directions.items():
                if (cell_walls & wall_bit) == 0:
                    nx, ny = cx + dx, cy + dy

                    if (
                        0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in visited
                    ):
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + dir_letter))

        return ""

    def _add_pattern_42(self) -> None:
        """Adds the protected '42' pattern in the center of the maze.

        Reserves the appropriate cells from the carving algorithm. If
        the maze is too small, it prints a warning and skips drawing.
        """
        if self.width < 11 or self.height < 9:
            print(
                "Warning: Maze is too small to generate the '42' pattern."
            )
            return

        ox = self.width // 2 - 3
        oy = self.height // 2 - 2

        digit_4 = [
            (0, 0), (2, 0),
            (0, 1), (2, 1),
            (0, 2), (1, 2), (2, 2),
            (2, 3),
            (2, 4)
        ]

        digit_2 = [
            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4)
        ]

        for dx, dy in digit_4 + digit_2:
            self.reserved_cells.add((ox + dx, oy + dy))

    def _make_playable(self) -> None:
        """Converts a perfect maze into a Pac-Man style board.

        Finds all dead ends on the map and tears down one of the walls
        in each of them towards a free corridor, creating loops.
        """
        directio = {
            'N': (0, -1, 1, 4),
            'S': (0, 1, 4, 1),
            'E': (1, 0, 2, 8),
            'W': (-1, 0, 8, 2)
        }

        dead_ends = {7, 11, 13, 14}

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.reserved_cells:
                    continue

                if self.grid[y][x] in dead_ends:
                    possible_walls = []

                    for d_name, (dx, dy, w_here, w_there) in directio.items():
                        if self.grid[y][x] & w_here:
                            nx, ny = x + dx, y + dy

                            if (
                                0 <= nx < self.width
                                and 0 <= ny < self.height
                                and (nx, ny) not in self.reserved_cells
                            ):
                                possible_walls.append(
                                    (nx, ny, w_here, w_there)
                                )

                    if possible_walls:
                        nx, ny, w_here, w_there = random.choice(possible_walls)
                        self.grid[y][x] &= ~w_here
                        self.grid[ny][nx] &= ~w_there
