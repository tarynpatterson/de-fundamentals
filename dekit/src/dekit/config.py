import logging
import os
import tomllib

logger = logging.getLogger(__name__)

SENSITIVE_MARKERS = ("password", "secret", "token")


class ConfigError(Exception):
    """Raised when config loading fails for any reason."""


def _is_sensitive(key: str) -> bool:
    return any(marker in key.lower() for marker in SENSITIVE_MARKERS)


def load_config(
    path: str, required_keys: list[str] | None = None, prefix: str = "DEKIT_"
) -> dict:
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

    for section, settings in data.items():
        if not isinstance(settings, dict):
            continue
        for key, value in settings.items():
            shown = "<redacted>" if _is_sensitive(key) else value
            logger.info("Loaded %s.%s = %s (source: file)", section, key, shown)

    for env_var, value in os.environ.items():
        if not env_var.startswith(prefix):
            continue

        remainder = env_var[len(prefix) :]
        parts = remainder.lower().split("_", 1)
        if len(parts) != 2:
            continue

        section, key = parts
        if section in data and isinstance(data[section], dict):
            data[section][key] = value
            shown = "<redacted>" if _is_sensitive(key) else value
            logger.info(
                "Overrode %s.%s = %s (source: env var %s)", section, key, shown, env_var
            )

    return data
