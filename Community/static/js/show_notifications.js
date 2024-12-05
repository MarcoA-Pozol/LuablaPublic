$(document).ready(function() {
    console.log("Read notifications script loaded successfully!")


    $(".read-notification-button").on('click', function() {
        const notificationId = $(this).data('id'); // Retrieve notification ID from data-id on the button saved as data parameter

        if(!notificationId) {
            console.error("No notification ID found for this notification´s button.");
            return;
        }

        // Make AJAX request to save the current notification as read
        $.ajax({
            url: readNotificationUrl,
            type: "POST",
            data: JSON.stringify({ notification_id: notificationId }),
            contentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },
            success: function(response) {
                console.log("Notification read:", response.message);

                // Remove the Notification´s HTML element from the DOM
                $(`#notification-${notificationId}`).remove();

                // If no more notifications are available
                if ($('.notification').length === 0) {
                    console.log("There are no more notifications available.")
                    //$('#notifications-container').classList.remove('visible');
                    $('#notifications-container').removeClass('notifications-container').addClass('hidden');
                    $('#no-notifications-container').removeClass('hidden').addClass('no-notifications-container');

                }
            },
            error: function(error) {
                console.error("Error reading notification:", error.responseJSON?.error || error);
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