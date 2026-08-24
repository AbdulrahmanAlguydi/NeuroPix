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
