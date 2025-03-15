function toggleFishList(containerId, buttonId) {
  var container = document.getElementById(containerId);
  var button = document.getElementById(buttonId);
  var parentContainer = container.parentElement;
  
  if (container.style.display === "none") {
    container.style.display = "block";
    button.textContent = "Hide";
    parentContainer.classList.add("blur_group");

    // Get the position of the startLists element
    var rect = container.getBoundingClientRect();
    
    // 10% above
    var offset = window.scrollY + rect.top - window.innerHeight * 0.1;
    window.scrollTo({
      top: offset,
      behavior: "smooth",
    });
  } else {
    parentContainer.classList.remove("blur_group");
    container.style.display = "none";
    button.textContent = "Show";
  }
}
