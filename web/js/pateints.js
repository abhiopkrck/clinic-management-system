const token = localStorage.getItem("token");
if (!token) {
    alert("Login first");
    window.location.href = "/";
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

// Load doctor list for dropdown
async function loadDoctors() {
    const res = await fetch("/doctors/", {
        headers: { "Authorization":"Bearer " + token }
    });
    const data = await res.json();
    const select = document.getElementById("doctor_id");
    data.forEach(d => {
        const option = document.createElement("option");
        option.value = d.id;
        option.text = d.name + " (" + d.specialty + ")";
        select.appendChild(option);
    });
}

async function addPatient() {
    const name = document.getElementById("name").value;
    const age = parseInt(document.getElementById("age").value);
    const phone = document.getElementById("phone").value;
    const disease = document.getElementById("disease").value;
    const doctor_id = parseInt(document.getElementById("doctor_id").value) || null;

    if (!name || !age || !phone || !disease) {
        alert("Please fill all fields");
        return;
    }

    const res = await fetch("/patients/add", {
        method: "POST",
        headers: {
            "Content-Type":"application/json",
            "Authorization":"Bearer " + token
        },
        body: JSON.stringify({
            full_name: name,
            age: age,
            phone: phone,
            disease: disease,
            doctor_id: doctor_id
        })
    });

    if (res.ok) {
        alert("Patient added successfully ✅");
        document.getElementById("name").value = "";
        document.getElementById("age").value = "";
        document.getElementById("phone").value = "";
        document.getElementById("disease").value = "";
        document.getElementById("doctor_id").value = "";
    } else {
        alert("Failed to add patient ❌");
    }

    loadPatients(); // reload patients list
}

// Load existing patients
async function loadPatients() {
    const res = await fetch("/patients/list", {
        headers: { "Authorization":"Bearer " + token }
    });
    const data = await res.json();

    let html = "";
    data.forEach(p => {
        html += `<div>
          ${p.full_name} | ${p.age} | ${p.phone} | ${p.disease} | Doctor ID: ${p.doctor_id || "N/A"}
          <button onclick="del(${p.id})">❌</button>
          <button onclick="edit(${p.id}, '${p.full_name}', ${p.age}, '${p.phone}', '${p.disease}', ${p.doctor_id || 0})">✏️</button>
        </div>`;
    });

    document.getElementById("list").innerHTML = html;
}

// Delete patient
async function del(id) {
    await fetch("/patients/delete/" + id, {
        method: "DELETE",
        headers: { "Authorization":"Bearer " + token }
    });
    loadPatients();
}

// Edit patient
async function edit(id, name, age, phone, disease, doctor_id) {
    const newName = prompt("Name:", name);
    const newAge = prompt("Age:", age);
    const newPhone = prompt("Phone:", phone);
    const newDisease = prompt("Disease:", disease);
    const newDoctorId = prompt("Doctor ID:", doctor_id);

    await fetch("/patients/update/" + id, {
        method: "PUT",
        headers: {
            "Content-Type":"application/json",
            "Authorization":"Bearer " + token
        },
        body: JSON.stringify({
            full_name: newName,
            age: parseInt(newAge),
            phone: newPhone,
            disease: newDisease,
            doctor_id: parseInt(newDoctorId) || null
        })
    });

    loadPatients();
}

// Initial load
loadDoctors();
loadPatients();
