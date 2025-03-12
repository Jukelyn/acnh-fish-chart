function toggleFishList(containerId, buttonId) {
  var button = document.getElementById(buttonId);
  var container = document.getElementById(containerId);
  if (container.style.display === "none") {
    container.style.display = "block";
    button.textContent = "Hide";
  } else {
    container.style.display = "none";
    button.textContent = "Show";
  }
}
