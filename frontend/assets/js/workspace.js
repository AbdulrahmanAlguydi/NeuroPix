// Stores the selected image and current editing mode.
const state = {
	imageFile: null,
	originalUrl: "",
	editMode: "standard",
};

// Finds an element on the page using a CSS selector.
function getElement(selector) {
	return document.querySelector(selector);
}
function showUploadError(title, message) {
  getElement("#uploadErrorTitle").textContent = title;
  getElement("#uploadErrorMessage").textContent = message;
  getElement("#uploadError").classList.remove("hidden");
}

function clearUploadError() {
  getElement("#uploadError").classList.add("hidden");
}
// Validates and displays the selected image.
function handleImage(file) {
  if (!file) return;

  clearUploadError();

  // Checks if the file is JPG or PNG.
  if (file.type !== "image/jpeg" && file.type !== "image/png") {
    showUploadError(
      "File type is not supported.",
      "Only JPG and PNG images are allowed."
    );

    getElement("#status").textContent = "";
    return;
  }

  // Checks if the file is larger than 5 MB.
  if (file.size > 5 * 1024 * 1024) {
    showUploadError(
      "File is too large.",
      "Maximum file size is 5 MB."
    );

    getElement("#status").textContent = "";
    return;
  }

  const imageUrl = URL.createObjectURL(file);
  const image = new Image();

  image.onload = function () {

    // Checks if the image resolution is larger than 1920 x 1080.
    if (image.width > 1920 || image.height > 1080) {
      URL.revokeObjectURL(imageUrl);

      showUploadError(
        "Image resolution is too large.",
        "Maximum allowed resolution is 1920 × 1080 pixels."
      );

      getElement("#status").textContent = "";
      return;
    }

    // Removes the old image URL if another image was selected before.
    if (state.originalUrl) {
      URL.revokeObjectURL(state.originalUrl);
    }

    state.imageFile = file;
    state.originalUrl = imageUrl;

    // Displays information about the selected image.
    getElement("#originalPreview").src = imageUrl;
    getElement("#fileName").textContent = file.name;
    getElement("#imageInfo").textContent =
      image.width + " x " + image.height;

    // Hides the upload box and shows the image preview.
    getElement("#uploadZone").classList.add("hidden");
    getElement("#previewArea").classList.remove("hidden");

    clearUploadError();
    getElement("#status").textContent = "Image ready.";
  };

  image.src = imageUrl;
}
// Switches between Standard and AI controls.
function setEditMode(mode) {
	state.editMode = mode;

	const standardMode = mode === "standard";

	getElement(".mode-toggle").classList.toggle("ai-selected", !standardMode);

	getElement("#standardControls").classList.toggle("hidden", !standardMode);

	getElement("#aiControls").classList.toggle("hidden", standardMode);

	getElement("#standardBtn").classList.toggle("active", standardMode);

	getElement("#aiBtn").classList.toggle("active", !standardMode);
}

// Collects Standard parameters for a future backend request.
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

// Collects AI parameters for a future backend request.
function getAiSettings() {
	return {
		generativeModification: getElement("#generatePrompt").value.trim(),

		backgroundManipulation: getElement("#backgroundPrompt").value.trim(),

		enhancement: getElement("#enhancePrompt").value.trim(),

		upscaling: getElement("#upscale").value,
	};
}

// Prepares the settings that will later be sent to the backend.
function processImage() {
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

	console.log("Edit mode:", state.editMode);
	console.log("Settings for backend:", settings);

	getElement("#status").textContent =
		"Settings are ready. Backend processing is not connected yet.";
}

// Shows the current value beside a slider.
function connectRange(inputId, valueId, suffix) {
	const input = getElement(inputId);
	const output = getElement(valueId);

	function updateValue() {
		output.textContent = input.value + suffix;
	}

	input.addEventListener("input", updateValue);
	updateValue();
}

// Gets the main upload elements.
const uploadZone = getElement("#uploadZone");
const fileInput = getElement("#fileInput");

// Opens the file picker when Choose Image is clicked.
getElement("#chooseFileBtn").addEventListener("click", function () {
	fileInput.click();
});

// Opens the file picker when Replace Image is clicked.
getElement("#replaceBtn").addEventListener("click", function () {
	fileInput.click();
});

// Handles an image selected from the file picker.
fileInput.addEventListener("change", function (event) {
	handleImage(event.target.files[0]);
});

// Allows an image to be dragged over the upload area.
uploadZone.addEventListener("dragover", function (event) {
	event.preventDefault();
	uploadZone.classList.add("dragging");
});

// Removes the drag effect when the image leaves the area.
uploadZone.addEventListener("dragleave", function () {
	uploadZone.classList.remove("dragging");
});

// Handles an image dropped into the upload area.
uploadZone.addEventListener("drop", function (event) {
	event.preventDefault();

	uploadZone.classList.remove("dragging");
	handleImage(event.dataTransfer.files[0]);
});

// Switches to Standard editing mode.
getElement("#standardBtn").addEventListener("click", function () {
	setEditMode("standard");
});

// Switches to AI editing mode.
getElement("#aiBtn").addEventListener("click", function () {
	setEditMode("ai");
});

// Prepares the selected settings for processing.
getElement("#processBtn").addEventListener("click", processImage);

// Connects each slider to the value shown beside it.
connectRange("#cropWidth", "#cropWidthValue", "%");
connectRange("#cropHeight", "#cropHeightValue", "%");
connectRange("#brightness", "#brightnessValue", "%");
connectRange("#contrast", "#contrastValue", "%");
connectRange("#exposure", "#exposureValue", "%");
connectRange("#saturation", "#saturationValue", "%");
connectRange("#blur", "#blurValue", "");
connectRange("#sharpness", "#sharpnessValue", "%");
connectRange("#grayscale", "#grayscaleValue", "%");
