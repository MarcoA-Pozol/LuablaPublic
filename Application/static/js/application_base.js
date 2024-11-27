$(document).ready(function () {
    // Smooth scrolling for links
    $("a").on("click", function (e) {
        if (this.hash) {
            e.preventDefault();
            const hash = this.hash;
            $("html, body").animate(
                {
                    scrollTop: $(hash).offset().top,
                },
                800,
                function () {
                    window.location.hash = hash;
                }
            );
        }
    });

    // Add hover effect on notifications/messages
    $(".notifications_messages_container a").hover(
        function () {
            $(this).css("opacity", "0.8");
        },
        function () {
            $(this).css("opacity", "1");
        }
    );
});
