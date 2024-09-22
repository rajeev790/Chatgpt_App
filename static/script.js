document.getElementById('user-input')?.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message === '') return;

    addMessageToChatBox('user-message', message);
    userInput.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        addMessageToChatBox('bot-message', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function addMessageToChatBox(className, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = className;
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function search(query) {
    window.location.href = `/search?query=${encodeURIComponent(query)}`;
}
