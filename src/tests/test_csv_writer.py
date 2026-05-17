"""tests.test_csv_writer"""
import csv
import pytest
from common.csv.csv_writer import write


class TestWrite:
    def test_creates_file_with_header(self, tmp_path):
        path = tmp_path / "out.csv"
        rows = [{"id": "1", "val": "a"}, {"id": "2", "val": "b"}]
        write(str(path), rows, mode="w")
        with open(path) as f:
            reader = list(csv.DictReader(f))
        assert len(reader) == 2
        assert reader[0]["id"] == "1"

    def test_overwrite_replaces_content(self, tmp_path):
        path = tmp_path / "out.csv"
        write(str(path), [{"id": "1"}], mode="w")
        write(str(path), [{"id": "2"}], mode="w")
        with open(path) as f:
            reader = list(csv.DictReader(f))
        assert len(reader) == 1
        assert reader[0]["id"] == "2"

    def test_append_adds_rows_without_duplicate_header(self, tmp_path):
        path = tmp_path / "out.csv"
        write(str(path), [{"id": "1"}], mode="w")
        write(str(path), [{"id": "2"}], mode="a")
        with open(path) as f:
            reader = list(csv.DictReader(f))
        assert len(reader) == 2

    def test_append_to_empty_file_writes_header(self, tmp_path):
        path = tmp_path / "out.csv"
        path.touch()
        write(str(path), [{"id": "1"}], mode="a")
        with open(path) as f:
            reader = list(csv.DictReader(f))
        assert len(reader) == 1

    def test_write_empty_rows_does_nothing(self, tmp_path):
        path = tmp_path / "out.csv"
        write(str(path), [], mode="w")
        assert not path.exists() or path.stat().st_size == 0
