// get all the stars
const one = document.getElementById("first");
const two = document.getElementById("second");
const three = document.getElementById("third");
const four = document.getElementById("fourth");
const five = document.getElementById("fifth");

// get the form, confirm-box and csrf token
const form = document.querySelector("#rate-form");
const confirmBox = document.getElementById("confirm-box");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const favDialog = document.getElementById("favDialog");

// "Score" button opens the <dialog> modally
$(".Score").click(function onOpen() {
  if (typeof favDialog.showModal === "function") {
    favDialog.showModal();
  } else {
    alert("The <dialog> API is not supported by this browser");
  }
});

// color all the stars with less value than the one over which mouse is
const handleStarSelect = size => {
  const children = form.children;
  console.log(children[0]);
  for (let i = 0; i < children.length; i++) {
    if (i <= size) {
      children[i].classList.add("checked");
    } else {
      children[i].classList.remove("checked");
    }
  }
};

// color stars based on the selected star and using function above
const handleSelect = selection => {
  switch (selection) {
    case "first": {
      handleStarSelect(1);
      return;
    }
    case "second": {
      handleStarSelect(2);
      return;
    }
    case "third": {
      handleStarSelect(3);
      return;
    }
    case "fourth": {
      handleStarSelect(4);
      return;
    }
    case "fifth": {
      handleStarSelect(5);
      return;
    }
    default: {
      handleStarSelect(0);
    }
  }
};

// translate ratings into numeric values
const getNumericValue = stringValue => {
  let numericValue;
  if (stringValue === "first") {
    numericValue = 1;
  } else if (stringValue === "second") {
    numericValue = 2;
  } else if (stringValue === "third") {
    numericValue = 3;
  } else if (stringValue === "fourth") {
    numericValue = 4;
  } else if (stringValue === "fifth") {
    numericValue = 5;
  } else {
    numericValue = 0;
  }
  return numericValue;
};

function score(order_id) {
  if (one) {
    const arr = [one, two, three, four, five];

    arr.forEach(item =>
      item.addEventListener("mouseover", event => {
        handleSelect(event.target.id);
      })
    );

    arr.forEach(item =>
      item.addEventListener("click", event => {
        // value of the rating not numeric
        const val = event.target.id;

        let isSubmit = false;
        form.addEventListener("submit", e => {
          e.preventDefault();
          if (isSubmit) {
            return;
          }
          isSubmit = true;
          // value of the rating translated into numeric
          const val_num = getNumericValue(val);

          $.ajax({
            type: "POST",
            url: "/accounts/rate/",
            data: {
              csrfmiddlewaretoken: csrf[0].value,
              order_id: order_id,
              val: val_num
            },
            success: function(response) {
              console.log(response);
              confirmBox.innerHTML = `<h6>Successfully rated with ${response.score}</h6>`;
            },
            error: function(error) {
              console.log(error);
              confirmBox.innerHTML = "<h6>Ops... something went wrong</h6>";
            }
          });
        });
      })
    );
  }
}
