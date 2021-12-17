// get the form, confirm-box and csrf token
const commentform = document.querySelector('#comment-form')
const ccsrf = document.getElementsByName('csrfmiddlewaretoken')
const comDialog = document.getElementById("comDialog");

// "Comment" button opens the <dialog> modally
$(".Comment").click(function onOpen() {
  if (typeof comDialog.showModal === "function") {
    comDialog.showModal();
  } else {
    alert("The <dialog> API is not supported by this browser");
  }
});

function commenting(order_id) {
  console.log("hereee");
  let isSubmit = false
  commentform.addEventListener('submit', e => {
    e.preventDefault()
    if (isSubmit) {
      return
    }
    isSubmit = true
    // value of the comment
    const comment_val = $("#comment").val()

    $.ajax({
      type: 'POST',
      url: '/accounts/comment/',
      data: {
        'csrfmiddlewaretoken': ccsrf[0].value,
        'order_id': order_id,
        'comment': comment_val,
      },
    })
  })
}


