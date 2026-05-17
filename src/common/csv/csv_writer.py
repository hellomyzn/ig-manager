"""common.csv.csv_writer"""
import csv
import os


def write(filepath: str, rows: list, mode: str = "w") -> None:
    """CSV にデータを書き込む。

    Args:
        filepath: 出力先ファイルパス
        rows: dict のリスト（全行同一キー構成を前提）
        mode: "w" で上書き、"a" で追記
    """
    if not rows:
        return

    fieldnames = list(rows[0].keys())
    need_header = mode == "w" or not _file_has_content(filepath)

    with open(filepath, mode=mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if need_header:
            writer.writeheader()
        writer.writerows(rows)


def _file_has_content(filepath: str) -> bool:
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0
