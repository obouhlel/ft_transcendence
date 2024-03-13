import * as JS_UTILS from './jsUtils.js';

import { doRequest } from '../utils/fetch.js';

// ----------------- Send functions -----------------
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

// ----------------- Listeners -----------------
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

function windowListener(socket, infos, btn) {
    window.addEventListener('hashchange', function () {
        if (socket.readyState == 1) {
            sendUnregister(socket, infos);
            socket.close();
        }
    });

    window.addEventListener('beforeunload', function () {
        if (socket.readyState == 1) {
            sendUnregister(socket, infos);
            socket.close();
        }
    });

    btn.addEventListener('click', function () {
        if (btn.innerHTML == 'Matchmaking') {
            sendMatchmakingJoin(socket, infos);
        } else if (btn.innerHTML == 'Cancel matchmaking') {
            sendMatchmakingLeave(socket, infos);
        }
    });
}

export async function matchmacking(gameName) {
    const url = `wss://${window.location.host}/ws/matchmaking/`;
    const socketMatchmaking = new WebSocket(url);

    const JsonUsername = await doRequest.get(`/api/get_user_name/`);
    const infos = { username: JsonUsername['username'], mmr: 0, registered: false, gameName: gameName };
    JS_UTILS.createCookie('username', infos['username'], 1);
    
    const btn = document.getElementById('matchmaking');
    
    socketListener(socketMatchmaking, infos);
    windowListener(socketMatchmaking, infos, btn);
}
