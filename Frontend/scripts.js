let selectedCriminals = [];

// Function to fetch and display data
function fetchData() {
    const searchQuery = document.getElementById("searchInput").value;

    // Dummy data
    const dummyData = [
        {
            criminalID: "67227778",
            firNumber: "12334",
            name: "Lakshay",
            dob: "1966-12-16",
            location: "Anna Nagar",
            area: "Chennai"
        },
        {
            criminalID: "98765432",
            firNumber: "56789",
            name: "Rahul",
            dob: "1988-05-22",
            location: "T Nagar",
            area: "Chennai"
        }
    ];

    // Inject data into the table
    const resultsTable = document.getElementById("resultsTable");
    resultsTable.innerHTML = "";

    dummyData.forEach(data => {
        const row = `
            <tr>
                <td>${data.criminalID}</td>
                <td>${data.firNumber}</td>
                <td>${data.name}</td>
                <td>${data.dob}</td>
                <td>${data.location}</td>
                <td>${data.area}</td>
                <td><button class="mapping-button" onclick="startMapping(${JSON.stringify(data).replace(/"/g, '&quot;')})">Start Mapping</button></td>
            </tr>
        `;
        resultsTable.innerHTML += row;
    });
}

// Function to store selected criminals and redirect
function startMapping(criminalData) {
    selectedCriminals.push(criminalData);

    // Store the selected criminals in localStorage
    localStorage.setItem("selectedCriminals", JSON.stringify(selectedCriminals));

    // Redirect to mapping.html
    window.location.href = "mapping.html";
}
