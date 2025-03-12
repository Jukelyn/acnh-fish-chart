function toggleSpin() {
  var spinEnabled = localStorage.getItem("spin_enabled") === "false";
  localStorage.setItem("spin_enabled", spinEnabled ? "true" : "false");
}
