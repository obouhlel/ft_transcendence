export function sendMessageToSocket(socket, message) {
    socket.send(JSON.stringify(message));
    console.log("Sent message: " + JSON.stringify(message));
}

export function createCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

export function readCookie(name) {
    let cherchName = name + "=";
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i];
        while (cookie.charAt(0) == ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(cherchName) == 0) {
            return cookie.substring(cherchName.length, cookie.length);
        }
    }
}

export function eraseCookie(name) {
    createCookie(name, "", -1);
}