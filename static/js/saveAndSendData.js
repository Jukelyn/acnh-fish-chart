function saveAndSendData() {
  let newData = document.getElementById("fishData").value;
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
    data = newData;
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
        displaySuggestions(data.invalid_fish_names, data.suggestions);
      }
    })
    .catch((error) => {
      // SyntaxError happens when all entries are valid... or so I hope...
      if (error instanceof SyntaxError) {
        console.error("SyntaxError:", error);
        window.location.href = "/";
      } else {
        console.error("Error:", error);
      }
    });
}
