const pollLog = document.querySelector('#poll-log');
const roomUuid = JSON.parse(document.getElementById('room-uuid').textContent);

const pollSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/poll/'
    + roomUuid
    + '/'
);

pollSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const pollElement = document.createElement('div');
    const questionElement = document.createElement('h3');
    const optionsElement = document.createElement('ul');

    questionElement.innerText = data.question;
    pollElement.appendChild(questionElement);

    data.options.forEach(option => {
        const optionElement = document.createElement('li');
        optionElement.innerText = option;
        optionsElement.appendChild(optionElement);
    });

    pollElement.appendChild(optionsElement);
    pollLog.prepend(pollElement);
    pollLog.scrollTop = pollLog.scrollHeight;
};

pollSocket.onclose = function(e) {
    console.error('Poll socket closed unexpectedly');
};

document.querySelector('#poll-create-button').onclick = function(e) {
    const questionInputDom = document.querySelector('#poll-question-input');
    const optionsInputDom = document.querySelector('#poll-options-input');
    const multipleAnswersDom = document.querySelector('#poll-multiple-answers-input');
    const question = questionInputDom.value;
    const options = optionsInputDom.value.split(',');
    const allowMultipleAnswers = multipleAnswersDom.checked;

    pollSocket.send(JSON.stringify({
        'type': 'create_poll',
        'question': question,
        'options': options,
        'allow_multiple_answers': allowMultipleAnswers,
        'user_id': 'USER_ID'
    }));

    questionInputDom.value = '';
    optionsInputDom.value = '';
    multipleAnswersDom.checked = false;
};
