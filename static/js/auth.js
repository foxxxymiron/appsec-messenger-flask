document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirmPassword');
    const errorBox = document.getElementById('errorMessage');

    form.addEventListener('submit', (event) => {
        errorBox.textContent = '';

        const username = usernameInput.value.trim();
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        const confirm = confirmInput.value;

        let error = '';

        if (username.length < 3) {
            error = 'Логин должен быть не менее 3 символов';
        } else if (!email.includes('@') || !email.includes('.')) {
            error = 'Введите корректный email';
        } else if (password.length < 6) {
            error = 'Пароль должен быть не менее 6 символов';
        } else if (password !== confirm) {
            error = 'Пароли не совпадают';
        }

        if (error) {
            event.preventDefault();
            errorBox.textContent = error;
        }
    });
});