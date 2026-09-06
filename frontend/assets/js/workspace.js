// Keep the current image and processing mode in one small state object.
const state = {
	imageFile: null,
	originalUrl: "",
	processedUrl: "",
	editMode: "standard",
};

function getElement(selector) {
	return document.querySelector(selector);
}

function getProcessedFileName() {
	let name = "neuropix";
	if (state.imageFile) {
		name = state.imageFile.name;
	}

	const stem = name.replace(/\.[^/.]+$/, "");
	let extension = "jpg";
	if (state.editMode === "ai") {
		extension = "png";
	}

	return stem + "-processed." + extension;
}

function showUploadError(title, message) {
	getElement("#uploadErrorTitle").textContent = title;
	getElement("#uploadErrorMessage").textContent = message;
	getElement("#uploadError").classList.remove("hidden");
	getElement("#status").textContent = "";
}

function clearUploadError() {
	getElement("#uploadError").classList.add("hidden");
}

function requireLogin() {
	alert("Please log in first.");
	window.location.href = "login.html";
}

async function uploadToBackend(file) {
	const formData = new FormData();
	formData.append("image", file);

	const response = await fetch("/api/upload", {
		method: "POST",
		body: formData,
	});
	const data = await response.json();

	if (response.ok) {
		return true;
	}
	if (response.status === 401) {
		requireLogin();
		return false;
	}

	let message = data.error;
	if (!message) {
		message = "Please try again.";
	}
	showUploadError("Upload failed.", message);
	return false;
}

function handleImage(file) {
	if (!file) {
		return;
	}

	clearUploadError();

	if (file.type !== "image/jpeg" && file.type !== "image/png") {
		showUploadError("File type is not supported.", "Only JPG and PNG images are allowed.");
		return;
	}

	if (file.size > 5 * 1024 * 1024) {
		showUploadError("File is too large.", "Maximum file size is 5 MB.");
		return;
	}

	const imageUrl = URL.createObjectURL(file);
	const image = new Image();

	image.onload = async function () {
		let maxWidth = 1920;
		let maxHeight = 1080;
		if (image.width < image.height) {
			maxWidth = 1080;
			maxHeight = 1920;
		}

		if (image.width > maxWidth || image.height > maxHeight) {
			URL.revokeObjectURL(imageUrl);
			showUploadError(
				"Image resolution is too large.",
				"Maximum allowed resolution is 1920 × 1080 for landscape images or 1080 × 1920 for portrait images."
			);
			return;
		}

		if (state.originalUrl) {
			URL.revokeObjectURL(state.originalUrl);
		}

		state.imageFile = file;
		state.originalUrl = imageUrl;
		state.processedUrl = "";
		getElement("#originalPreview").src = imageUrl;
		getElement("#processedPreview").removeAttribute("src");
		getElement("#downloadBtn").removeAttribute("href");
		getElement("#processedArea").classList.add("hidden");
		getElement("#fileName").textContent = file.name;
		getElement("#imageInfo").textContent = image.width + " x " + image.height;
		getElement("#uploadZone").classList.add("hidden");
		getElement("#previewArea").classList.remove("hidden");

		getElement("#status").textContent = "Uploading...";
		const uploaded = await uploadToBackend(file);
		if (uploaded) {
			getElement("#status").textContent = "Image ready.";
		} else {
			getElement("#status").textContent = "";
		}
	};

	image.src = imageUrl;
}

function setEditMode(mode) {
	state.editMode = mode;
	const standard = mode === "standard";

	getElement(".mode-toggle").classList.toggle("ai-selected", !standard);
	getElement("#standardControls").classList.toggle("hidden", !standard);
	getElement("#aiControls").classList.toggle("hidden", standard);
	getElement("#standardBtn").classList.toggle("active", standard);
	getElement("#aiBtn").classList.toggle("active", !standard);
}

function getStandardSettings() {
	return {
		cropWidth: getElement("#cropWidth").value,
		cropHeight: getElement("#cropHeight").value,
		rotation: getElement("#rotation").value,
		brightness: getElement("#brightness").value,
		contrast: getElement("#contrast").value,
		exposure: getElement("#exposure").value,
		saturation: getElement("#saturation").value,
		blur: getElement("#blur").value,
		sharpness: getElement("#sharpness").value,
		grayscale: getElement("#grayscale").value,
	};
}

