function saveAndSendData() {
  const loader = document.getElementById("loader");
  // Inputted fish
  let newData = document.getElementById("fish-data").value.toLowerCase();
  // Existing fish
  let existingData = localStorage.getItem("userInput");
  let data;
  if (existingData) {
    // Convert existing data to lowercase
    let existingDataArray = existingData.toLowerCase().split("\n");
    let newDataArray = newData.split("\n");
    let combinedDataArray = [
      ...new Set([...existingDataArray, ...newDataArray]),
    ];
    data = combinedDataArray.join("\n");
  } else {
    // Prevent adding duplicate entries if no data exists
    let newDataArray = newData.split("\n");
    let uniqueNewData = newDataArray.filter(
      (entry, index, self) => self.indexOf(entry) === index
    );
    data = uniqueNewData.join("\n");
  }

  localStorage.setItem("userInput", data); // Stores data in the browser
  console.log("Data saved in browser storage!");

  loader.style.display = "flex";
  fetch("/fish-input", {
    // FIXME
    method: "POST",
    headers: {
      "Content-Type": "text/plain",
    },
    body: data, // fish data, split by newlines
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Flask response: ", data);
      loader.style.display = "none";
      if (data.invalid_fish_names && data.suggestions) {
        console.log("Calling displaySuggestions");
        displaySuggestions(data.invalid_fish_names, data.suggestions);
      } else {
        console.log("No invalid fish names or suggestions found");
      }
    })
    .catch((error) => {
      // SyntaxError happens when all entries are valid... or so I hope...
      if (error instanceof SyntaxError) {
        console.error("SyntaxError:", error);
        console.error("This should usually be the index page HTML");
        // window.location.href = "/";
      } else {
        console.error("Error:", error);
      }
    });
}
