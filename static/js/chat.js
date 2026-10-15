document.addEventListener('DOMContentLoaded', () => {
    const chats = {
        'Иван': [
            { from: 'them', text: 'Привет!' },
            { from: 'me', text: 'Привет, как дела?' },
            { from: 'them', text: 'Всё отлично' }
        ],
        'Мария': [
            { from: 'them', text: 'Ты где?' },
            { from: 'me', text: 'Скоро буду' }
        ],
        'Группа': [
            { from: 'them', text: 'Всем привет' }
        ]
    };

    let currentChat = 'Иван';

    const input = document.getElementById('messageInput');
    const button = document.getElementById('sendBtn');
    const messagesBox = document.querySelector('.messages');
    const userHeader = document.getElementById('chatUserName');

    
    function renderMessages(contactName) {
        messagesBox.innerHTML = '';

        const messages = chats[contactName] || [];

        messages.forEach((msg) => {
            const div = document.createElement('div');
            div.className = 'message ' + msg.from;
            div.textContent = msg.text;
            messagesBox.appendChild(div);
        });

        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    renderMessages('Иван');
    const contacts = document.querySelectorAll('.contact');
    contacts.forEach((contact) => {
        contact.addEventListener('click', () => {
            const name = contact.textContent.trim();
            currentChat = name;
            userHeader.textContent = name;
            renderMessages(name);
        });
    });

    button.addEventListener('click', () => {
        const text = input.value.trim();
        if (!text) return;

        chats[currentChat].push({ from: 'me', text: text });
        renderMessages(currentChat);

        input.value = '';
    });

    input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            button.click();
        }
    });
});