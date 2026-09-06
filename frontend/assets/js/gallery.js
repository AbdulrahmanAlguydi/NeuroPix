const modal = document.querySelector("#modal");
const comparisonBox = document.querySelector("#comparisonBox");
const beforeLayer = document.querySelector("#beforeLayer");
const afterLayer = document.querySelector("#afterLayer");
const afterImage = document.querySelector("#afterImage");
const compareLine = document.querySelector("#compareLine");
const modalAiSign = document.querySelector("#modalAiSign");
const compareTags = document.querySelectorAll(".compare-tag");
const comparisonHelp = document.querySelector(".comparison-help");
const galleryGrid = document.querySelector("#galleryGrid");
const galleryStatus = document.querySelector("#galleryStatus");

let dragging = false;

// Moves the divider and reveals the After image on the right side.
function updateComparison(value) {
	const safeValue = Math.max(0, Math.min(100, value));

	afterLayer.style.clipPath = "inset(0 0 0 " + safeValue + "%)";

	compareLine.style.left = safeValue + "%";
}

// Converts the pointer position into a percentage across the image.
function moveDivider(event) {
	const box = comparisonBox.getBoundingClientRect();
	const value = ((event.clientX - box.left) / box.width) * 100;

	updateComparison(value);
}

// Opens an image pair in the comparison slider.
function openComparison(title, beforeUrl, afterUrl, type) {
	document.querySelector("#modalTitle").textContent = title;

	beforeLayer.src = beforeUrl;

	const hasComparison = Boolean(afterUrl);
	comparisonBox.classList.toggle("single-image", !hasComparison);
	afterLayer.classList.toggle("hidden", !hasComparison);
	compareLine.classList.toggle("hidden", !hasComparison);
	comparisonHelp.classList.toggle("hidden", !hasComparison);
	compareTags.forEach(function (tag) {
		tag.classList.toggle("hidden", !hasComparison);
	});

	if (hasComparison) {
		afterImage.src = afterUrl;
	} else {
		afterImage.removeAttribute("src");
	}

	if (type === "ai") {
		modalAiSign.classList.remove("hidden");
	} else {
		modalAiSign.classList.add("hidden");
	}

	modal.classList.remove("hidden");

	if (hasComparison) {
		updateComparison(50);
	}
}

function formatGalleryDate(value) {
	if (!value) {
		return "Unknown date";
	}

	const date = new Date(value);
	return Number.isNaN(date.getTime())
		? value
		: date.toLocaleDateString("en-GB", {
				day: "2-digit",
				month: "2-digit",
				year: "numeric",
		  });
}

