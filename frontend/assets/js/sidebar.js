const logoutLink = document.querySelector(".logout-link");

if (logoutLink) {
	logoutLink.addEventListener("click", async function (event) {
		event.preventDefault();
		try {
			await fetch("/api/auth/logout", { method: "POST" });
		} finally {
			window.location.href = logoutLink.href;
		}
	});
}
