window.onload = function () {
    const checkbox = document.getElementById("showPassword");
    checkbox.addEventListener("click", function () {
        const passwordInput = document.getElementById("password");
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
        } else {
            passwordInput.type = "password";
        }
    });
};

console.log(`js loaded`)