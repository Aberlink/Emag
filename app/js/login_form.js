const loginForm = document.getElementById('login-form');

const storedUsername = localStorage.getItem('username');
const storedPassword = localStorage.getItem('password');

if (storedUsername) {
    loginForm.username.value = storedUsername;
}

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = event.target.username.value;
    const password = event.target.password.value;

    localStorage.setItem('username', username);
    localStorage.setItem('password', password);

});
