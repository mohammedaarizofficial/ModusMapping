<<<<<<< HEAD
function viewMore(summary) {
    localStorage.setItem("crimeSummary", summary);
    window.location.href = "/Frontend/second_page/mapping.html";
}


=======
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const filterOptions = document.querySelectorAll("input[name='filter']");

    // Function to update the placeholder based on selected filter
    function updatePlaceholder() {
        const selectedFilter = document.querySelector("input[name='filter']:checked")?.value;

        if (selectedFilter === "criminal_id") {
            searchInput.placeholder = "Enter Criminal ID";
        } else if (selectedFilter === "name") {
            searchInput.placeholder = "Enter Criminal Name";
        } else if (selectedFilter === "fir_no") {
            searchInput.placeholder = "Enter FIR Number";
        } else {
            searchInput.placeholder = "Search by Criminal Name, FIR Number, Place...";
        }
    }

    // Attach event listeners to all radio buttons
    filterOptions.forEach(radio => {
        radio.addEventListener("change", updatePlaceholder);
    });

    // Ensure placeholder updates on page load
    updatePlaceholder();
});

// Your existing fetchData function remains unchanged
>>>>>>> origin/main
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
                <td><button onclick="viewMore(${row.id})">View More</button></td>
            `;
            resultsTable.appendChild(tr);
        });

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Function to handle showing more details (can be expanded later)
// function showDetails(id) {
//     alert(`More details for Criminal ID: ${id}`);
// }
