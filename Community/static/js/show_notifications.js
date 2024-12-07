$(document).ready(function() {
    console.log("Read notifications script loaded successfully!")




    // Read Notification
    $(".read-notification-button").on('click', function() {
        const notificationId = $(this).data('id'); // Retrieve notification ID from data-id as identifier for each loaded notification in the template
        const readNotificationId = $(this).data('id'); // Retrieve read notification ID from data-id as identifier for each loaded notification in the template

        if(!notificationId) {
            console.error("No any notification related to the current ID was found.");
            return;
        }

        if(!readNotificationId) {
            console.error("No any read notification related to the current ID was found.");
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
                //$(`#notification-${notificationId}`).remove();

                $(`#notification-${notificationId}`).prependTo('#read-notifications-container'); // Move the notification to the "read notifications" container
                $(`#notification-${notificationId}`).removeClass('notification').addClass('read-notification'); // Change its style (.notification style -> .read-notifiation style)
                $(`#notification-${notificationId}`).find("button").remove(); // Remove the read-notification-button after notification is read
                $('#no-notifications-container').removeClass('no-notifications-container').addClass('hidden'); // Hide No notifications Container

                // If no more notifications are available
                if ($('.notification').length === 0) {
                    console.log("There are no more notifications available.")
                    $('#no-notifications-container').removeClass('hidden').addClass('no-notifications-container');
                }
            },
            error: function(error) {
                console.error("Error reading notification:", error.responseJSON?.error || error);
            },
        });
    });


    // Delete read Notification
    $(".delete-notification-button").on('click', function() {
        const notificationId = $(this).data('id');

        if (!notificationId) {
            console.error("No any read notification related with the ID was found.");
            return;
        }

        // AJAX request to delete notification from DB
        $.ajax({
            url: deleteNotificationUrl,
            type: "POST",
            data: JSON.stringify({ notification_id: notificationId }),
            contentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },
            success: function(response) {
                console.log("Notification was deleted:", response.message);

                $(`#read-notification-${notificationId}`).remove();
            }
        })
    });


    // Display new notifications list
    $(".list-new-notifications-button").on('click', function() {
        $('#notifications-container').removeClass('hidden').addClass('notifications-container');
        $('#read-notifications-container').removeClass('read-notifications-container').addClass('hidden');
    });


    // Display read notifications list
    $(".list-read-notifications-button").on('click', function() {
        $('#notifications-container').removeClass('notifications-container').addClass('hidden');
        $('#read-notifications-container').removeClass('hidden').addClass('read-notifications-container');
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