function saveAndSendData() {
  let newData = document.getElementById("fish-data").value;
  let existingData = localStorage.getItem("userInput");
  let data;

  if (existingData) {
    let existingDataArray = existingData.split("\n");
    let newDataArray = newData.split("\n");
    let combinedDataArray = [
      ...new Set([...existingDataArray, ...newDataArray]),
    ];
    data = combinedDataArray.join("\n");
  } else {
    // Prevent adding duplicate entries if no data exists
    let newDataArray = newData.split("\n");
    let uniqueNewData = newDataArray.filter((entry, index, self) => self.indexOf(entry) === index);
    data = uniqueNewData.join("\n");
  }

  localStorage.setItem("userInput", data); // Stores data in the browser
  console.log("Data saved in browser storage!");

  fetch("/process", {
    method: "POST",
    headers: {
      "Content-Type": "text/plain",
    },
    body: data,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Flask response: ", data);
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
        // ADD LOADING SCREEN HERE
        console.error("SyntaxError:", error);
        console.error("This should usually be the index page HTML");
        // window.location.href = "/";
      } else {
        console.error("Error:", error);
      }
    });
}
