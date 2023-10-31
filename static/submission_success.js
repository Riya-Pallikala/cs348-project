document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("add_book");
    const successMessage = document.getElementById("success-message");

    form.addEventListener("submit", function(event) {
        //event.preventDefault(); // Prevent the form from submitting traditionally

        successMessage.style.display = "block";
    });
});