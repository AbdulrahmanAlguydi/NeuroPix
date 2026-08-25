const state = {
  user: null,
  imageFile: null,
  originalUrl: "",
  editedUrl: ""
};

// Finds one HTML element using a CSS selector.
function getElement(selector) {

// Finds all HTML elements using a CSS selector.
function getElements(selector) {
  return document.querySelectorAll(selector);
}

// Shows a short message at the bottom of the screen.
function showToast(message) {
  const toast = getElement("#toast");
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2200);
}

// Changes between the landing, login and application views.
function changeView(viewName) {
  getElements(".view").forEach((view) => view.classList.remove("active"));

  if (viewName === "landing") getElement("#landingView").classList.add("active");
  if (viewName === "login" || viewName === "register") {
    getElement("#authView").classList.add("active");
    changeAuthForm(viewName);
  }
  if (viewName === "app") getElement("#appView").classList.add("active");
}

// Switches between the login and registration forms.
function changeAuthForm(formName) {
  getElement("#loginForm").classList.toggle("hidden", formName !== "login");
  getElement("#registerForm").classList.toggle("hidden", formName !== "register");
}

// Opens a page inside the main application.
function openPage(pageName) {
  getElements(".app-page").forEach((page) => page.classList.remove("active"));
  getElement("#" + pageName + "Page").classList.add("active");
}

// Handles the temporary frontend login until the backend is connected.
function loginUser(event) {
  event.preventDefault();
  const username = getElement("#loginUsername").value.trim();
  state.user = { username: username };
  getElement("#usernameText").textContent = username;
  changeView("app");
}

// Handles the temporary registration form until the backend is connected.
function registerUser(event) {
  event.preventDefault();
  const username = getElement("#registerUsername").value.trim();
  state.user = { username: username };
  getElement("#usernameText").textContent = username;
  changeView("app");
}

// Logs the current frontend user out.
function logoutUser() {
  state.user = null;
  changeView("landing");
}

// Checks the selected file and displays only the original image.
function handleImage(file) {
  if (!file) return;

  if (file.type !== "image/jpeg" && file.type !== "image/png") {
    showToast("Only JPG and PNG images are allowed.");
    return;
  }

  const imageUrl = URL.createObjectURL(file);
  const image = new Image();

  image.onload = function () {
    if (image.width > 1920 || image.height > 1080) {
      URL.revokeObjectURL(imageUrl);
      showToast("Maximum resolution is 1920 x 1080.");
      return;
    }

    state.imageFile = file;
    state.originalUrl = imageUrl;
    state.editedUrl = "";
    getElement("#originalPreview").src = imageUrl;
    getElement("#imageInfo").textContent = image.width + " x " + image.height;
    getElement("#originalArea").classList.remove("hidden");
    getElement("#comparisonArea").classList.add("hidden");
    showToast("Image selected.");
  };

  image.src = imageUrl;
}
// Placeholder for sending the selected image to the backend later.
function processImage() {
  if (!state.imageFile) {
    showToast("Choose an image first.");
    return;
  }

  const tool = getElement("#toolSelect").value;
  console.log("Selected backend tool:", tool);
  showToast("Backend processing is not connected yet.");
}

// Displays an edited image after the backend returns its URL.
function showProcessedImage(editedUrl) {
  if (!editedUrl || !state.originalUrl) return;

  state.editedUrl = editedUrl;
  getElement("#compareOriginal").src = state.originalUrl;
  getElement("#compareEdited").src = editedUrl;
  getElement("#originalArea").classList.add("hidden");
  getElement("#comparisonArea").classList.remove("hidden");
  updateComparison(50);
}

// Reveals more or less of the edited image without moving either image.
function updateComparison(value) {
  const hiddenPercent = 100 - Number(value);
  getElement("#compareEdited").style.clipPath = `inset(0 ${hiddenPercent}% 0 0)`;
  getElement("#sliderLine").style.left = value + "%";
}

// Connects the HTML buttons and forms to the functions above.
function setupEvents() {
  getElements("[data-route]").forEach((button) => {
    button.addEventListener("click", () => changeView(button.dataset.route));
  });

  getElements("[data-auth-mode]").forEach((button) => {
    button.addEventListener("click", () => changeAuthForm(button.dataset.authMode));
  });

  getElements("[data-page]").forEach((button) => {
    button.addEventListener("click", () => openPage(button.dataset.page));
  });

  getElement("#loginForm").addEventListener("submit", loginUser);
  getElement("#registerForm").addEventListener("submit", registerUser);
  getElement("#logoutBtn").addEventListener("click", logoutUser);
  getElement("#processBtn").addEventListener("click", processImage);
  getElement("#chooseFileBtn").addEventListener("click", () => getElement("#fileInput").click());

  getElement("#fileInput").addEventListener("change", (event) => {
    handleImage(event.target.files[0]);
  });

  getElement("#compareSlider").addEventListener("input", (event) => {
    updateComparison(event.target.value);
  });
}
// Starts the frontend after the page has loaded.
function startApp() {
  setupEvents();
  changeView("landing");
}

startApp();
