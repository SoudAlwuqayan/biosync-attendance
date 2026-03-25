function getIdCardIcon(status) {
    if (status === "found") {
        return `<span class="status-ok">✔</span>`;
    } else {
        return `<span class="status-bad">✖</span>`;
    }
}

function getFingerprintIcon(status) {
    if (status === "matched") {
        return `<span class="status-ok">✔</span>`;
    } else {
        return `<span class="status-bad">✖</span>`;
    }
}

function getAttendanceIcon(status) {
    if (status === "present") {
        return `<span class="status-ok">✔</span>`;
    } else {
        return `<span class="status-bad">✖</span>`;
    }
}

async function loadClassDetails() {
    const classId = localStorage.getItem("class_id");

    if (!classId) {
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/class/${classId}`);
        const data = await response.json();

        document.getElementById("class-title").textContent = data.class_name;

        const table = document.getElementById("class-table-body");
        table.innerHTML = "";

        data.students.forEach(student => {
            const row = `
                <tr>
                    <td>${student.student_name}</td>
                    <td>${student.student_number}</td>
                    <td>${student.timestamp}</td>
                    <td>${getIdCardIcon(student.id_card_status)}</td>
                    <td>${getFingerprintIcon(student.fingerprint_status)}</td>
                    <td>${getAttendanceIcon(student.attendance_status)}</td>
                    <td>${student.device_id}</td>
                </tr>
            `;
            table.innerHTML += row;
        });
    } catch (error) {
        console.error(error);
        alert("Failed to load class details");
    }
}

function goBack() {
    const role = localStorage.getItem("role");
    if (role === "professor") {
        window.location.href = "professor.html";
    } else if (role === "gold_user") {
        window.location.href = "gold.html";
    } else {
        window.location.href = "login.html";
    }
}

window.onload = loadClassDetails;