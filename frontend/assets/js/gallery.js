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
const editChoiceModal = document.querySelector("#editChoiceModal");
const editChoiceTitle = document.querySelector("#editChoiceTitle");
const closeEditChoiceModal = document.querySelector("#closeEditChoiceModal");
const useOriginalButton = document.querySelector("#useOriginalButton");
const useEditedButton = document.querySelector("#useEditedButton");

let dragging = false;
let selectedGalleryImage = null;
let galleryAction = "edit";

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

function getWorkspaceUrl(imageId, source) {
	return (
		"workspace.html?imageId=" +
		encodeURIComponent(imageId) +
		"&source=" +
		encodeURIComponent(source)
	);
}

function openVersionChoice(image, action) {
	if (!image.modified_url) {
		if (action === "edit") {
			window.location.href = getWorkspaceUrl(image.image_id, "original");
			return;
		}
	}

	selectedGalleryImage = image;
	galleryAction = action;
	const popupLabel = editChoiceModal.querySelector(".eyebrow");
	const popupDescription = editChoiceModal.querySelector("p");

	if (action === "download") {
		popupLabel.textContent = "DOWNLOAD IMAGE";
		popupDescription.textContent = "Download the original upload or the saved edited result.";
		useOriginalButton.textContent = "Download original";
		useEditedButton.textContent = "Download edited";
	} else {
		popupLabel.textContent = "EDIT IMAGE";
		popupDescription.textContent = "Select which version you want to continue editing in Studio.";
		useOriginalButton.textContent = "Use original";
		useEditedButton.textContent = "Use edited";
	}
	useEditedButton.disabled = !image.modified_url;
	editChoiceTitle.textContent = "Choose a version of " + image.title;
	editChoiceModal.classList.remove("hidden");
}

function closeEditChoice() {
	selectedGalleryImage = null;
	editChoiceModal.classList.add("hidden");
}

function chooseEditSource(source) {
	if (!selectedGalleryImage) {
		return;
	}

	if (galleryAction === "download") {
		window.location.href = "/api/gallery/" + selectedGalleryImage.image_id + "/download?source=" + source;
		closeEditChoice();
	} else {
		window.location.href = getWorkspaceUrl(selectedGalleryImage.image_id, source);
	}
}

// Flask renders the cards; JavaScript connects their actions.
document.querySelectorAll(".gallery-card").forEach(function (card) {
	const image = {
		image_id: card.dataset.imageId,
		title: card.dataset.title,
		original_url: card.dataset.originalUrl,
		modified_url: card.dataset.modifiedUrl,
		edit_type: card.dataset.editType,
	};

	card.querySelector(".gallery-card-preview").addEventListener("click", function () {
		openComparison(image.title, image.original_url, image.modified_url, image.edit_type);
	});
	card.querySelector(".gallery-edit").addEventListener("click", function (event) {
		event.preventDefault();
		openVersionChoice(image, "edit");
	});
	card.querySelector(".gallery-download").addEventListener("click", function () {
		openVersionChoice(image, "download");
	});
	card.querySelector(".gallery-delete").addEventListener("click", function () {
		deleteGalleryImage(image.image_id, card);
	});
});

async function deleteGalleryImage(imageId, card) {
	// Ask for confirmation before removing both the database row and S3 files.
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

if (editChoiceModal) {
	closeEditChoiceModal.addEventListener("click", closeEditChoice);
	useOriginalButton.addEventListener("click", function () {
		chooseEditSource("original");
	});
	useEditedButton.addEventListener("click", function () {
		chooseEditSource("edited");
	});
	editChoiceModal.addEventListener("click", function (event) {
		if (event.target === editChoiceModal) {
			closeEditChoice();
		}
	});
}
