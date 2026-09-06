const modal = document.querySelector("#modal");
const comparisonBox = document.querySelector("#comparisonBox");
const beforeLayer = document.querySelector("#beforeLayer");
const afterLayer = document.querySelector("#afterLayer");
const afterImage = document.querySelector("#afterImage");
const compareLine = document.querySelector("#compareLine");
const modalAiSign = document.querySelector("#modalAiSign");
const compareTags = document.querySelectorAll(".compare-tag");
const comparisonHelp = document.querySelector(".comparison-help");

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

// Opens the selected example with its Before and After images.
document.querySelectorAll(".gallery-card").forEach(function (card) {
	card.addEventListener("click", function () {
		openComparison(
			card.dataset.title,
			card.dataset.before,
			card.dataset.after,
			card.dataset.type
		);
	});
});

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
