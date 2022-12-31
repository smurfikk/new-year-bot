from functions.func import *


def admin_stats() -> str:
    conn, cursor = connect()
    cursor.execute("SELECT COUNT(id) FROM users")
    count_users, = cursor.fetchone()
    conn.close()
    text = f"""
<b>Статистика</b>

<b>Всего пользователей:</b> <i>{count_users}</i>
"""
    return text

