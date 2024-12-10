$(document).ready(function() {
    console.log("Profile script loaded successfully!")


    // Get Cookie for CSRF token and security on formulary sending
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
    };

    // Define csrftoken using cookie
    const csrftoken = getCookie('csrftoken');


    // Display formulary for profile´s data updation
    $("#display-formulary-button").on('click', function() {
        $('#update-profile-data-form').removeClass('hidden');
        console.log("Formulary displayed")
    });



    // Update Profile Data
    $(".update-profile-data-button").on('click', function(event) {
        // Prevent default form submission
        event.preventDefault();

        if (!userId) {
            console.error("No user matches the current ID.") 
            return;
        }

        // Get data from formulary fields 
        const form = document.getElementById("update-profile-data-form");

        const profileImage = document.getElementById("id_profile_image")?.value.trim() || "";
        const learningGoals = document.getElementById("id_learning_goals")?.value.trim() || "";
        const description = document.getElementById("id_description")?.value.trim() || "";


        // Make AJAX request to update user info
        $.ajax({
            url: updateProfileDataURL,
            type: "POST",
            data: JSON.stringify({
                user_id: userId,
                profile_image: profileImage,
                learning_goals: learningGoals,
                description: description
            }),
            constentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },

            //Success
            success: function(response) {
                console.log("Updated profile´s data:", response.message);

                // Form submission turned down because we are using AJAX request instead of Django request: form.onsubmit()

                // Hide formulary data updating formulary after a success data updation
                $('#update-profile-data-form').addClass('hidden');
                

                // Update the data that is displayed on the profile´s data with the new updated ones
                if (profileImage) {
                    $('#user-profile-image').attr('src', profileImage);
                }
                $('#user-learning-goals').text(learningGoals);
                $('#user-description').text(description);


                // Show a "success alert" to let the user know that the data has been updated with success
                showSuccessAlert();
            },
            error: function(error) {
                console.error("Error updating profile´s data:", error.responseJSON?.error || error);
                showErrorAlert();
            },
        });
    });

    function showSuccessAlert() {
        console.log("Updated data!");
        const alertBox = document.getElementById('alert-box');

        alertBox.classList.remove('hidden');
        alertBox.classList.add('visible');

        // Remove the alert after 2.5 seconds
        setTimeout(() => {
            alertBox.classList.remove('visible');
            alertBox.classList.add('hidden');
        }, 2500);
    };

    function showErrorAlert() {
        console.log("There was a server error. Try it again later.");
        const errorBox = document.getElementById('error-box');

        errorBox.classList.remove('hidden');
        errorBox.classList.add('visible');

        // Remove alert after 2.5 seconds
        setTimeout(() => {
            errorBox.classList.remove('visible');
            errorBox.classList.add('hidden');
        }, 3500);
    };
});