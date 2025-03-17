document.querySelectorAll(".fish-card-button").forEach((button) => {
  button.addEventListener("click", function () {
    // Add the 'clicked' class to trigger animation
    this.classList.add("clicked");

    // Remove the class after the animation is done (500ms)
    setTimeout(() => {
      this.classList.remove("clicked");
    }, 500);
  });
});
