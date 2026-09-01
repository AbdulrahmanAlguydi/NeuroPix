const loginForm = document.querySelector("#loginForm");
const registerForm = document.querySelector("#registerForm");

if (loginForm) {
	loginForm.addEventListener("submit", function (event) {
		event.preventDefault();

		const username = document.querySelector("#loginUsername").value.trim();

		if (!username) {
			alert("Please enter your username.");
			return;
		}

		// Temporary navigation until backend authentication is connected.
		window.location.href = "dashboard.html";
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
