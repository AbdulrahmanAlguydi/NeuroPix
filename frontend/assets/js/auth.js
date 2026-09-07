const loginForm = document.querySelector("#loginForm");
const registerForm = document.querySelector("#registerForm");

// Keep JSON requests in one helper so login and registration use the same format.
async function postJson(url, body) {
	const response = await fetch(url, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(body),
	});
	const data = await response.json();
	return { response: response, data: data };
}

if (loginForm) {
	loginForm.addEventListener("submit", async function (event) {
		event.preventDefault();

		const username = document.querySelector("#loginUsername").value.trim();
		const password = document.querySelector("#loginPassword").value;
		if (!username || !password) {
			alert("Please enter your username and password.");
			return;
		}

		const result = await postJson("/api/auth/login", {
			username: username,
			password: password,
		});
		if (result.response.ok) {
			window.location.href = "dashboard.html";
		} else {
			let message = result.data.error;
			if (!message) {
				message = "Login failed. Please try again.";
			}
			alert(message);
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

		// The backend performs the final validation and saves the password hash.
		const result = await postJson("/api/auth/register", {
			username: username,
			password: password,
		});
		if (result.response.ok) {
			alert("Account created! Please log in.");
			window.location.href = "login.html";
		} else {
			let message = result.data.error;
			if (!message) {
				message = "Registration failed. Please try again.";
			}
			alert(message);
		}
	});
}
