async function loadData() {
    try {
        const response = await fetch("http://127.0.0.1:8000/attendance");
        const data = await response.json();

        const table = document.getElementById("table-body");
        const totalRecords = document.getElementById("total-records");

        table.innerHTML = "";
        totalRecords.textContent = data.length;

        data.forEach(item => {
            const row = `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.student_name}</td>
                    <td>${item.student_id}</td>
                    <td>${item.timestamp}</td>
                </tr>
            `;
            table.innerHTML += row;
        });
    } catch (error) {
        console.error("Error loading data:", error);
        alert("Failed to load data");
    }
}

window.onload = loadData;