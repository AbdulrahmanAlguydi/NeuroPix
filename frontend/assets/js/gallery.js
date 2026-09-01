const modal = document.querySelector("#modal");
const comparisonBox = document.querySelector("#comparisonBox");
const beforeLayer = document.querySelector("#beforeLayer");
const editedLayer = document.querySelector("#editedLayer");
const editedImage = document.querySelector("#editedImage");
const compareLine = document.querySelector("#compareLine");

// Moves the divider and changes how much of the edited image is visible.
function updateComparison(value) {
  const safeValue = Math.max(0, Math.min(100, value));
  editedLayer.style.clipPath = "inset(0 0 0 " + safeValue + "%)";
  compareLine.style.left = safeValue + "%";
}

// Finds the pointer position inside the comparison image.
function moveDivider(event) {
  const box = comparisonBox.getBoundingClientRect();
  const point = event.touches ? event.touches[0] : event;
  const value = ((point.clientX - box.left) / box.width) * 100;
  updateComparison(value);
}

// Opens the comparison window using the image from the selected gallery card.
document.querySelectorAll(".gallery-card").forEach(function (card) {
  card.addEventListener("click", function () {
    const imagePath = card.dataset.image;
    document.querySelector("#modalTitle").textContent = card.dataset.title;
    beforeLayer.src = imagePath;
    editedImage.src = imagePath;
    modal.classList.remove("hidden");
    updateComparison(75);
  });
});

// Closes the comparison window.
document.querySelector("#closeModal").addEventListener("click", function () {
  modal.classList.add("hidden");
});

let dragging = false;

comparisonBox.addEventListener("mousedown", function (event) {
  dragging = true;
  moveDivider(event);
});

document.addEventListener("mousemove", function (event) {
  if (dragging) moveDivider(event);
});

document.addEventListener("mouseup", function () {
  dragging = false;
});

// Touch support for phones and tablets.
comparisonBox.addEventListener("touchstart", function (event) {
  dragging = true;
  moveDivider(event);
}, { passive: true });

comparisonBox.addEventListener("touchmove", function (event) {
  if (dragging) moveDivider(event);
}, { passive: true });

comparisonBox.addEventListener("touchend", function () {
  dragging = false;
});

// Closes the modal when the dark background is clicked.
modal.addEventListener("click", function (event) {
  if (event.target === modal) modal.classList.add("hidden");
});
