$(document).ready(function() {
    // DOM Elements
    const form = document.getElementById("create-deck-form");
    const language = document.getElementById("selected-language").textContent;

    console.log("Deck creation script loaded succesfully");
    console.log("Selected Language:", language);

    $('#create-deck-button').on('click', function(event){
        event.preventDefault();

        // Get the form fields directly by their IDs
        const title = document.getElementById("id_title")?.value.trim() || "";
        const description = document.getElementById("id_description")?.value.trim() || "";
        const hsk_level = document.getElementById("id_hsk_level")?.value.trim() || "";
        const cefr_level = document.getElementById("id_cefr_level")?.value.trim() || "";
        const is_shareable = document.getElementById("id_is_shareable")?.value.trim() || "";
        const image = document.getElementById("id_image")?.value.trim() || "";

        // Validation
        let isValid = true;

        if (!is_shareable) {
            isValid = true;
            console.warn("'Is shareable' field is not required, user can decide if share the deck with the community or not.");
        } else {
            isValid = true;
            console.warn("'Is shareable' field is not required, user can decide if share the deck with the community or not.");
        }
        if (!image) {
            isValid = true;
            console.warn("'Image' field is not required, but it is recommended to place an image there.");
        } else {
            isValid = true;
            console.warn("'Image' field is not required, but it is recommended to place an image there.");
        }
        if (!title) {
            isValid = false;
            console.error("'Title' field is required.");
        }
        if (!description) {
            isValid = false;
            console.error("'Description' fields is required.");
        }
        if (language === "Chinese"){
            if (!hsk_level) {
                isValid = false;
                console.error("'HSK level' field is required.");
            }
        } else {
            if (!cefr_level) {
                isValid = false;
                console.error("'CEFR level' field is required.");
            }
        }

        if (isValid) {
            showAlert();
        } else {
            showError();
        }
    })


    // Show Alert or Error depending the data validation on Deck creation formulary.
    
    function showAlert() {
        console.log("New deck created");
        const alertBox = document.getElementById('alert-box');

        alertBox.classList.remove('hidden');
        alertBox.classList.add('visible');

        // Remove the alert after 2.5 seconds
        setTimeout(() => {
            alertBox.classList.remove('visible');
            alertBox.classList.add('hidden');
        }, 2500);

        form.submit();
    }

    function showError() {
        console.log("Fill up all the required fields please.");
        const errorBox = document.getElementById('error-box');

        errorBox.classList.remove('hidden');
        errorBox.classList.add('visible');

        // Remove alert after 2.5 seconds
        setTimeout(() => {
            errorBox.classList.remove('visible');
            errorBox.classList.add('hidden');
        }, 2500);
    }
})