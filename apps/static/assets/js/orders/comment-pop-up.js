var updateButton = document.getElementById('Comment');
var commentDialog = document.getElementById('CommentDialog');
var outputBox = document.querySelector('output');
var selectEl = document.querySelector('select');
var confirmBtn = document.getElementById('confBtn');

updateButton.addEventListener('click', function onOpen() {
  if (typeof commentDialog.showModal === "function") {
    commentDialog.showModal();
  } else {
    alert("The <dialog> API is not supported by this browser");
  }
});
