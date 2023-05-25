const chatLog = document.querySelector('#chat-log')
const roomUuid = JSON.parse(document.getElementById('room-uuid').textContent);
const isGroupChat = JSON.parse(document.getElementById('is-group-chat').textContent);
const picker = document.querySelector('#emoji-picker');
const emojiButton = document.querySelector('#emoji-button');

emojiButton.addEventListener('click', () => {
    if (picker.style.display === 'none') {
        picker.style.display = 'block';
    } else {
        picker.style.display = 'none';
    }
});

picker.addEventListener('emoji-click', event => {
    const messageInputDom = document.querySelector('#chat-message-input');
    messageInputDom.value += event.detail.emoji.unicode;
});

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

    if (data.message.startsWith('A file has been uploaded: ')) {
        const fileUrl = data.message.split(': ')[1];
        const fileLink = document.createElement('a');
        fileLink.href = fileUrl;
        fileLink.innerText = 'Download the uploaded file';
        messageElement.appendChild(fileLink);
    } else {
        const messageText = document.createElement('p');
        messageText.innerText = data.message;
        messageElement.appendChild(messageText);
    }

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

document.querySelector('#file-upload').addEventListener('change', function() {
    const file = this.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const csrftoken = getCookie('csrftoken');

    $.ajax({
        url: '/upload/' + roomUuid + '/',
        headers: {'X-CSRFToken': csrftoken},
        data: formData,
        type: 'POST',
        contentType: false,
        processData: false,
        success: function(response) {
            const messageElement = document.createElement('div');
            const fileLink = document.createElement('a');
            fileLink.href = response.file_url;
            fileLink.innerText = 'Download the uploaded file';
            messageElement.appendChild(fileLink);
            messageElement.classList.add('message', 'sender')
            chatLog.prepend(messageElement)
            chatLog.scrollTop = chatLog.scrollHeight;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error(errorThrown);
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const pollSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/poll/'
    + roomUuid
    + '/'
);

pollSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const pollArea = document.querySelector('#poll-area');
    const pollElement = document.createElement('div');

    if (data.type === 'new_poll') {
        const questionElement = document.createElement('h3');
        questionElement.innerText = data.question;
        pollElement.appendChild(questionElement);

        data.options.forEach(option => {
            const optionElement = document.createElement('button');
            optionElement.innerText = option.text;
            const voteCountElement = document.createElement('span');
            voteCountElement.innerText = ' (0 votes)';
            optionElement.appendChild(voteCountElement);

            optionElement.addEventListener('click', function() {
                pollSocket.send(JSON.stringify({
                    'type': 'vote',
                    'user_id': loggedInUserId,
                    'poll_id': data.poll_id,
                    'option_id': option.id
                }));
            });
            pollElement.appendChild(optionElement);
        });
    }

    else if (data.type === 'new_vote') {
        const optionElement = pollElement.querySelector(`[data-option-id="${data.option_id}"]`);
        const voteCountElement = optionElement.querySelector('span');
        const currentVoteCount = parseInt(voteCountElement.innerText.match(/\d+/)[0]);
        voteCountElement.innerText = ` (${currentVoteCount + 1} votes)`;
    }

    pollArea.appendChild(pollElement);
};


