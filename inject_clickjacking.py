import sqlite3

conn = sqlite3.connect('app.db')
conn.execute("""
    INSERT INTO messages (sender, recipient, text) 
    VALUES ('Иван', 'admin', 'Привет! Смотри какой приз я выиграл! http://127.0.0.1:5500/attack/clickjacking_realisation.html')
""")
conn.commit()
conn.close()
print("Сообщение добавлено!")