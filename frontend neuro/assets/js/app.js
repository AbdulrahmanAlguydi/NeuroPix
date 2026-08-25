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
