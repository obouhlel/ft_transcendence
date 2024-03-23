export function message() {
    let hash = window.location.hash.substring(1);
    let params = new URLSearchParams(hash.split('?')[1]);
    let message = params.get('message');

    if (message) {
        const messageElement = document.getElementById('message');
        if (messageElement) {
            messageElement.innerText = 'Error : ' + decodeURIComponent(message);
        }
        else {
            console.error(`Element with ID message not found`);
        }
    }
}