document.addEventListener("DOMContentLoaded", () => {
    const languageCards = document.querySelectorAll(".language-card");
    const hiddenInput = document.getElementById("selected-language");
    const submitButton = document.querySelector(".submit-button");

    languageCards.forEach(card => {
        card.addEventListener("click", () => {
            // Remove active state from all cards
            languageCards.forEach(card => card.classList.remove("active"));

            // Add active state to selected card
            card.classList.add("active");

            // Update hidden input value and enable submit button
            hiddenInput.value = card.getAttribute("data-language");
            submitButton.disabled = false;
        });
    });
});
