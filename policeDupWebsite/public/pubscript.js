// JavaScript remains the same as in the previous versions
function addPersonField() {
    const container = document.getElementById("peopleContainer");

    const div = document.createElement("div");
    div.classList.add("person-entry");

    div.innerHTML = `
        <label>Name: <input type="text" name="personName[]" required></label>
        <label>Date Of Birth: <input type="date" name="personDob[]" required></label>
        <label>Relationship: <input type="text" name="relation[]" required></label>
        <button type="button" onclick="removePersonField(this)">Remove</button>
        <br><br>
    `;

    container.appendChild(div);
}

function removePersonField(button) {
    button.parentElement.remove();
}

function submitCriminal(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById("criminalForm"));
    
    let criminalData = {
        name: formData.get("name"),
        dob: formData.get("dob"),
        description: formData.get("description"),
        uniqueIdentifier: formData.get("uniqueIdentifier"),
        firNumber: formData.get("firNumber"),
        people: []
    };

    const personNames = formData.getAll("personName[]");
    const personDobs = formData.getAll("personDob[]");
    const relations = formData.getAll("relation[]");

    for (let i = 0; i < personNames.length; i++) {
        criminalData.people.push({
            personName: personNames[i],
            personDob: personDobs[i],
            relation: relations[i]
        });
    }
    console.log(criminalData);
    document.getElementById("criminalForm").reset();
    document.getElementById("peopleContainer").innerHTML = "";
    fetch("/add-criminal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(criminalData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Criminal & Related People added successfully!");
        } else {
            alert("Error adding data: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

function submitCrime(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById("criminalForm"));

    let crimeData = {
        type: formData.get("crimeType"),
        location: formData.get("crimeLocation"),
        area: formData.get("area"),
        date: formData.get("crimeDate"),
        status: formData.get("crimeStatus"),
        modusOperandi: formData.get("modusOperandi"),
        firNumber: formData.get("crimeFirNumber"),
        bailDetails: formData.get("bailDetails"),
        bailGrantDate: formData.get("bailGrantDate"),
        progress: formData.get("progress"),
        victimDetails: formData.get("victimDetails")
    };
    console.log(crimeData);
    document.getElementById("criminalForm").reset();
    fetch("/add-crime", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(crimeData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Crime details added successfully!");
        } else {
            alert("Error adding data: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}