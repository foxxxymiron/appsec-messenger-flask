# SQL-инъекция (Этап 6)

## Описание уязвимости
В приложении была обнаружена уязвимость SQL-инъекции (SQLi) в функционале аутентификации (`/login`) и поиска (`/search`). Корневой причиной является динамическое конструирование запросов с использованием `f-strings` (конкатенация строк), что позволяет СУБД интерпретировать пользовательский ввод как исполняемый код, а не как данные.

## Целевая база данных (Исходное состояние)
До проведения атаки база данных содержала следующих пользователей:
![Исходные пользователи БД](../static/screenshots/stage-6-sqli/db-all-users.png)

## 1. Обход аутентификации (Auth Bypass)
- **Уязвимый код:** 
  `query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"`
- **Пейлоад:** `' OR '1'='1`
- **Результат:** Успешный вход в систему без знания пароля. База данных вернула первого пользователя, так как условие `1=1` всегда истинно.

### Уязвимый код
![Уязвимый код входа](../static/screenshots/stage-6-sqli/vulnerable-code-login.png)

### Ввод пейлоада
![Ввод пейлоада для обхода](../static/screenshots/stage-6-sqli/auth-bypass-input.png)

### Успешный результат обхода
![Успешный вход в чат](../static/screenshots/stage-6-sqli/auth-bypass-chat.png)

## 2. SQL-инъекция на основе UNION (Эксфильтрация данных)
- **Уязвимый код:** 
  `sql = f"SELECT sender, text FROM messages WHERE text LIKE '%{query}%'"`
- **Пейлоад:** `' UNION SELECT username, password FROM users --`
- **Результат:** Страница поиска отобразила логины и пароли всех пользователей из таблицы `users`.

### Уязвимый код
![Уязвимый код поиска](../static/screenshots/stage-6-sqli/vulnerable-code-search.png)

### Ввод пейлоада
![Ввод пейлоада UNION](../static/screenshots/stage-6-sqli/SQL-injection-UNION.png)

### Украденные данные
![Украденные данные](../static/screenshots/stage-6-sqli/SQL-injection-UNION-result.png)

### Сравнение состояния базы данных
Извлеченные данные совпадают с записями в таблице `users`:
![Пользователи БД после UNION](../static/screenshots/stage-6-sqli/db-UNION-all-users.png)

## 3. Меры защиты (Mitigation)
Для устранения уязвимости были применены **Параметризованные запросы (Prepared Statements)**. Теперь пользовательский ввод передается отдельно от SQL-кода с помощью плейсхолдеров `?`, что предотвращает его интерпретацию как команд.

- **Исправленный код (вход):** `conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))`
- **Исправленный код (поиск):** `conn.execute("SELECT sender, text FROM messages WHERE text LIKE ?", (search_pattern,))`

### Исправленный код
![Исправленный код входа](../static/screenshots/stage-6-sqli/fixed-code-login.png)
![Исправленный код поиска](../static/screenshots/stage-6-sqli/fixed-code-search.png)

### Провал атаки (Обход аутентификации)
![Провал обхода авторизации](../static/screenshots/stage-6-sqli/fixed-auth-bypass.png)

### Провал атаки (UNION-инъекция)
![Провал UNION-инъекции](../static/screenshots/stage-6-sqli/fixed-UNION-injection.png)