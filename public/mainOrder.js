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
  let menu = document.querySelector(".menu-grid");
  let OrderForm = document.querySelector(".order-form");
  let quantity = OrderForm.querySelector("input[name=quantity]").value;
  let selector = OrderForm.querySelector("#selector");
  //HANDLE PRICE
  function handlePrice() {
    let quantity = OrderForm.querySelector("input[name=quantity]").value;
    let selector = document.getElementById("selector");
    let choice = document.getElementById("selector").options.selectedIndex;
    // let theId = selector.value;
    // console.log(selector.value);
    let id = selector.options[choice].value;
    let row = menu.querySelector(`.row[data-id='${id}']`);
    let price = parseInt(row.children[1].innerText);
    let theCost = OrderForm.querySelector(".the-cost");
    let ans = parseFloat(price) * parseFloat(quantity);
    theCost.innerText = "Cost " + ans;
  }
  if (quantity != null) {
    setInterval(handlePrice, 500);
  }

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Handle POST Requests
  OrderForm.addEventListener("submit", (event) => {
    // Stop the default form behavior
    event.preventDefault();
    let action = OrderForm.getAttribute("action");
    let method = OrderForm.getAttribute("method");
    // GET THE ELEMENT VIA /MENU
    let selector = document.getElementById("selector");
    let choice = document.getElementById("selector").options.selectedIndex;
    let id = selector.options[choice].value;
    let data = {};

    data = Object.fromEntries(new FormData(OrderForm).entries());
    data["item"] = id;
    data["status"] = 0;
    console.log(JSON.stringify(data));
    server_request(action, data, method, (response) => {});
  });
  //UPDATE
});
