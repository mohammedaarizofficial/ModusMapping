// document.addEventListener("DOMContentLoaded", function () {
//     const mappedResults = document.getElementById("mappedResults");

//     // Retrieve selected criminals from localStorage
//     const selectedCriminals = JSON.parse(localStorage.getItem("selectedCriminals")) || [];

//     mappedResults.innerHTML = "";

//     selectedCriminals.forEach(data => {
//         const row = `
//             <tr>
//                 <td>${data.criminalID}</td>
//                 <td>${data.firNumber}</td>
//                 <td>${data.name}</td>
//                 <td>${data.dob}</td>
//                 <td>${data.location}</td>
//                 <td>${data.area}</td>
//             </tr>
//         `;
//         mappedResults.innerHTML += row;
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
    const mappedResults = document.getElementById("mappedResults");

    // Retrieve selected criminals from localStorage
    const selectedCriminals = JSON.parse(localStorage.getItem("selectedCriminals")) || [];

    mappedResults.innerHTML = "";

    selectedCriminals.forEach(data => {
        const row = `
            <tr>
                <td>${data.criminalID}</td>
                <td>${data.firNumber}</td>
                <td>${data.name}</td>
                <td>${data.dob}</td>
                <td>${data.location}</td>
                <td>${data.area}</td>
            </tr>
        `;
        mappedResults.innerHTML += row;
    });

    // Get the "View More" button and add a click event listener
    const viewMoreButton = document.getElementById("View-More");
    
    if (viewMoreButton) { // Ensure the button exists
        viewMoreButton.addEventListener("click", function () {
            window.location.href = "Complete-mapping.html"; // Redirect on click
        });
    }
});
