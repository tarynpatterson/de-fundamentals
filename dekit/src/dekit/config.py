import os
import tomllib


class ConfigError(Exception):
    """Raised when config loading fails for any reason."""
    pass


def load_config(path: str, required_keys: list[str] | None = None, prefix: str = "DEKIT_") -> dict:
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {path}") from None
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"Invalid TOML in {path}: {e}") from None

    if required_keys:
        missing = [key for key in required_keys if key not in data]
        if missing:
            raise ConfigError(f"Missing required keys in {path}: {missing}")

    for env_var, value in os.environ.items():
        if not env_var.startswith(prefix):
            continue

        remainder = env_var[len(prefix):]
        parts = remainder.lower().split("_", 1)
        if len(parts) != 2:
            continue

        section, key = parts
        if section in data and isinstance(data[section], dict):
            data[section][key] = value

    return data