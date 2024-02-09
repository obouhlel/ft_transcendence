import { doRequest, SERVER_URL } from './fetch.js';

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('register-form');
    if (!form) { return; }

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        var username = document.getElementById('username').value;
        var firstname = document.getElementById('firstname').value;
        var lastname = document.getElementById('lastname').value;
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
        var password_confirm = document.getElementById('password_confirm').value;
        var avatar = document.getElementById('avatar').files[0];
        var birthdate = document.getElementById('birthdate').value;
        var sex = document.getElementById('sexe').value;

        var data = new FormData();
        data.append('username', username);
        data.append('firstname', firstname);
        data.append('lastname', lastname);
        data.append('email', email);
        data.append('password', password);
        data.append('password_confirm', password_confirm);
        data.append('avatar', avatar);
        data.append('birthdate', birthdate);
        data.append('sexe', sex);

        doRequest.Fetch(`${SERVER_URL}/register/`, 'POST', data, doRequest.callbackRegister);
    });
});
