import logging

import pytest

from dekit.config import ConfigError, load_config


def test_load_config_valid_file(tmp_path):
    config_file = tmp_path / "sample.toml"
    config_file.write_text('[database]\nhost = "localhost"\nport = 5432\n')

    config = load_config(str(config_file), prefix="NO_MATCH_")

    assert config == {"database": {"host": "localhost", "port": 5432}}


def test_load_config_env_override(tmp_path, monkeypatch):
    config_file = tmp_path / "sample.toml"
    config_file.write_text('[database]\nhost = "localhost"\nport = 5432\n')

    monkeypatch.setenv("DEKIT_DATABASE_HOST", "override-host")

    config = load_config(str(config_file))

    assert config["database"]["host"] == "override-host"
    assert config["database"]["port"] == 5432


def test_load_config_missing_file(tmp_path):
    missing_path = tmp_path / "does_not_exist.toml"

    with pytest.raises(ConfigError, match="not found"):
        load_config(str(missing_path))


def test_load_config_malformed_toml(tmp_path):
    config_file = tmp_path / "broken.toml"
    config_file.write_text('[database\nhost = "localhost"\n')

    with pytest.raises(ConfigError, match="Invalid TOML"):
        load_config(str(config_file))


@pytest.mark.parametrize(
    "required_keys, expected_missing",
    [
        (["api"], "api"),
        (["database", "api"], "api"),
        (["database", "api", "cache"], "api"),
    ],
)
def test_load_config_missing_keys(tmp_path, required_keys, expected_missing):
    config_file = tmp_path / "sample.toml"
    config_file.write_text('[database]\nhost = "localhost"\n')

    with pytest.raises(ConfigError, match=expected_missing):
        load_config(str(config_file), required_keys=required_keys)


def test_load_config_redacts_secrets(tmp_path, caplog):
    config_file = tmp_path / "sample.toml"
    config_file.write_text('[database]\nhost = "localhost"\npassword = "hunter2"\n')

    with caplog.at_level(logging.INFO):
        load_config(str(config_file), prefix="NO_MATCH_")

    assert "hunter2" not in caplog.text
    assert "<redacted>" in caplog.text
