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
});
