from functions.func import *


def first_join(user_id: int, username) -> bool:
    conn, cursor = connect()
    cursor.execute(f"SELECT id FROM users WHERE user_id = ?", [user_id])
    row = cursor.fetchone()
    if not row:
        cursor.execute(f"INSERT INTO users (user_id, username, date_reg) "
                       f"VALUES (?, ?, ?)", (user_id, username, get_date()))
    conn.commit()
    conn.close()
    return row is None


def all_users() -> tuple:
    conn, cursor = connect()
    cursor.execute(f"SELECT user_id FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows
