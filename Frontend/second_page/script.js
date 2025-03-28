    function fetchData() {
        const searchQuery = document.getElementById("searchInput").value;
        
        // 🚀 Simulating backend data fetch (replace this with actual API call)
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

        // Injecting data into table
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
                    <td><button class="mapping-button">Start Mapping</button></td>
                </tr>
            `;
            resultsTable.innerHTML += row;
        });
    }
