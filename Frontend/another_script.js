async function fetchData() {
    const searchInput = document.getElementById('searchInput').value.trim();
    const selectedFilter = document.querySelector('input[name="filter"]:checked')?.value;

    if (!searchInput) {
        alert("Please enter a search value.");
        return;
    }

    let queryParams = new URLSearchParams();
    queryParams.append(selectedFilter, searchInput);

    try {
        console.log("Query Params:", queryParams.toString()); // Debugging

        const response = await fetch(`http://localhost:5000/search_criminal?${queryParams.toString()}`);
        const data = await response.json();

        console.log("API Response:", data); // Debugging

        const resultsTable = document.getElementById("resultsTable");
        resultsTable.innerHTML = ""; // Clear previous results

        // Handle API returning an object instead of an array
        if (!Array.isArray(data) || data.length === 0) {
            resultsTable.innerHTML = `<tr><td colspan="7">No results found</td></tr>`;
            return;
        }

        data.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.id}</td>
                <td>${row.fir_no}</td>
                <td>${row.name}</td>
                <td>${row.date_of_birth}</td>
                <td>${row.location}</td>
                <td>${row.area}</td>
                <td><button onclick="showDetails(${row.id})">View</button></td>
            `;
            resultsTable.appendChild(tr);
        });

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}


// Function to handle showing more details (can be expanded later)
function showDetails(id) {
    alert(`More details for Criminal ID: ${id}`);
}
