document.addEventListener("DOMContentLoaded", () => {
    const registerContainer = document.querySelector(".register-container");
    registerContainer.style.opacity = 0;
    registerContainer.style.transform = "scale(0.9)";
    
    setTimeout(() => {
        registerContainer.style.transition = "all 0.5s ease";
        registerContainer.style.opacity = 1;
        registerContainer.style.transform = "scale(1)";
    }, 100);
});
