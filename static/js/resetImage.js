function resetImage() {
  let existingData = localStorage.getItem("userInput");
  
  if (existingData === null) {
    console.log("There is nothing to reset.");
    return;
  }

  const loader = document.getElementById("loader");
  loader.style.display = "flex";

  fetch("/fish-input/", {
    method: "POST",
    headers: {
      "Content-Type": "text/plain",
    },
    body: "reset",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Successfully reset images:", data);
      loader.style.display = "none";
      window.location.href = "/";
      //   alert(data.status || "Calendars reset!");
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Failed to reset calendars");
    });
}
