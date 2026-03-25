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

async function loadStudent() {
    const userId = localStorage.getItem("user_id");
    const role = localStorage.getItem("role");

    if (!userId || role !== "student") {
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/student/${userId}`);
        const data = await response.json();

        document.getElementById("student-name").textContent = data.student_name;
        document.getElementById("student-number").textContent = data.student_number;
        document.getElementById("total-records").textContent = data.attendance.length;

        const table = document.getElementById("table-body");
        table.innerHTML = "";

        data.attendance.forEach(item => {
            const row = `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.timestamp}</td>
                    <td>${getIdCardIcon(item.id_card_status)}</td>
                    <td>${getFingerprintIcon(item.fingerprint_status)}</td>
                    <td>${getAttendanceIcon(item.attendance_status)}</td>
                    <td>${item.device_id}</td>
                </tr>
            `;
            table.innerHTML += row;
        });
    } catch (error) {
        console.error(error);
        alert("Failed to load student data");
    }
}

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

window.onload = loadStudent;