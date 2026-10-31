# DOM-based Cross-Site Scripting (Stage 9)

## Vulnerability Description
The application was found vulnerable to DOM-based Cross-Site Scripting (DOM XSS). Unlike Reflected or Stored XSS, the server-side code is completely safe and does not process the payload. The vulnerability exists entirely in the client-side JavaScript.

The root cause is an insecure data flow (Source to Sink):
1. **Source:** The script reads the `name` parameter from the URL (`window.location.search`).
2. **Sink:** The script writes this data directly into the DOM using the unsafe `innerHTML` property.

Because `innerHTML` parses strings as HTML, an attacker can execute arbitrary JavaScript by injecting HTML tags with event handlers.

## Exploitation Steps
1. An attacker crafts a malicious URL containing a payload in the `name` parameter:
   `http://127.0.0.1:5000/chat?name=<img src=x onerror="document.body.innerHTML='<div style=\'background:#111;color:red;...\'>[!] XSS: СИСТЕМА ВЗЛОМАНА</div>'">`
2. The victim clicks the link. The browser requests the page from the server.
3. The server returns a safe, static HTML page.
4. The browser executes the client-side JavaScript, which extracts the payload from the URL and passes it to `innerHTML`.
5. The browser parses the injected `<img>` tag, triggers the `onerror` event, and executes the JavaScript, completely defacing the application.

## Evidence (Exploitation)

### Vulnerable Code
![Vulnerable Code](../static/screenshots/dom-xss/01-vulnerable-code.png)

### DOM XSS Defacement Result
![DOM XSS Defacement](../static/screenshots/dom-xss/02-dom-xss-defacement.png)

## Mitigation
To fix DOM XSS, the application must avoid unsafe DOM APIs and use **Contextual Output Encoding** (Safe DOM APIs).
1. **Safe Sink:** Replaced `header.innerHTML = nameFromUrl` with `header.textContent = nameFromUrl`. This forces the browser to treat the payload as plain text and prevents execution.
2. **Secondary Fix:** Reverted the chat rendering to `div.textContent = msg.text` to prevent the payload from being delivered via a clickable link (Stored XSS).

## Evidence (Defense)

### Fixed Code
![Fixed Code](../static/screenshots/dom-xss/03-fixed-code.png)

### Exploit Failed (Payload rendered as text)
![Exploit Failed](../static/screenshots/dom-xss/04-exploit-failed.png)

---

## XSS Types Comparison (Reflected vs Stored vs DOM)

| Feature | Reflected XSS | Stored XSS | DOM XSS |
| :--- | :--- | :--- | :--- |
| **Location of Vulnerability** | Server-side (Backend) | Server-side + Database | Client-side (JavaScript) |
| **Role of Server** | Actively reflects payload in the response | Stores and retrieves payload from the DB | Passive (returns safe, static HTML) |
| **Payload Execution** | In the HTTP response from the server | When a user opens the infected page | When the client-side JS reads the URL |
| **Attack Scale** | Targeted (requires sending a link) | Mass (affects all users visiting the page) | Targeted (requires sending a link) |
