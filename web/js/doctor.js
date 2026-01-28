const token = localStorage.getItem("token");
if (!token) {
    alert("Login first");
    window.location.href = "/web/login.html";
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/web/login.html";
}

// Add doctor
async function addDoctor() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const specialty = document.getElementById("specialty").value;
    const phone = document.getElementById("phone").value;

    if (!name || !email || !specialty || !phone) {
        alert("Please fill all fields");
        return;
    }

    const res = await fetch("/doctors/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ name, email, specialty, phone })
    });

    if (res.ok) {
        alert("Doctor added successfully ✅");
        document.getElementById("name").value = "";
        document.getElementById("email").value = "";
        document.getElementById("specialty").value = "";
        document.getElementById("phone").value = "";
    } else {
        alert("Failed to add doctor ❌");
    }

    loadDoctors();
}

// Load doctors
async function loadDoctors() {
    const res = await fetch("/doctors/", {
        headers: { "Authorization": "Bearer " + token }
    });
    const data = await res.json();

    let html = "";
    data.forEach(d => {
        let patients = d.patients.map(p => p.full_name).join(", ") || "No patients";
        html += `<tr>
            <td>${d.name}</td>
            <td>${d.email}</td>
            <td>${d.specialty}</td>
            <td>${d.phone}</td>
            <td>${patients}</td>
            <td>
                <button class="delete-btn" onclick="del(${d.id})">❌</button>
                <button class="edit-btn" onclick="edit(${d.id}, '${d.name}', '${d.email}', '${d.specialty}', '${d.phone}')">✏️</button>
            </td>
        </tr>`;
    });

    document.getElementById("list").innerHTML = html;
}

// Delete doctor
async function del(id) {
    await fetch("/doctors/delete/" + id, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + token }
    });
    loadDoctors();
}

// Edit doctor
async function edit(id, name, email, specialty, phone) {
    const newName = prompt("Name:", name);
    const newEmail = prompt("Email:", email);
    const newSpecialty = prompt("Specialty:", specialty);
    const newPhone = prompt("Phone:", phone);

    await fetch("/doctors/update/" + id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            name: newName,
            email: newEmail,
            specialty: newSpecialty,
            phone: newPhone
        })
    });

    loadDoctors();
}

// Initial load
loadDoctors();
