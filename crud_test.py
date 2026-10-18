import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()


def create_user(username, email, password):
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )
    conn.commit()
    print(f"Пользователь {username} добавлен.")


def read_users():
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    print("\nСписок пользователей:")
    for user in users:
        print(f"ID: {user[0]}, Логин: {user[1]}, Email: {user[2]}")


def update_user_email(username, new_email):
    cursor.execute(
        "UPDATE users SET email = ? WHERE username = ?",
        (new_email, username)
    )
    conn.commit()
    print(f"Email пользователя {username} обновлен на {new_email}.")


def delete_user(username):
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    print(f"Пользователь {username} удален.")


create_user("test_user", "test@mail.ru", "123456")
create_user("admin", "admin@mail.ru", "adminpass")
read_users()

update_user_email("test_user", "new_test@mail.ru")
read_users()

delete_user("admin")
read_user_list = read_users()

conn.close()