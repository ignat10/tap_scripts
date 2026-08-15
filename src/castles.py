from sqlite3 import connect

from src.actions import Castle
from src.worksheet import get_row, keys
from src.paths import CASTLES_DB_PATH
from src.worksheet import get_column


def iter_castles():
    for row in range(10):
        name = get_available()
        row = get_row(name)
        castle = Castle(**dict(zip(keys, row)))
        try:
            yield castle
        finally:
            release(name)


def initialize() -> None:
    with connect(CASTLES_DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS castles (
                name TEXT PRIMARY KEY,
                is_busy INTEGER NOT NULL DEFAULT 0 CHECK (is_busy IN (0, 1)),
                last_login TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        castles = [(name, 0) for name in get_column("name")]
        connection.executemany(
            """
            INSERT OR IGNORE INTO castles (name, is_busy)
            VALUES (?, ?)
            """,
            castles
        )


def get_available() -> str:
    """Mark a free castle busy. Return False if it is already busy."""
    initialize()
    with connect(CASTLES_DB_PATH) as connection:
        row: tuple[str, bool] = connection.execute(
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

        return row[0]


def release(name: str) -> None:
    initialize()
    with connect(CASTLES_DB_PATH) as connection:
        cursor = connection.execute(
            "UPDATE castles SET is_busy = 0 WHERE name = ?",
            (name,),
        )

    if cursor.rowcount == 0:
        raise KeyError(f"unknown castle: {name}")