function getAiSettings() {
	return {
		generativeModification: getElement("#generatePrompt").value.trim(),
		backgroundManipulation: getElement("#backgroundPrompt").value.trim(),
		enhancement: getElement("#enhancePrompt").value.trim(),
		upscaling: getElement("#upscale").value,
	};
}

async function processImage() {
	if (!state.imageFile) {
		getElement("#status").textContent = "Choose an image first.";
		return;
	}

	let settings;
	if (state.editMode === "standard") {
		settings = getStandardSettings();
	} else {
		settings = getAiSettings();
	}
	getElement("#status").textContent = "Processing...";

	const response = await fetch("/api/process", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ editMode: state.editMode, settings: settings }),
	});
	const data = await response.json();

	if (!response.ok) {
		if (response.status === 401) {
			requireLogin();
			return;
		}
		let message = data.error;
		if (!message) {
			message = "Processing failed.";
		}
		getElement("#status").textContent = message;
		return;
	}

	if (data.result && data.result.processedUrl) {
		state.processedUrl = data.result.processedUrl;
		getElement("#processedPreview").src = state.processedUrl;
		getElement("#downloadBtn").href = "/api/download";
		getElement("#downloadBtn").download = getProcessedFileName();
		getElement("#processedArea").classList.remove("hidden");
	}

	getElement("#status").textContent = "Image processed successfully!";
}

function connectRange(inputId, valueId, suffix) {
	const input = getElement(inputId);
	const output = getElement(valueId);

	function updateValue() {
		output.textContent = input.value + suffix;
	}

	input.addEventListener("input", updateValue);
	updateValue();
}

const uploadZone = getElement("#uploadZone");
const fileInput = getElement("#fileInput");

getElement("#chooseFileBtn").addEventListener("click", function () {
	fileInput.click();
});

getElement("#replaceBtn").addEventListener("click", function () {
	fileInput.click();
});

fileInput.addEventListener("change", function (event) {
	handleImage(event.target.files[0]);
});

uploadZone.addEventListener("dragover", function (event) {
	event.preventDefault();
	uploadZone.classList.add("dragging");
});

uploadZone.addEventListener("dragleave", function () {
	uploadZone.classList.remove("dragging");
});

uploadZone.addEventListener("drop", function (event) {
	event.preventDefault();
	uploadZone.classList.remove("dragging");
	handleImage(event.dataTransfer.files[0]);
});

getElement("#standardBtn").addEventListener("click", function () {
	setEditMode("standard");
});

getElement("#aiBtn").addEventListener("click", function () {
	setEditMode("ai");
});

getElement("#processBtn").addEventListener("click", processImage);

function showImageComparison() {
	if (!state.originalUrl) {
		return;
	}

	let title = "Selected image";
	let editType = "";
	if (state.processedUrl) {
		title = "Image comparison";
		editType = state.editMode;
	}

	openComparison(title, state.originalUrl, state.processedUrl, editType);
}

getElement("#originalPreviewButton").addEventListener("click", showImageComparison);
getElement("#processedPreviewButton").addEventListener("click", showImageComparison);

getElement("#downloadBtn").addEventListener("click", function (event) {
	if (!state.processedUrl) {
		event.preventDefault();
		return;
	}

	event.preventDefault();
	window.open(state.processedUrl, "_blank", "noopener,noreferrer");

	const downloadLink = document.createElement("a");
	downloadLink.href = "/api/download";
	downloadLink.download = getElement("#downloadBtn").download;
	document.body.appendChild(downloadLink);
	downloadLink.click();
	downloadLink.remove();
});

connectRange("#cropWidth", "#cropWidthValue", "%");
connectRange("#cropHeight", "#cropHeightValue", "%");
connectRange("#brightness", "#brightnessValue", "%");
connectRange("#contrast", "#contrastValue", "%");
connectRange("#exposure", "#exposureValue", "%");
connectRange("#saturation", "#saturationValue", "%");
connectRange("#blur", "#blurValue", "");
connectRange("#sharpness", "#sharpnessValue", "%");
connectRange("#grayscale", "#grayscaleValue", "%");
