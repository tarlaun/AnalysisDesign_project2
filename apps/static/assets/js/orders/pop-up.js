var updateButton = document.getElementById("Score");
var favDialog = document.getElementById("favDialog");
var outputBox = document.querySelector("output");
var selectEl = document.querySelector("select");
var confirmBtn = document.getElementById("confirmBtn");

// "Score" button opens the <dialog> modally
updateButton.addEventListener("click", function onOpen() {
  if (typeof favDialog.showModal === "function") {
    favDialog.showModal();
  } else {
    alert("The <dialog> API is not supported by this browser");
  }
});
