const sidebarUsername = document.querySelector("#sidebarUsername");
const logoutLink = document.querySelector(".logout-link");
const savedUsername = localStorage.getItem("neuropixUsername");

// Show the cached username immediately, then refresh it from the backend below.
if (sidebarUsername && savedUsername) {
	sidebarUsername.textContent = savedUsername;
}

if (sidebarUsername) {
	fetch("/api/auth/me")
		.then(function (response) {
			if (response.status === 401) {
				localStorage.removeItem("neuropixUsername");
				localStorage.removeItem("neuropixGallery");
				window.location.href = "login.html";
				return null;
			}

			if (!response.ok) {
				throw new Error("Could not load the username");
			}

			return response.json();
		})
		.then(function (data) {
			if (data) {
				sidebarUsername.textContent = data.username;
				localStorage.setItem("neuropixUsername", data.username);
			}
		})
		.catch(function () {
			sidebarUsername.textContent = "Unknown user";
		});
}

if (logoutLink) {
	logoutLink.addEventListener("click", async function (event) {
		event.preventDefault();
		// Clear cached page data so the next account cannot see old values.
		localStorage.removeItem("neuropixUsername");
		localStorage.removeItem("neuropixGallery");

		try {
			await fetch("/api/auth/logout", { method: "POST" });
		} finally {
			window.location.href = logoutLink.href;
		}
	});
}
