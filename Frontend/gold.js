async function loadGold() {
    const userId = localStorage.getItem("user_id");
    const role = localStorage.getItem("role");

    if (!userId || role !== "gold_user") {
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/gold/${userId}`);
        const data = await response.json();

        document.getElementById("gold-name").textContent = data.gold_name;

        const table = document.getElementById("gold-body");
        table.innerHTML = "";

        data.classes.forEach(item => {
            const row = `
                <tr>
                    <td>${item.class_id}</td>
                    <td>${item.class_name}</td>
                    <td>${item.enrolled_count}</td>
                    <td>${item.attended_count}</td>
                    <td>${item.absent_count}</td>
                    <td>${item.summary}</td>
                    <td><button class="refresh-btn" onclick="openClass(${item.class_id})">Open</button></td>
                </tr>
            `;
            table.innerHTML += row;
        });
    } catch (error) {
        console.error(error);
        alert("Failed to load gold user data");
    }
}

function openClass(classId) {
    localStorage.setItem("class_id", classId);
    window.location.href = "class.html";
}

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

window.onload = loadGold;