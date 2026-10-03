# dekit — build notes

What I learned building each module, beyond just "it works."

## Config loader

- Built a custom `ConfigError` exception instead of letting raw `tomllib`/`FileNotFoundError` errors leak out, so callers get one consistent, clear exception type with a message naming exactly what's wrong (missing file, invalid TOML, or which required keys are missing).
- Environment variable overrides use a `PREFIX_SECTION_KEY` convention, split on the first underscore only, so keys containing underscores (like `max_connections`) still parse correctly.
- Logging records where every value came from (file vs. env override), but keys matching `password`/`secret`/`token` are redacted before logging — proven with a `caplog`-based test that asserts the real secret value never appears in captured log output.
- Tests use `tmp_path` for every file-based case (no shared fixture files), `monkeypatch.setenv` for the env-override test (auto-cleans up after itself), and `pytest.mark.parametrize` to cover multiple missing-key scenarios with one test function.

## Retry decorator

- (fill in after Day 3)

## CSV-to-Parquet CLI

- (fill in after Day 4)