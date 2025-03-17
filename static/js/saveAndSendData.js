const socket = io.connect("http://localhost:5000");

// Send data through WebSocket
function saveAndSendData() {
  const loader = document.getElementById("loader");
  let newData = document.getElementById("fish-data").value.toLowerCase();
  let existingData = localStorage.getItem("userInput");
  let data;

  if (existingData) {
    let existingDataArray = existingData.toLowerCase().split("\n");
    let newDataArray = newData.split("\n");
    let combinedDataArray = [
      ...new Set([...existingDataArray, ...newDataArray]),
    ];
    data = combinedDataArray.join("\n");
  } else {
    let newDataArray = newData.split("\n");
    let uniqueNewData = newDataArray.filter(
      (entry, index, self) => self.indexOf(entry) === index
    );
    data = uniqueNewData.join("\n");
  }

  localStorage.setItem("userInput", data); // Store data in the browser
  console.log("Data saved in browser storage!");

  loader.style.display = "flex";

  // Send data to Python backend via WebSocket
  socket.emit("send_fish_data", data);

  socket.on("receive_suggestions", function (data) {
    console.log("Flask response: ", data);
    loader.style.display = "none";
    if (data.invalid_fish_names && data.suggestions) {
      displaySuggestions(data.invalid_fish_names, data.suggestions);
    } else {
      console.log("No invalid fish names or suggestions found");
    }
  });

  socket.on("fish_data_processed", function (data) {
    console.log("Fish data processed: ", data);
    // Handle the processed data here (e.g., update the UI with uncaught fish, image URL)
  });
}
