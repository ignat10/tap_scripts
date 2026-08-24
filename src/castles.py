from sqlite3 import Connection, Row, connect
from typing import Any

from src.paths import CASTLES_DB_PATH


DATA_COLUMNS = ("name", "lv", "google", "account", "alliance", "marches_limit")
MUTABLE_COLUMNS = frozenset(DATA_COLUMNS[1:])


def _connect() -> Connection:
    connection = connect(CASTLES_DB_PATH, timeout=30)
    connection.row_factory = Row
    connection.execute("PRAGMA busy_timeout = 30000")
    return connection


def get_castle(name: str) -> dict[str, Any]:
    with _connect() as connection:
        row = connection.execute(
            f"SELECT {', '.join(DATA_COLUMNS)} FROM castles WHERE name = ?",
            (name,),
        ).fetchone()
    if row is None:
        raise KeyError(f"unknown castle: {name}")
    return dict(row) # type: ignore


def get_column(column: str) -> list[Any]:
    if column not in DATA_COLUMNS:
        raise ValueError(f"unknown castle column: {column}")
    with _connect() as connection:
        return [row[0] for row in connection.execute(f"SELECT {column} FROM castles")]


def update_castle(name: str, column: str, value: Any) -> None:
    if column not in MUTABLE_COLUMNS:
        raise ValueError(f"cannot update castle column: {column}")
    with _connect() as connection:
        cursor = connection.execute(
            f"UPDATE castles SET {column} = ? WHERE name = ?",
            (value, name),
        )
    if cursor.rowcount != 1:
        raise KeyError(f"unknown castle: {name}")


def iter_castles():
    # Imported locally because actions persists Castle properties through this module.
    from src.actions import Castle

    while True:
        name = get_available()
        castle = Castle(**get_castle(name))
        try:
            yield castle
        finally:
            release(name)


def get_available() -> str:
    """Mark a free castle busy. Return False if it is already busy."""
    with _connect() as connection:
        row = connection.execute(
            """
            UPDATE castles
            SET is_busy = 1, last_login = CURRENT_TIMESTAMP
            WHERE name = (
                SELECT name
                FROM castles
                WHERE is_busy = 0
                ORDER BY last_login ASC
                LIMIT 1
            )
            RETURNING name
            """
        ).fetchone()

        if row is None:
            raise RuntimeError(f"No available castles in {CASTLES_DB_PATH}")
        return row[0]


def release(name: str) -> None:
    with _connect() as connection:
        cursor = connection.execute(
            "UPDATE castles SET is_busy = 0 WHERE name = ?",
            (name,),
        )

    if cursor.rowcount == 0:
        raise KeyError(f"unknown castle: {name}")


def release_all() -> None:
    """Release every castle before starting a new group of workers."""
    with _connect() as connection:
        connection.execute("UPDATE castles SET is_busy = 0")
