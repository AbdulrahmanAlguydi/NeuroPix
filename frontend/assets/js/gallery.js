const modal = document.querySelector("#modal");
const comparisonBox = document.querySelector("#comparisonBox");
const beforeLayer = document.querySelector("#beforeLayer");
const afterLayer = document.querySelector("#afterLayer");
const afterImage = document.querySelector("#afterImage");
const compareLine = document.querySelector("#compareLine");
const modalAiSign = document.querySelector("#modalAiSign");

let dragging = false;

// Moves the divider and reveals the After image on the right side.
function updateComparison(value) {
  const safeValue = Math.max(0, Math.min(100, value));

  afterLayer.style.clipPath =
    "inset(0 0 0 " + safeValue + "%)";

  compareLine.style.left = safeValue + "%";
}

// Converts the pointer position into a percentage across the image.
function moveDivider(event) {
  const box = comparisonBox.getBoundingClientRect();
  const value = ((event.clientX - box.left) / box.width) * 100;

  updateComparison(value);
}

// Opens the selected example with its Before and After images.
document.querySelectorAll(".gallery-card").forEach(function (card) {
  card.addEventListener("click", function () {
    document.querySelector("#modalTitle").textContent =
      card.dataset.title;

    beforeLayer.src = card.dataset.before;
    afterImage.src = card.dataset.after;

    if (card.dataset.type === "ai") {
      modalAiSign.classList.remove("hidden");
    } else {
      modalAiSign.classList.add("hidden");
    }

    modal.classList.remove("hidden");
    updateComparison(50);
  });
});

// Closes the comparison window.
document.querySelector("#closeModal").addEventListener(
  "click",
  function () {
    modal.classList.add("hidden");
  }
);

// Starts dragging when the mouse or finger is pressed on the image.
comparisonBox.addEventListener("pointerdown", function (event) {
  if (event.pointerType === "mouse" && event.button !== 0) {
    return;
  }

  event.preventDefault();
  dragging = true;
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
