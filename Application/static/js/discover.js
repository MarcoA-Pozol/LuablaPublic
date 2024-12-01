$(document).on('click', '.get-deck-button', function() {
    const deckId = $(this).data('id'); // Retrieve deck ID from data-id
    if (!deckId) {
        console.error("No deck ID found for this button.");
        return;
    }

    // Make AJAX request to save the current user as an owner of the deck
    $.ajax({
        url: "{% url 'get-deck-ajax' %}",
        type: "POST",
        data: JSON.stringify({ deck_id: deckId }),
        contentType: "application/json",
        headers: { "X-CSRFToken": "{{ csrf_token }}" },
        success: function(response) {
            console.log("Deck obtained:", response.message);
            
            // Remove the deck's HTML element from the DOM
            $(`#deck-${deckId}`).remove();

            // Notify the user that a new deck is obtained to study
            showAlert();

            // If no more decks are available
            if ($('.deck').length === 0) {
                $('#decks-container').html(`
                    <h5 id="no_decks_available" style="
                        width: 100%;
                        text-align: center;
                        justify-content: center;
                        align-content: center;
                        font-size: 2.0rem;
                        color: #222;">
                        No more decks available
                    </h5>
                    <h6 style="margin-left:30%;width:40%;text-align: center;justify-content: center;font-size: 1.4rem;color: #333;">
                        Redirecting...
                    </h6>
                `);

                // Redirect to learn page after a short delay
                setTimeout(() => {
                    window.location.href = "{% url 'study' %}";
                    showAlert()
                }, 1800);
            }
        },
        error: function(error) {
            console.error("Error obtaining deck:", error.responseJSON?.error || error);
        },
    });
});


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

const csrftoken = getCookie('csrftoken');

function updateOptions() {
    const form = document.getElementById('filter-form');
    form.submit();  // Automatically submit form to update options
}

function updateDecks() {
    const form = document.getElementById('filter-form');
    const formData = new FormData(form);
    const url = form.action;

    fetch(url + '?' + new URLSearchParams(formData), {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken  
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update the decks container with the new HTML
        document.getElementById('decks-container').innerHTML = data.html;
    })
    .catch(error => console.log('Error:', error));
}

// Debugging: Log the raw cards JSON to the console for verification
console.log("Deck JSON:", JSON.parse('{{ decks_json|escapejs }}')); 

// Parse Decks to JSON safely
let decks_list = JSON.parse('{{ decks_json|escapejs}}');

function showAlert() {
    const alertBox = document.getElementById('alert-box');
    alertBox.classList.remove('hidden');
    alertBox.classList.add('visible');

    // Remove the alert after 2.5 seconds
    setTimeout(() => {
        alertBox.classList.remove('visible');
        alertBox.classList.add('hidden');
    }, 2500);
}