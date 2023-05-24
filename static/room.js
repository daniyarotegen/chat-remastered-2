const chatLog = document.querySelector('#chat-log')
const roomUuid = JSON.parse(document.getElementById('room-uuid').textContent);
const isGroupChat = JSON.parse(document.getElementById('is-group-chat').textContent);

if (chatLog.childNodes.length <= 1) {
    const emptyText = document.createElement('h3')
    emptyText.id = 'emptyText'
    emptyText.innerText = 'No Messages'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomUuid
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageElement = document.createElement('div')
    const userId = data['user_id']
    const username = data['username']
    const loggedInUserId = JSON.parse(document.getElementById('user_id').textContent)
    const messageText = document.createElement('p');

    messageText.innerText = data.message;
    messageElement.appendChild(messageText);

    if (userId === loggedInUserId) {
        messageElement.classList.add('message', 'sender')
    } else {
        const usernameElement = document.createElement('small');
        usernameElement.classList.add('username');
        usernameElement.innerText = username;
        messageElement.prepend(usernameElement);
        messageElement.classList.add('message', 'receiver')
    }

    chatLog.prepend(messageElement)
    chatLog.scrollTop = chatLog.scrollHeight;

    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelectorAll('.expandable').forEach(function (element) {
    element.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
    messageInputDom.style.height = 'auto';
};
