import argparse
import os

import duckdb


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dekit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    csv_to_parquet = subparsers.add_parser("csv-to-parquet")
    csv_to_parquet.add_argument("input")
    csv_to_parquet.add_argument("output")
    csv_to_parquet.add_argument("--compression", default="snappy")
    csv_to_parquet.add_argument("--overwrite", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not os.path.exists(args.input):
        print(f"Error: input file not found: {args.input}")
        return 1

    if os.path.exists(args.output) and not args.overwrite:
        print(f"Error: output file already exists: {args.output} (use --overwrite to replace it)")
        return 1

    con = duckdb.connect()
    con.sql(f"""
        COPY (SELECT * FROM read_csv_auto('{args.input}'))
        TO '{args.output}'
        (FORMAT PARQUET, COMPRESSION '{args.compression}')
    """)

    result = con.sql(f"SELECT COUNT(*) FROM '{args.output}'").fetchone()
    assert result is not None
    row_count = result[0]
    print(f"Converted {args.input} to {args.output} ({row_count} rows)")

    return 0