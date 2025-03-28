document.addEventListener("DOMContentLoaded", function () {
    const summaryText = localStorage.getItem("crimeSummary");
    if (summaryText) {
        document.querySelector(".summarydetails").innerHTML = summaryText;
        localStorage.removeItem("crimeSummary"); // Remove after displaying
    }
});
