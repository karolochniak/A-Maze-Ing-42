import sys

from config_parser import (
    parse_config,
    validate_config_dimensions,
    # parse_coordinates
)


def main() -> None:
    """Main function to run the maze generation."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        config = parse_config(config_file)
        validate_config_dimensions(config)
    except (ValueError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    # width = int(config["WIDTH"])
    # height = int(config["HEIGHT"])
    # entry = parse_coordinates(config["ENTRY"])
    # exit = parse_coordinates(config["EXIT"])
    # output_file = config["OUTPUT_FILE"]
    # perfect = config["PERFECT"].lower() == "true"


if __name__ == "__main__":
    main()
