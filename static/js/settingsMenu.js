const settingsMenu = document.querySelector(".settings-menu");

const offScreenMenu = document.querySelector(".settings-menu-options");

settingsMenu.addEventListener("click", () => {
  settingsMenu.classList.toggle("active");
  settingsMenu.style.backgroundColor = "unset";
  offScreenMenu.classList.toggle("active");
});
