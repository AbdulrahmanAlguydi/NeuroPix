const standardEditCount = document.querySelector("#standardEditCount");
const aiEditCount = document.querySelector("#aiEditCount");
const recentActivityTitle = document.querySelector("#recentActivityTitle");
const recentActivityMessage = document.querySelector("#recentActivityMessage");
const recentActivityList = document.querySelector("#recentActivityList");

function formatDashboardDate(value) {
	const date = new Date(value);

	if (Number.isNaN(date.getTime())) {
		return "Unknown date";
	}

	return date.toLocaleDateString("en-GB", {
		day: "2-digit",
		month: "2-digit",
		year: "numeric",
	});
}

function getEditTypeLabel(editType) {
	if (editType === "ai") {
		return "AI Edited";
	}

	if (editType === "standard") {
		return "Standard Edit";
	}

	return "Original";
}

function createRecentActivityItem(image) {
	const fileName = image.file_name || "Edited image";
	const item = document.createElement("a");
	item.className = "recent-activity-item";
	item.href = "gallery.html";
	item.setAttribute("aria-label", "Open " + fileName + " in Gallery");

	const thumbnail = document.createElement("img");
	thumbnail.src = image.modified_url || image.original_url;
	thumbnail.alt = fileName;
	item.appendChild(thumbnail);

	const metadata = document.createElement("div");
	metadata.className = "gallery-chips recent-activity-meta";

	const typeChip = document.createElement("span");
	typeChip.className = image.edit_type === "ai" ? "chip ai-chip" : "chip";
	typeChip.textContent = getEditTypeLabel(image.edit_type);
	metadata.appendChild(typeChip);

	const dateChip = document.createElement("span");
	dateChip.className = "chip";
	dateChip.textContent = formatDashboardDate(image.upload_date);
	metadata.appendChild(dateChip);

	item.appendChild(metadata);
	return item;
}

async function loadDashboard() {
	try {
		const response = await fetch("/api/gallery");

		if (response.status === 401) {
			window.location.href = "login.html";
			return;
		}

		if (!response.ok) {
			throw new Error("Dashboard request failed");
		}

		const images = await response.json();
		const standardImages = images.filter(function (image) {
			return image.edit_type === "standard";
		});
		const aiImages = images.filter(function (image) {
			return image.edit_type === "ai";
		});

		standardEditCount.textContent = standardImages.length;
		aiEditCount.textContent = aiImages.length;
		recentActivityList.replaceChildren();

		if (!images.length) {
			recentActivityTitle.textContent = "No activity yet";
			recentActivityMessage.textContent =
				"Process an image in Studio to see it here.";
			return;
		}

		recentActivityTitle.textContent = "Latest edits";
		recentActivityMessage.textContent = "Your three most recent processed images.";
		images.slice(0, 3).forEach(function (image) {
			recentActivityList.appendChild(createRecentActivityItem(image));
		});
	} catch (error) {
		recentActivityTitle.textContent = "Recent activity unavailable";
		recentActivityMessage.textContent = "Could not load your gallery.";
	}
}

loadDashboard();
