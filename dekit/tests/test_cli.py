import duckdb

from dekit.cli import main


def test_csv_to_parquet_converts_file(tmp_path):
    input_file = tmp_path / "data.csv"
    input_file.write_text("col1,col2\n1,2\n3,4\n")

    output_file = tmp_path / "out.parquet"

    exit_code = main(["csv-to-parquet", str(input_file), str(output_file)])

    assert exit_code == 0
    assert output_file.exists()

    con = duckdb.connect()
    rows = con.sql(f"SELECT * FROM '{output_file}' ORDER BY col1").fetchall()
    assert rows == [(1, 2), (3, 4)]


def test_csv_to_parquet_missing_input(tmp_path):
    missing_input = tmp_path / "does_not_exist.csv"
    output_file = tmp_path / "out.parquet"

    exit_code = main(["csv-to-parquet", str(missing_input), str(output_file)])

    assert exit_code == 1
    assert not output_file.exists()


def test_csv_to_parquet_refuses_overwrite(tmp_path):
    input_file = tmp_path / "data.csv"
    input_file.write_text("col1,col2\n1,2\n")

    output_file = tmp_path / "out.parquet"
    output_file.write_text("pretend this is an existing file")

    exit_code = main(["csv-to-parquet", str(input_file), str(output_file)])

    assert exit_code == 1
    assert output_file.read_text() == "pretend this is an existing file"


def test_csv_to_parquet_overwrite_flag_allows_it(tmp_path):
    input_file = tmp_path / "data.csv"
    input_file.write_text("col1,col2\n1,2\n")

    output_file = tmp_path / "out.parquet"
    output_file.write_text("pretend this is an existing file")

    exit_code = main(
        ["csv-to-parquet", str(input_file), str(output_file), "--overwrite"]
    )

    assert exit_code == 0
    assert output_file.read_text() != "pretend this is an existing file"


def test_csv_to_parquet_prints_row_count(tmp_path, capsys):
    input_file = tmp_path / "data.csv"
    input_file.write_text("col1,col2\n1,2\n3,4\n5,6\n")

    output_file = tmp_path / "out.parquet"

    main(["csv-to-parquet", str(input_file), str(output_file)])

    captured = capsys.readouterr()
    assert "3" in captured.out
