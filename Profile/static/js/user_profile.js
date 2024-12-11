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
        $('#update-profile-data-form').removeClass('not-displayed').addClass('update-profile-data-form');
        console.log("Formulary displayed")

        // Smooth scrolling to the bottom (formulary)
        window.scrollTo({
            top: document.body.scrollHeight * 0.5,
            behavior: 'smooth' 
        });
    });



    // Update Profile Data
    $(".update-profile-data-button").on('click', function(event) {
        // Prevent default form submission
        event.preventDefault();

        console.log("Clicked button")

        if (!userID) {
            console.error("No user matches the current ID.") 
            return;
        }

        // Get data from formulary fields 
        // Create a FormData object
        const formData = new FormData();
        const profileImage = document.getElementById("id_profile_image").files[0]; // Use `.files` to get the file
        const learningGoals = document.getElementById("id_learning_goals").value.trim();
        const description = document.getElementById("id_description").value.trim();

        // Append data to FormData
        if (profileImage) formData.append("profile_picture", profileImage);
        formData.append("learning_goals", learningGoals);
        formData.append("description", description);
        formData.append("user_id", userID);


        // Make AJAX request to update user info
        $.ajax({
            url: updateProfileDataURL,
            type: "POST",
            data: formData,
            processData: false, // Prevent jQuery from processing the data
            contentType: false, // Prevent jQuery from setting content type
            constentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },

            //Success
            success: function (response) {
                console.log("Updated profile´s data:", response.message);

                // Update the data that is displayed on the profile´s data with the new updated ones
                if (response.profile_picture) {
                    $('#user-profile-picture').attr('src', `${response.profile_picture}?t=${new Date().getTime()}`);
                    console.log("Profile picture changed:", response.profile_picture);
                }
                if (response.learning_goals) {
                    $('#user-learning-goals').text("“" + response.learning_goals + "”");
                    console.log("Learning goals changed:", response.learning_goals);
                }
                if (response.description) {
                    $('#user-description').text(response.description);
                    console.log("Description changed:", response.description);
                }

                // Smooth scrolling to the top (profile data)
                window.scrollTo({
                    top: document.body.scrollHeight * 0,
                    behavior: 'smooth' 
                });

                // Hide formulary data updating formulary after a success data updation but after 1 second
                setTimeout(() => {
                    $('#update-profile-data-form').addClass('not-displayed').removeClass('update-profile-data-form');
                }, 1000);

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