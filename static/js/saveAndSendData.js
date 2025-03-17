function saveAndSendData() {
  const loader = document.getElementById("loader");

  // Inputted fish
  let newData = document.getElementById("fish-data").value.toLowerCase();

  // Existing fish in localStorage
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
    let uniqueNewData = [...new Set(newDataArray)];
    data = uniqueNewData.join("\n");
  }

  // Store in localStorage
  localStorage.setItem("userInput", data);
  console.log("Data saved in browser storage!");

  loader.style.display = "flex";

  // Using FormData to send fish data
  const formData = new FormData();
  formData.append("fish-data", data);

  fetch("/fish-input/", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      loader.style.display = "none";

      // Handle non-JSON responses
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        return response.json();
      } else {
        return response.text(); // Fallback for debugging
      }
    })
    .then((data) => {
      console.log("Flask response: ", data);

      if (data.invalid_fish_names && data.suggestions) {
        console.log("Calling displaySuggestions");
        displaySuggestions(data.invalid_fish_names, data.suggestions);
      } else {
        if (typeof data === "string" && data.includes("<html")) {
          console.log("Received an HTML page instead of JSON!");
          return; // Go to page
        }
      }
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    });
}
