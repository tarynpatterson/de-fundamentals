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

## Setup

```powershell
uv sync
docker compose up
```

## Notes

See `sql-practice/notes.md` for optimization lessons learned along the way.
