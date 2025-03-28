

document.addEventListener("DOMContentLoaded", function () {
    const backButton = document.getElementById("Back"); // Get the Back button

    if (backButton) { // Ensure the button exists
        backButton.addEventListener("click", function () {
            window.location.href = "mapping.html"; // Redirect to mapping.html
        });
    }
});
