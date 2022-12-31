import sqlite3


def main():
    count_db = "2"
    k = 1

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if len(cursor.execute("PRAGMA table_info(users)").fetchall()) > 0:
        print(f"Table was found({k}/{count_db})")
    else:
        cursor.execute("CREATE TABLE users("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "user_id INTEGER,"
                       "username TEXT,"
                       "date_reg DATETIME)")
        print(f"Table was not found({k}/{count_db}) | Creating...")
    k += 1

    if len(cursor.execute("PRAGMA table_info(messages)").fetchall()) > 0:
        print(f"Table was found({k}/{count_db})")
    else:
        cursor.execute("CREATE TABLE messages("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "date_send DATETIME,"
                       "from_user INTEGER,"
                       "input_text INTEGER,"
                       "output_text TEXT)")
        print(f"Table was not found({k}/{count_db}) | Creating...")
    k += 1



    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
