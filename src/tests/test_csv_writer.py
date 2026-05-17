"""tests.test_csv_writer"""
import csv
import pytest
from common.csv.csv_writer import write, read_last_fetched


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


class TestReadLastFetched:
    def test_returns_last_fetched_per_id(self, tmp_path):
        path = tmp_path / "snap.csv"
        rows = [
            {"id": "1", "fetched_at": "2026-05-17T10:00:00"},
            {"id": "1", "fetched_at": "2026-05-17T11:00:00"},
            {"id": "2", "fetched_at": "2026-05-17T09:00:00"},
        ]
        write(str(path), rows, mode="w")
        result = read_last_fetched(str(path), id_col="id")
        assert result["1"] == "2026-05-17T11:00:00"
        assert result["2"] == "2026-05-17T09:00:00"

    def test_returns_empty_dict_when_file_not_exists(self, tmp_path):
        path = tmp_path / "missing.csv"
        result = read_last_fetched(str(path), id_col="id")
        assert result == {}

    def test_returns_empty_dict_when_file_is_empty(self, tmp_path):
        path = tmp_path / "empty.csv"
        path.touch()
        result = read_last_fetched(str(path), id_col="id")
        assert result == {}
