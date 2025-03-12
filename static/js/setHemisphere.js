function setHemisphere(hemisphere) {
  var imageSrc =
    hemisphere === "NH"
      ? "static/images/NH_spawning_calendar.png"
      : "static/images/SH_spawning_calendar.png";
  document.getElementById("hemisphereButton").value = hemisphere;
  document.getElementById("image").src = imageSrc;
  var svgElement = document.getElementById("hemisphereSvg");
  svgElement.style.transition = "transform 0.6s ease-in";
  svgElement.style.transform = `rotate(${hemisphere === "NH" ? 90 : 270}deg)`;
}
