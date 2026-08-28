const modal = document.querySelector("#modal");
const editedLayer = document.querySelector("#editedLayer");
const compareLine = document.querySelector("#compareLine");
const compareRange = document.querySelector("#compareRange");

function updateComparison(value) {
  editedLayer.style.width = value + "%";
  compareLine.style.left = value + "%";
}

document.querySelectorAll(".gallery-card").forEach(function (card) {
  card.addEventListener("click", function () {
    modal.classList.remove("hidden");

    document.querySelector("#modalTitle").textContent =
      card.dataset.title;

    // Opens mostly on the edited result.
    compareRange.value = 80;
    updateComparison(80);
  });
});

document.querySelector("#closeModal").addEventListener("click", function () {
  modal.classList.add("hidden");
});

compareRange.addEventListener("input", function () {
  updateComparison(compareRange.value);
});
