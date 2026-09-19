def parse_config(filename: str) -> dict[str, str]:
    """Read and validate the structure of a maze configuration file.

    Args:
        filename: Path to the configuration file.

    Returns:
        A dictionary containing configuration keys and values.

    Raises:
        ValueError: If the configuration format is invalid.
        OSError: If the file cannot be opened or read.
    """
    config = {}

    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    }
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if line == "":
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Invalid line in config file: {line}")

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key == "" or value == "":
                raise ValueError(f"Invalid line in config file: {line}")

            if key in config:
                raise ValueError(f"Duplicate key in config file: {key}")

            config[key] = value

    missing_keys = required_keys - config.keys()
    if missing_keys:
        raise ValueError(f"Missing required keys {missing_keys}")
    return config


def validate_config_dimensions(config: dict[str, str]) -> bool:
    """Validate maze configuration values.

    Args:
        config: Dictionary containing the maze configuration.

    Raises:
        ValueError: If any configuration value is invalid.
    """
    work = False
    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        entry = parse_coordinates(config["ENTRY"])
        exit = parse_coordinates(config["EXIT"])
        perfect = config["PERFECT"].lower()
        work = True
    except ValueError as e:
        raise ValueError(f"Invalid value in config file: {e}")

    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive integers")
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ValueError("ENTRY coordinates are out of bounds")
    if not (0 <= exit[0] < width and 0 <= exit[1] < height):
        raise ValueError("EXIT coordinates are out of bounds")
    if entry == exit:
        raise ValueError("ENTRY and EXIT coordinates cannot be the same")
    if perfect not in {"true", "false"}:
        raise ValueError("PERFECT must be 'true' or 'false'")
    return work


def parse_coordinates(value: str) -> tuple[int, int]:
    """Convert a coordinate string into a tuple of integers.

    Args:
        value: Coordinates in the "x,y" format.

    Returns:
        A tuple containing the x and y coordinates.

    Raises:
        ValueError: If the coordinate format is invalid.
    """
    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate format: {value}")
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        raise ValueError(f"Coordinates must be integers: {value}")

    return (x, y)
