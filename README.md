# de-fundamentals

Core skills refresh before diving into full data engineering projects - SQL, Python packaging/testing, Docker, and data modeling fundamentals.
Built as part of a structured re-skilling plan
(see [full plan](https://github.com/tarynpatterson/de-reskilling-plan)).

## What's in here

| Folder | What it covers |
|---|---|
| `sql-practice/` | 30 solved SQL problems (window functions, CTEs/recursive CTEs, query optimization) plus EXPLAIN ANALYZE before/after comparisons |
| `dekit/` | Small Python package: config loader, retry decorator, CSV-to-Parquet CLI. Tested with pytest, typed, linted with ruff |
| `docker-compose.yml` | Postgres + pgAdmin + a Python loader container, for practicing containerized local dev |
| `modeling/` | Star schema, Data Vault, and One Big Table versions of the same domain, with a tradeoff write-up |
| `data/` | Local NYC taxi dataset loaded into DuckDB (`taxi.duckdb`), used for the EXPLAIN ANALYZE optimization exercises. Gitignored — not committed; see `load_taxi.py` to regenerate |

## Setup

```powershell
uv sync
docker compose up
```

To regenerate the local DuckDB dataset used in `sql-practice/`, download an NYC taxi Parquet file into `data/` (see the plan's Phase 0 setup steps), then run:

```powershell
uv run python data/load_taxi.py
```

## Notes

See `sql-practice/notes.md` for optimization lessons learned along the way.