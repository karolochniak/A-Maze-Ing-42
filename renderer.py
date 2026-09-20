NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class Renderer:
    """Render a maze in the terminal using ASCII characters."""

    def __init__(self) -> None:
        """Initialize the Renderer with a default wall color."""
        self.wall_color = "white"

    def display(self, maze: list[list[int]], entry: tuple[int, int],
                exit: tuple[int, int], path: list[tuple[int, int]],
                show_path: bool) -> None:
        """Display the complete maze in the terminal.

        Args:
            maze: Two-dimensional list containing the encoded maze cells.
            entry: Coordinates of the maze entry.
            exit: Coordinates of the maze exit.
            path: Coordinates forming the solution path.
            show_path: Whether the solution path should be displayed.
        """
        for y, row in enumerate(maze):
            top, middle, bottom = self.draw_row(row, y, entry, exit, path,
                                                show_path)
            if y == 0:
                print(top)
                print(middle)
                print(bottom)
            else:
                print(middle)
                print(bottom)

    def has_wall(self, cell: int, direction: int) -> bool:
        """Check whether a cell has a wall in the given direction.

        Args:
            cell: Encoded value representing the walls of a cell.
            direction: Bit value representing the direction to check.

        Returns:
            True if the wall exists, otherwise False.
        """
        return bool(cell & direction)

    def draw_cell(self, cell: int, x: int, y: int, entry: tuple[int, int],
                  exit: tuple[int, int],
                  path: list[tuple[int, int]],
                  show_path: bool) -> tuple[str, str, str]:
        """Create the ASCII representation of a single maze cell.

        Args:
            cell: Encoded value representing the walls of the cell.
            x: Horizontal coordinate of the cell.
            y: Vertical coordinate of the cell.
            entry: Coordinates of the maze entry.
            exit: Coordinates of the maze exit.
            path: Coordinates forming the solution path.
            show_path: Whether the solution path should be displayed.

        Returns:
            The top, middle, and bottom ASCII parts of the cell.
        """
        if (x, y) == entry:
            filling = " S "
        elif (x, y) == exit:
            filling = " E "
        elif show_path and (x, y) in path:
            filling = " * "
        else:
            filling = "   "
        if self.has_wall(cell, NORTH):
            top = "+---+"
        else:
            top = "+   +"
        if self.has_wall(cell, WEST):
            middle = "|" + filling
        else:
            middle = " " + filling
        if self.has_wall(cell, EAST):
            middle += "|"
        else:
            middle += " "
        if self.has_wall(cell, SOUTH):
            bottom = "+---+"
        else:
            bottom = "+   +"

        return top, middle, bottom

    def draw_row(self, row: list[int], y: int, entry: tuple[int, int],
                 exit: tuple[int, int],
                 path: list[tuple[int, int]],
                 show_path: bool) -> tuple[str, str, str]:
        """Create the ASCII representation of one maze row.

        Args:
            row: List of encoded maze cells in the row.
            y: Vertical coordinate of the row.
            entry: Coordinates of the maze entry.
            exit: Coordinates of the maze exit.
            path: Coordinates forming the solution path.
            show_path: Whether the solution path should be displayed.

        Returns:
            The top, middle, and bottom ASCII parts of the row.
        """
        full_top = ""
        full_middle = ""
        full_bottom = ""
        for x, cell in enumerate(row):
            top, middle, bottom = self.draw_cell(cell, x, y, entry, exit, path,
                                                 show_path)
            if x == 0:
                full_top += top
                full_middle += middle
                full_bottom += bottom
            else:
                full_top += top[1:]
                full_middle += middle[1:]
                full_bottom += bottom[1:]

        full_top = self.color_text(full_top, self.wall_color)
        full_middle = self.color_middle_part(full_middle)
        full_bottom = self.color_text(full_bottom, self.wall_color)

        return full_top, full_middle, full_bottom

    def color_text(self, text: str, color: str) -> str:
        """Apply an ANSI color code to text.

        Args:
            text: Text to color.
            color: Name of the color to apply.

        Returns:
            The text wrapped in ANSI color codes.
        """
        color_codes = {
            "red": "\033[91m",
            "pink": "\033[95m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m"
        }
        return f"{color_codes.get(color, '')}{text}{color_codes['reset']}"

    def color_middle_part(self, text: str) -> str:
        """Apply the wall color to vertical wall characters.

        Args:
            text: Text containing the vertical maze walls.

        Returns:
            Text with ANSI color codes applied to vertical walls.
        """
        result = ""
        for char in text:
            if char == "|":
                result += self.color_text(char, self.wall_color)
            else:
                result += char
        return result
