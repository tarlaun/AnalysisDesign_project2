var commentDialog = document.getElementById('CommentDialog');
$(".Comment").click(function onOpen() {
    if (typeof commentDialog.showModal === "function") {
    commentDialog.showModal();
  } else {
    alert("The <dialog> API is not supported by this browser");
  }
});
