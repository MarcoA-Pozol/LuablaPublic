document.addEventListener("DOMContentLoaded", () => {
    const loginContainer = document.querySelector(".login-container");
    loginContainer.style.opacity = 0;
    loginContainer.style.transform = "translateY(20px)";
    
    setTimeout(() => {
        loginContainer.style.transition = "all 0.5s ease";
        loginContainer.style.opacity = 1;
        loginContainer.style.transform = "translateY(0)";
    }, 100);
});
