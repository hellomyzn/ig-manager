"""common.csv.csv_writer"""
import csv
import os
from typing import Optional


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


def read_last_fetched(filepath: str, id_col: str = "id") -> dict:
    """各 ID の最終 fetched_at を返す。

    Args:
        filepath: 読み込む CSV ファイルパス
        id_col: ID カラム名

    Returns:
        {id: fetched_at} の辞書（ファイルが存在しない場合は空辞書）
    """
    if not os.path.exists(filepath) or not _file_has_content(filepath):
        return {}

    result = {}
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            result[row[id_col]] = row["fetched_at"]
    return result


def _file_has_content(filepath: str) -> bool:
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0
