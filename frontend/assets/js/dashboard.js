const standardEditCount = document.querySelector("#standardEditCount");
const aiEditCount = document.querySelector("#aiEditCount");
const recentActivityTitle = document.querySelector("#recentActivityTitle");
const recentActivityMessage = document.querySelector("#recentActivityMessage");
const recentActivityList = document.querySelector("#recentActivityList");
const GALLERY_CACHE_KEY = "neuropixGallery";

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

function createChip(text, className = "chip") {
	const chip = document.createElement("span");
	chip.className = className;
	chip.textContent = text;
	return chip;
}

function createRecentActivityItem(image) {
	let fileName = image.file_name;
	if (!fileName) {
		fileName = "Edited image";
	}

	const item = document.createElement("a");
	item.className = "recent-activity-item";
	item.href = "gallery.html";
	item.setAttribute("aria-label", "Open " + fileName + " in Gallery");

	const thumbnail = document.createElement("img");
	let thumbnailUrl = image.modified_url;
	if (!thumbnailUrl) {
		thumbnailUrl = image.original_url;
	}
	thumbnail.src = thumbnailUrl;
	thumbnail.alt = fileName;

	const metadata = document.createElement("div");
	metadata.className = "gallery-chips recent-activity-meta";

	let typeClass = "chip";
	if (image.edit_type === "ai") {
		typeClass = "chip ai-chip";
	}

	const typeChip = createChip(getEditTypeLabel(image.edit_type), typeClass);
	const dateChip = createChip(formatDashboardDate(image.upload_date));
	metadata.append(typeChip, dateChip);

	item.append(thumbnail, metadata);
	return item;
}

function renderDashboard(images) {
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
		recentActivityMessage.textContent = "Process an image in Studio to see it here.";
		return;
	}

	recentActivityTitle.textContent = "Latest edits";
	recentActivityMessage.textContent = "Your three most recent processed images.";
	images.slice(0, 3).forEach(function (image) {
		recentActivityList.appendChild(createRecentActivityItem(image));
	});
}

async function loadDashboard() {
	// Render cached data first so navigation does not show an empty dashboard.
	const cachedValue = localStorage.getItem(GALLERY_CACHE_KEY);
	let cachedGallery = null;
	if (cachedValue) {
		cachedGallery = JSON.parse(cachedValue);
	}

	if (cachedGallery) {
		renderDashboard(cachedGallery);
	}

	try {
		// The API request refreshes the cache with the account's current gallery.
		const response = await fetch("/api/gallery");
		if (response.status === 401) {
			localStorage.removeItem(GALLERY_CACHE_KEY);
			window.location.href = "login.html";
			return;
		}
		if (!response.ok) {
			throw new Error("Dashboard request failed");
		}

		const images = await response.json();
		localStorage.setItem(GALLERY_CACHE_KEY, JSON.stringify(images));
		renderDashboard(images);
	} catch (error) {
		if (!cachedGallery) {
			recentActivityTitle.textContent = "Recent activity unavailable";
			recentActivityMessage.textContent = "Could not load your gallery.";
		}
	}
}

loadDashboard();
