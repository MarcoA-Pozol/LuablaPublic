$(document).ready(function() {
    // DOM Elements
    const form = document.getElementById("create-card-form");
    const language = document.getElementById("selected-language").textContent;

    console.log("Card creation script loaded succesfully");
    console.log("Selected Language:", language)

    $('#create-card-button').on('click', function (event){
        event.preventDefault();

        // Get the form fields directly by their IDs
        const word = document.getElementById("id_word")?.value.trim() || "";
        const hanzi = document.getElementById("id_hanzi")?.value.trim() || "";
        const pinyin = document.getElementById("id_pinyin")?.value.trim() || "";
        const meaning = document.getElementById("id_meaning")?.value.trim() || "";
        const examplePhrase = document.getElementById("id_example_phrase")?.value.trim() || "";
        const deck = document.getElementById("id_deck")?.value.trim() || "";

        let isValid = true;
        if (language === "Chinese"){
            if (!hanzi) {
                isValid = false;
                console.error("Hanzi field is required.");
            }
            if (!pinyin) {
                isValid = false;
                console.error("Pinyin field is required.");
            }
        } else {
            if (!word) {
                isValid = false;
                console.error("Word field is required.");
            }
        }
        if (!meaning) {
            isValid = false;
            console.error("Meaning field is required.");
        }
        if (!examplePhrase) {
            isValid = true;
            console.warn("Example phrase is not required, but it´s recommended to be filled too.");
        } else {
            isValid = true;
            console.warn("Example phrase is not required, but it´s recommended to be filled too.");
        }
        if (!deck) {
            isValid = false;
            console.error("Deck field is required.");
        }

        if (isValid) {
            showAlert()
        } else {
            showError()
        }
    })


    // Show Alert to tell the user that the new card was created or there was an issue during formulary filling up.
    function showAlert() {
        console.log("New card created");
        const alertBox = document.getElementById('alert-box');

        alertBox.classList.remove('hidden');
        alertBox.classList.add('visible');

        // Remove the alert after 2.0 seconds
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

        // Remove alert after 2.0 seconds
        setTimeout(() => {
            errorBox.classList.remove('visible');
            errorBox.classList.add('hidden');
        }, 2500);
    }
})

