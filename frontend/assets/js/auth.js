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
	registerForm.addEventListener("submit", async function (event) {
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

		// Send the new account info to the Flask backend.
		const response = await fetch("/api/auth/register", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ username: username, password: password }),
		});

		const data = await response.json();

		if (response.ok) {
			// Account was created, send the user to log in with it.
			alert("Account created! Please log in.");
			window.location.href = "login.html";
		} else {
			alert(data.error || "Registration failed. Please try again.");
		}
	});
}
