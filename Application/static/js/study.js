$(document).ready(function() {
    console.log("Study page script loaded successfully!")



    // Remove Deck
    $(".remove-deck-button").on('click', function() {
        const deckId = $(this).data('id'); // Retrieve deck ID from data-id on the button saved as data parameter

        if(!deckId) {
            console.error("No deck ID found for this deck´s button.");
            return;
        }

        // Make AJAX request to save the current deck as removed
        $.ajax({
            url: removeDeckUrl,
            type: "POST",
            data: JSON.stringify({ deck_id: deckId }),
            contentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },
            success: function(response) {
                console.log("Deck removed:", response.message);

                // Remove the Deck´s HTML element from the DOM
                $(`#deck-${deckId}`).remove();

                // If no more decks are available
                // if ($('.deck').length === 0) {
                //     console.log("There are no more decks available.")
                //     //$('#decks-container').classList.remove('visible');
                //     $('#decks-container').removeClass('decks-container').addClass('hidden');
                //     $('#no-decks-container').removeClass('hidden').addClass('no-decks-container');

                // }
            },
            error: function(error) {
                console.error("Error reading deck:", error.responseJSON?.error || error);
            },
        });
    });


    

    // Get cookie for better page security
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Define csrftoken using cookie
    const csrftoken = getCookie('csrftoken');


});