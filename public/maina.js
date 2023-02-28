document.addEventListener("DOMContentLoaded", () => {
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Define the 'request' function to handle interactions with the server
  function server_request(url, data = {}, verb, callback) {
    return fetch(url, {
      credentials: "same-origin",
      method: verb,
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((response) => {
        if (callback) callback(response);
      })
      .catch((error) => console.error("Error:", error));
  }

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // References to frequently accessed elements
  let main = document.querySelector("main");
  let menu = document.querySelector(".menu-grid");
  let menuGrid = document.querySelector(".form-grid");
  let addMenuForm = document.querySelector(".post-menu");
  let UpdateMenuForm = document.querySelector(".edit-menu");
  let deleteMenuForm = document.querySelector(".remove-menu");
  let OrderForm = document.querySelector(".order-form");

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  let messages = document.querySelectorAll("status-button");
  for (var i = 0; i < messages.length; i++) {
    if (messages[i].innerText === "0") {
      messages[i].style.background = "red";
    } else {
      messages[i].style.background = "green";
    }
  }
  //
  // Handle POST Requests
  addMenuForm.addEventListener("submit", (event) => {
    // Stop the default form behavior
    event.preventDefault();
    let action = addMenuForm.getAttribute("action");
    let method = addMenuForm.getAttribute("method");
    let data = Object.fromEntries(new FormData(addMenuForm).entries());
    // GET THE ELEMENT VIA /MENU
    server_request(action, data, method, (response) => {
      let ans = document.createElement("div");
      ans.className = data["name"];
      // Update the content for the corresponding html element
      // var parsed_obj = JSON.parse(my_json);
      ans.innerHTML =
        "<h4>Item: " +
        response["id"] +
        "<h4>Item: " +
        data["name"] +
        "</h4><h4> Cost: " +
        data["price"] +
        "</h4>";
      menu.appendChild(ans);
    });
  });
  //HANDLE TOGGLE
  document.addEventListener("click", (event) => {
    // Open edit form
    console.log("clck");
    if (event.target.classList.contains("status-button")) {
      console.log("GOOD");
      let ans = 0;
      let row = event.target.closest(".order-row");
      if (row.children[3].getAttribute("data-status") == 0) {
        row.children[3].style.background = "green";
        ans = 1;
      } else {
        row.children[3].style.background = "red";
        ans = 0;
      }
      let the_id = row.children[3].getAttribute("data-id");
      let data = { item_id: id, status: ans };
      server_request(
        `/editorder/${the_id}`,
        data,
        "PUT",
        function (response) {}
      );
    }
  });
  //UPDATE
  UpdateMenuForm.addEventListener("submit", (event) => {
    event.preventDefault();
    let id = UpdateMenuForm.querySelector("input[name=item_id]").value;
    const name = UpdateMenuForm.querySelector("input[name=name]").value;
    const price = UpdateMenuForm.querySelector("input[name=price]").value;
    let data = Object.fromEntries(new FormData(UpdateMenuForm).entries());
    server_request(`/editmenu/${id}`, data, "PUT", function (response) {
      if (response.success) {
        let row = menu.querySelector(`.row[data-id='${id}']`);
        // row.remove();
        row.children[1].innerText = "food: " + name;
        row.children[2].innerText = "price " + price;
      }
    });
  });
  //DELETE
  deleteMenuForm.addEventListener("submit", (event) => {
    event.preventDefault();
    let id = deleteMenuForm.querySelector("input[name=item_id]").value;
    server_request(
      `/deletemenu/${id}`,
      { item_id: id },
      "DELETE",
      function (response) {
        if (response.success) {
          let row = menu.querySelector(`.row[data-id='${id}']`);
          row.remove();
        }
      }
    );
  });
});