function getGalleryTitle(image) {
	return image.file_name || "Image #" + image.image_id;
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

function createGalleryCard(image) {
	const title = getGalleryTitle(image);
	const card = document.createElement("article");
	card.className = "gallery-card";

	const previewButton = document.createElement("button");
	previewButton.className = "gallery-card-preview";
	previewButton.type = "button";
	previewButton.setAttribute("aria-label", "Open " + title);

	const thumb = document.createElement("div");
	thumb.className = "gallery-thumb";

	const imageElement = document.createElement("img");
	imageElement.src = image.modified_url || image.original_url;
	imageElement.alt = title;
	thumb.appendChild(imageElement);

	if (image.edit_type === "ai") {
		const aiSign = document.createElement("span");
		aiSign.className = "gallery-ai-icon";
		aiSign.title = "AI edited";
		aiSign.setAttribute("aria-label", "AI edited");
		aiSign.textContent = "✦";
		thumb.appendChild(aiSign);
	}

	const info = document.createElement("div");
	info.className = "gallery-info";

	const titleElement = document.createElement("strong");
	titleElement.className = "gallery-title";
	titleElement.textContent = title;
	titleElement.title = image.file_name || title;
	info.appendChild(titleElement);

	const chips = document.createElement("div");
	chips.className = "gallery-chips";
	const typeChip = document.createElement("span");
	typeChip.className = image.edit_type === "ai" ? "chip ai-chip" : "chip";
	typeChip.textContent = getEditTypeLabel(image.edit_type);
	chips.appendChild(typeChip);

	const dateChip = document.createElement("span");
	dateChip.className = "chip";
	dateChip.textContent = formatGalleryDate(image.upload_date);
	chips.appendChild(dateChip);

	const infoRow = document.createElement("div");
	infoRow.className = "gallery-info-row";
	infoRow.appendChild(chips);

	const deleteButton = document.createElement("button");
	deleteButton.className = "gallery-delete";
	deleteButton.type = "button";
	deleteButton.setAttribute("aria-label", "Delete " + title);
	deleteButton.title = "Delete " + title;
	const trashIcon = document.createElement("span");
	trashIcon.className = "trash-icon";
	trashIcon.setAttribute("aria-hidden", "true");
	trashIcon.innerHTML =
		'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
		'<path d="M3 6h18"></path>' +
		'<path d="M8 6V4h8v2"></path>' +
		'<path d="M19 6l-1 14H6L5 6"></path>' +
		'<path d="M10 11v5"></path>' +
		'<path d="M14 11v5"></path>' +
		"</svg>";
	deleteButton.appendChild(trashIcon);
	deleteButton.addEventListener("click", function () {
		deleteGalleryImage(image.image_id, card);
	});
	infoRow.appendChild(deleteButton);

	info.appendChild(infoRow);
	previewButton.appendChild(thumb);

	previewButton.addEventListener("click", function () {
		openComparison(title, image.original_url, image.modified_url, image.edit_type);
	});

	card.appendChild(previewButton);
	card.appendChild(info);
	return card;
}

async function deleteGalleryImage(imageId, card) {
	if (!window.confirm("Delete this image?")) {
		return;
	}

	const response = await fetch("/api/gallery/" + imageId, { method: "DELETE" });

	if (response.status === 401) {
		window.location.href = "login.html";
		return;
	}

	if (!response.ok) {
		if (galleryStatus) {
			galleryStatus.textContent = "Could not delete this image.";
		}
		return;
	}

	card.remove();
	if (galleryGrid && galleryGrid.children.length === 0 && galleryStatus) {
		galleryStatus.textContent = "No images yet. Process an image in Studio to see it here.";
	}
}

async function loadGallery() {
	if (!galleryGrid) {
		return;
	}

	try {
		const response = await fetch("/api/gallery");

		if (response.status === 401) {
			window.location.href = "login.html";
			return;
		}

		if (!response.ok) {
			throw new Error("Gallery request failed");
		}

		const images = await response.json();
		galleryGrid.replaceChildren();

		if (!images.length) {
			galleryStatus.textContent = "No images yet. Process an image in Studio to see it here.";
			return;
		}

		images.forEach(function (image) {
			galleryGrid.appendChild(createGalleryCard(image));
		});
		galleryStatus.textContent = "Your saved images.";
	} catch (error) {
		galleryStatus.textContent = "Could not load the gallery.";
	}
}

// The workspace also uses this slider for newly processed images.
if (modal && comparisonBox) {
	// Closes the comparison window.
	document.querySelector("#closeModal").addEventListener("click", function () {
		modal.classList.add("hidden");
	});

	// Starts dragging when the mouse or finger is pressed on the image.
	comparisonBox.addEventListener("pointerdown", function (event) {
		if (comparisonBox.classList.contains("single-image")) {
			return;
		}

		if (event.pointerType === "mouse" && event.button !== 0) {
			return;
		}

		event.preventDefault();
		dragging = true;
		comparisonBox.setPointerCapture(event.pointerId);
		moveDivider(event);
	});

	// Keeps moving the divider while the pointer is held down,
	// even if the pointer moves outside the image for a moment.
	window.addEventListener("pointermove", function (event) {
		if (!dragging) {
			return;
		}

		event.preventDefault();
		moveDivider(event);
	});

	// Stops dragging only when the pointer is released.
	window.addEventListener("pointerup", function () {
		dragging = false;
	});

	window.addEventListener("pointercancel", function () {
		dragging = false;
	});

	// Prevents the browser from trying to drag the image itself.
	comparisonBox.addEventListener("dragstart", function (event) {
		event.preventDefault();
	});

	// Closes the modal when the dark background is clicked.
	modal.addEventListener("click", function (event) {
		if (event.target === modal) {
			modal.classList.add("hidden");
		}
	});
}

loadGallery();
