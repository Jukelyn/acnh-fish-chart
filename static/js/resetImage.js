function resetImage() {
  let existingData = localStorage.getItem("userInput");

  if (existingData === null) {
    const popup = document.getElementById("reset-popup");
    popup.style.display = "flex";
    console.log("There is nothing to reset.");
    console.log("Reset popup displayed.");
    setTimeout(() => {
      popup.style.display = "none";
    }, 2500);
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
