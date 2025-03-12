function displaySuggestions(invalidFish, suggestions) {
  const invalidFishList = document.getElementById("invalid-fish-list");
  const suggestionsList = document.getElementById("suggestions-list");
  const suggestionsContainer = document.getElementById("suggestions-container");

  invalidFishList.innerHTML = "";
  suggestionsList.innerHTML = "";

  invalidFish.forEach((fish) => {
    const li = document.createElement("li");
    li.textContent = fish;
    invalidFishList.appendChild(li);
  });

  suggestions.forEach((suggestion) => {
    const li = document.createElement("li");
    li.textContent = suggestion;
    suggestionsList.appendChild(li);
  });

  suggestionsContainer.style.display = "block";
}
