// get the form, confirm-box and csrf token
const complaintform = document.querySelector("#complaint-form");
const cccsrf = document.getElementsByName("csrfmiddlewaretoken");
const complaintDialog = document.getElementById("complaintDialog");

// "Complaint" button opens the <dialog> modally
$(".Complaint").click(function onOpen() {
  if (typeof complaintDialog.showModal === "function") {
    complaintDialog.showModal();
  } else {
    alert("The <dialog> API is not supported by this browser");
  }
});

function set_complaint(order_id) {
  let isSubmit = false;
  complaintform.addEventListener("submit", e => {
    e.preventDefault();
    if (isSubmit) {
      return;
    }
    isSubmit = true;
    // value of the complaint
    const complaint_val = $("#complaint").val();

    $.ajax({
      type: "POST",
      url: "/accounts/complaint/",
      data: {
        csrfmiddlewaretoken: cccsrf[0].value,
        order_id: order_id,
        complaint: complaint_val
      }
    });
  });
}
