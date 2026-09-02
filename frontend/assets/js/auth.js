const loginForm = document.querySelector("#loginForm");
const registerForm = document.querySelector("#registerForm");

if (loginForm) {
	loginForm.addEventListener("submit", async function (event) {
		event.preventDefault();

		const username = document.querySelector("#loginUsername").value.trim();
		const password = document.querySelector("#loginPassword").value;

		if (!username || !password) {
			alert("Please enter your username and password.");
			return;
		}

		// Send the login info to the Flask backend and wait for the answer.
		const response = await fetch("/api/auth/login", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ username: username, password: password }),
		});

		const data = await response.json();

		if (response.ok) {
			// Backend says the login worked, go to the dashboard.
			window.location.href = "dashboard.html";
		} else {
			// Backend rejected the login, show the error it sent back.
			alert(data.error || "Login failed. Please try again.");
		}
	});
}

if (registerForm) {
	registerForm.addEventListener("submit", function (event) {
		event.preventDefault();

		const username = document.querySelector("#registerUsername").value.trim();
		const password = document.querySelector("#registerPassword").value;
		const confirmPassword = document.querySelector("#confirmPassword").value;

		if (!username) {
			alert("Please enter a username.");
			return;
		}

		if (password !== confirmPassword) {
			alert("Passwords do not match.");
			return;
		}

		// Temporary navigation until backend registration is connected.
		window.location.href = "dashboard.html";
	});
}
