document.addEventListener('DOMContentLoaded', () => {
    let currentChat = 'Иван';
    const input = document.getElementById('messageInput');
    const button = document.getElementById('sendBtn');
    const messagesBox = document.querySelector('.messages');
    const userHeader = document.getElementById('chatUserName');

    async function loadMessages() {
        const response = await fetch('/api/messages');
        const messages = await response.json();
        
        messagesBox.innerHTML = '';
        
        messages.forEach((msg) => {
            if (msg.sender === currentChat || msg.recipient === currentChat) {
                const div = document.createElement('div');
                const isMe = msg.sender === sessionStorage.getItem('currentUser');
                div.className = 'message ' + (isMe ? 'me' : 'them');
                div.textContent = msg.text;
                messagesBox.appendChild(div);
            }
        });

        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        await fetch('/api/messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, recipient: currentChat })
        });

        input.value = '';
        loadMessages();
    }

    button.addEventListener('click', sendMessage);

    input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });

    const contacts = document.querySelectorAll('.contact');
    contacts.forEach((contact) => {
        contact.addEventListener('click', () => {
            const name = contact.textContent.trim();
            currentChat = name;
            userHeader.textContent = name;
            loadMessages();
        });
    });

    loadMessages();
});
