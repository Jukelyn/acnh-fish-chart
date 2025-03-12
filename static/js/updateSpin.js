document.getElementById("toggle-spin").addEventListener("click", function () {
  var spinEnabled = localStorage.getItem("spin_enabled") === "true";
  if (spinEnabled) {
    localStorage.setItem("spin_enabled", "false");
  } else {
    localStorage.setItem("spin_enabled", "true");
  }
});
