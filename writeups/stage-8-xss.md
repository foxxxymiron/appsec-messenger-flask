# Cross-Site Scripting (Stage 8)

## Vulnerability Description
The application was found vulnerable to Stored Cross-Site Scripting (XSS) in the chat rendering functionality (`/chat`). The root cause is the use of the `innerHTML` property in JavaScript to display user-controlled input. This allows an attacker to inject malicious HTML/JavaScript code into the database, which is then executed by the browser of any user viewing the chat.

## Target Environment (Initial State)
The application uses the `messages` table to store chat history. An attacker can inject a payload into this table either by sending a message through the UI or directly via a database injection script (`inject_xss.py`).

## 1. Stored XSS Exploitation (Defacement)
- **Vulnerable Code:** 
  `div.innerHTML = msg.text;`
- **Payload:** `<a href="javascript:document.body.innerHTML='<div style=\'background:#111;color:red;...\'>[!] XSS: СИСТЕМА ВЗЛОМАНА</div>';">Нажми сюда, чтобы выиграть 1000$!</a>`
- **Result:** A user opens the chat and sees a harmless-looking link. Upon clicking it, the JavaScript is executed, completely replacing the DOM and defacing the application.

### Payload Injection (Database)
![XSS Payload](../static/screenshots/xss/02-xss-payload.png)

### Malicious Link in Chat
![XSS Link](../static/screenshots/xss/01-xss-link.png)

### Successful Exploitation Result
![XSS Defacement](../static/screenshots/xss/03-xss-defacement.png)

## 2. Mitigation
To fix the vulnerability, **Safe DOM APIs** were implemented. The unsafe `innerHTML` was replaced with `textContent`, which treats user input strictly as plain text and prevents HTML/JavaScript execution.

- **Fixed Code:** `div.textContent = msg.text;`

### Fixed Code
![Fixed Code XSS](../static/screenshots/xss/05-xss-fixed-code.png)

### Exploit Failed (Payload rendered as text)
![Exploit Failed XSS](../static/screenshots/xss/04-xss-fixed.png)

## 3. Impact
Successful exploitation of this vulnerability allows an attacker to execute arbitrary JavaScript in the context of the victim's browser. This can lead to:
- **Session Hijacking:** Stealing session cookies (if `HttpOnly` is not set).
- **Defacement:** Altering the visual appearance of the application to mislead users.
- **Phishing:** Injecting fake login forms to steal credentials.

## 4. Conclusion
The Stored XSS vulnerability demonstrated the critical importance of separating code from data on the client side. By transitioning from `innerHTML` to `textContent`, the application now safely handles untrusted input, neutralizing the threat of HTML/JS injection.