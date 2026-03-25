async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("message");

    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Login failed";
            return;
        }

        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("role", data.role);

        if (data.role === "student") {
            window.location.href = "student.html";
        } else if (data.role === "professor") {
            window.location.href = "professor.html";
        } else if (data.role === "gold_user") {
            window.location.href = "gold.html";
        } else {
            message.textContent = "Unknown role";
        }
    } catch (error) {
        console.error(error);
        message.textContent = "Connection error";
    }
}