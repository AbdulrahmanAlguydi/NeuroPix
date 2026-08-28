const state = {
  imageFile: null,
  originalUrl: "",
  editMode: "standard"
};

function getElement(selector) {
  return document.querySelector(selector);
}

// Validates and displays the selected image.
function handleImage(file) {
  if (!file) return;

  if (file.type !== "image/jpeg" && file.type !== "image/png") {
    getElement("#status").textContent = "Only JPG and PNG images are allowed.";
    return;
  }

  if (file.size > 5 * 1024 * 1024) {
    getElement("#status").textContent = "Maximum file size is 5 MB.";
    return;
  }

  const imageUrl = URL.createObjectURL(file);
  const image = new Image();

  image.onload = function () {
    if (image.width > 1920 || image.height > 1080) {
      URL.revokeObjectURL(imageUrl);
      getElement("#status").textContent = "Maximum resolution is 1920 x 1080.";
      return;
    }

    if (state.originalUrl) {
      URL.revokeObjectURL(state.originalUrl);
    }

    state.imageFile = file;
    state.originalUrl = imageUrl;

    getElement("#originalPreview").src = imageUrl;
    getElement("#fileName").textContent = file.name;
    getElement("#imageInfo").textContent = image.width + " x " + image.height;

    getElement("#uploadZone").classList.add("hidden");
    getElement("#previewArea").classList.remove("hidden");
    getElement("#status").textContent = "Image ready.";
  };

  image.src = imageUrl;
}

// Changes between Standard and AI edit settings.
function setEditMode(mode) {
  state.editMode = mode;

  const standardMode = mode === "standard";

  getElement("#standardControls").classList.toggle("hidden", !standardMode);
  getElement("#aiControls").classList.toggle("hidden", standardMode);

  getElement("#standardBtn").classList.toggle("active", standardMode);
  getElement("#aiBtn").classList.toggle("active", !standardMode);

  getElement("#modeText").textContent =
    standardMode ? "Standard Edits" : "AI Edits";
}

// Collects Standard parameters for the future backend request.
function getStandardSettings() {
  return {
    cropWidth: getElement("#cropWidth").value,
    cropHeight: getElement("#cropHeight").value,
    rotation: getElement("#rotation").value,
    brightness: getElement("#brightness").value,
    contrast: getElement("#contrast").value,
    exposure: getElement("#exposure").value,
    blur: getElement("#blur").value,
    sharpness: getElement("#sharpness").value,
    grayscale: getElement("#grayscale").checked
  };
}

// Collects AI parameters for the future backend request.
function getAiSettings() {
  return {
    generativeModification: getElement("#generatePrompt").value.trim(),
    backgroundManipulation: getElement("#backgroundPrompt").value.trim(),
    enhancement: getElement("#enhancePrompt").value.trim(),
    upscaling: getElement("#upscale").value
  };
}

// Prepares the selected settings without processing the image in the browser.
function processImage() {
  if (!state.imageFile) {
    getElement("#status").textContent = "Choose an image first.";
    return;
  }

  const settings =
    state.editMode === "standard"
      ? getStandardSettings()
      : getAiSettings();

  console.log("Edit mode:", state.editMode);
  console.log("Settings for backend:", settings);

  getElement("#status").textContent =
    "Settings are ready. Backend processing is not connected yet.";
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
