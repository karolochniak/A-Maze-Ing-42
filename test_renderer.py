from renderer import Renderer

maze = [
    [15, 15, 15, 15, 15],
    [9,  7,  3,  0, 11],
    [9,  3,  4,  2, 11],
    [13, 12,  0,  6,  7],
    [15, 15, 15, 15, 15],
]

entry = (2, 1)
exit = (1, 3)
path = [(2, 1), (2, 2), (3, 2), (3, 3), (2, 3)]
show_path = True
renderer = Renderer()
allowed_colors = [
    "red",
    "pink",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white"
]

while True:
    print("\033[H\033[J", end="")
    renderer.display(maze, entry, exit, path, show_path)
    choice = input("P - show/hide path, Q - quit, C - change color: ").lower()
    if choice == "p":
        show_path = not show_path
    elif choice == "q":
        break
    elif choice == "c":
        while True:
            new_color = input("Enter new wall color: ").lower()
            if new_color in allowed_colors:
                renderer.wall_color = new_color
                break
            else:
                print("Invalid color. Please choose from the allowed colors.")
    # elif choice == "r":
    else:
        print("Invalid choice. Please try again.")
