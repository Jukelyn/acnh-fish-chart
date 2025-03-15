function updateFishCards() {
  console.log("Updated fish cards to new hemisphere.");

  // Clear existing content in the containers before re-rendering
  const allFishContainer = document.getElementById("all_fish_list_container");
  const uncaughtFishContainer = document.getElementById(
    "uncaught_list_container"
  );

  allFishContainer.innerHTML = ""; // Clear the list
  uncaughtFishContainer.innerHTML = ""; // Clear the list

  // Re-fetch and display fish data
  fetchFishForSection(allFish, "all_fish_list_container");
  fetchFishForSection(uncaughtFish, "uncaught_list_container");
}
