import * as JS_UTILS from './jsUtils.js';

function sendRegister(socket, infos) {
    const message = {
        register: 'in',
        username: infos['username'],
    };
    JS_UTILS.sendMessageToSocket(socket, message);
}

function sendUnregister(socket, infos) {
    const message = {
        register: 'out',
        username: infos['username'],
    };
    JS_UTILS.sendMessageToSocket(socket, message);
}

function sendMatchmakingJoin(socket, infos) {
    const message = {
        matchmaking: 'join',
        game: infos['gameName'],
        mmr: infos['mmr'],
        username: infos['username'],
    };
    JS_UTILS.sendMessageToSocket(socket, message);
}

function sendMatchmakingLeave(socket, infos) {
    const message = {
        matchmaking: 'leave',
        game: infos['gameName'],
        mmr: infos['mmr'],
        username: infos['username'],
    };
    JS_UTILS.sendMessageToSocket(socket, message);
}

function doMatchmaking(socket, infos, button) {
    if (button.innerHTML == 'Matchmaking') {
        sendMatchmakingJoin(socket, infos);
    } else if (button.innerHTML == 'Cancel matchmaking') {
        sendMatchmakingLeave(socket, infos);
    }
}

function parseMessage(message, infos) {
    if ('register' in message) {
        if (message['register'] == 'connected') {
            infos['registered'] = true;
        } else if (message['register'] == 'disconnected') {
            infos['registered'] = false;
        }
    }
    if ('matchmaking' in message) {
        const button = document.getElementById('matchmaking');
        if (message['matchmaking'] == 'waitlist joined') {
            button.innerHTML = 'Cancel matchmaking';
        } else if (message['matchmaking'] == 'waitlist leaved') {
            button.innerHTML = 'Matchmaking';
        } else if (message['matchmaking'] == 'match found') {
            JS_UTILS.createCookie('url', message['url'], 1);
            window.location.hash = message['game'];
        }
    }
}

function socketListener(socket, infos) {
    socket.onopen = function () {
        console.log('Connection established');
        sendRegister(socket, infos);
    };

    socket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        console.log('Received message: ' + e.data);
        parseMessage(data, infos);
    };

    socket.onclose = function () {
        console.log('Connection closed');
    };

    socket.onerror = function (error) {
        console.log(`socketMatchmaking error: ${error}`);
        console.error(error);
    };
}

// temp username
function generateRandomString(length) {
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

export function matchmacking(gameName) {
    const url = `wss://${window.location.host}/ws/matchmaking/`;
    const socketMatchmaking = new WebSocket(url);
    let infos = { username: generateRandomString(10), mmr: 0, registered: false, gameName: gameName };
    JS_UTILS.createCookie('username', infos['username'], 1);
    socketListener(socketMatchmaking, infos);

    const btn = document.getElementById('matchmaking');
    btn.addEventListener('click', function () {
        doMatchmaking(socketMatchmaking, infos, btn);
    });
    window.addEventListener('beforeunload', function () {
        sendUnregister(socketMatchmaking, infos);
        socketMatchmaking.close();
    });
}
