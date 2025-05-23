function showPopup() {
  const popup = document.getElementById("flying-popup");
  popup.style.display = "flex";

  setTimeout(() => {
    popup.style.display = "none";
  }, 5000);
}

let lastCallTime = 0;

function toggleHemisphere() {
  const now = Date.now();
  if (now - lastCallTime < 1000) { // Anti-spam 1s cooldown
    showPopup()
    console.log("Please wait before switching hemispheres again.");
    return;
  }

  lastCallTime = now;

  var imageElement = document.getElementById("image");
  var currentHemisphere = document.getElementById("hemisphereButton").value;
  var newHemisphere = currentHemisphere === "NH" ? "SH" : "NH";
  var newImageSrc =
    currentHemisphere === "NH"
      ? "static/images/SH_spawning_calendar.png"
      : "static/images/NH_spawning_calendar.png";

  imageElement.style.opacity = "0.5";
  setTimeout(() => {
    imageElement.src = newImageSrc;
    imageElement.style.opacity = "1";
  }, 800); // match CSS transition, see css rules for `img`

  document.getElementById("hemisphereButton").value = newHemisphere;
  document.getElementById("image").src = newImageSrc;
  var svgElement = document.getElementById("hemisphereSvg");
  svgElement.style.transition = "transform 0.6s ease-in";
  var currentRotation = svgElement.style.transform.match(/rotate\((\d+)deg\)/);
  var currentRotationValue = currentRotation ? parseInt(currentRotation[1]) : 0;
  var additionalRotation = 180;
  svgElement.style.transform = `rotate(${
    currentRotationValue + additionalRotation
  }deg)`;

  localStorage.setItem("lastHemisphere", newHemisphere);
  console.log("Updated Hemisphere to:", newHemisphere);
  localStorage.setItem("imageSrc", newImageSrc);
  console.log("Updated imageSrc to:", newImageSrc);

  // Update fish cards
  updateFishCards();
}
