function displaySuggestions(invalidFish, suggestions) {
  const invalidFishList = document.getElementById("invalid-fish-list");
  const suggestionsContainer = document.getElementById("suggestions-container");
  const fishDataTextArea = document.getElementById("fish-data");
  const invalidFishText = document.getElementById("invalid-fish-text");

  let userInput = localStorage.getItem("userInput") || "";
  let userInputArray = userInput.split("\n").filter((item) => item.trim() !== "");
  let ignoredFish = JSON.parse(localStorage.getItem("ignoredFish")) || [];

  invalidFishList.innerHTML = "";
  let anyInvalidFishDisplayed = false;

  invalidFish.forEach((fish, index) => {
    if (ignoredFish.includes(fish) || !userInputArray.includes(fish)) {
      console.log("Skipping ignored or already removed fish:", fish);
      return;
    }

    console.log("Processing invalid fish:", fish);

    const suggestionList = suggestions[index];
    const allSuggestionsInUserInput = suggestionList.every((suggestion) => userInputArray.includes(suggestion));

    if (allSuggestionsInUserInput) {
      userInputArray = userInputArray.filter((item) => item !== fish);
      return;
    }

    const li = document.createElement("li");
    li.textContent = fish;

    const ignoreButton = document.createElement("button");
    ignoreButton.textContent = "Ignore";
    ignoreButton.classList.add("ignore_button_container");
    ignoreButton.style.marginLeft = "10px";

    ignoreButton.addEventListener("click", () => {
      console.log("Ignore button clicked for:", fish);
      ignoredFish.push(fish);
      localStorage.setItem("ignoredFish", JSON.stringify(ignoredFish));
      li.remove();
      
      displaySuggestions(invalidFish, suggestions);
    });

    li.appendChild(ignoreButton);

    const didYouMeanText = document.createElement("p");
    didYouMeanText.textContent = "Did you mean?";
    li.appendChild(didYouMeanText);

    const sublist = document.createElement("ul");

    suggestionList.forEach((suggestion) => {
      if (userInputArray.includes(suggestion)) return;

      const suggestionLi = document.createElement("li");
      suggestionLi.textContent = suggestion;
      suggestionLi.style.cursor = "pointer";

      suggestionLi.addEventListener("click", () => {
        userInputArray.push(suggestion);
        userInputArray = userInputArray.filter((item) => item !== fish);
        localStorage.setItem("userInput", userInputArray.join("\n"));
        fishDataTextArea.value = userInputArray.join("\n");
        li.remove();
        displaySuggestions(invalidFish, suggestions);
      });

      sublist.appendChild(suggestionLi);
    });

    li.appendChild(sublist);
    invalidFishList.appendChild(li);

    anyInvalidFishDisplayed = true;
  });

  userInputArray = userInputArray.filter((item) => !ignoredFish.includes(item));
  localStorage.setItem("userInput", userInputArray.join("\n"));
  fishDataTextArea.value = userInputArray.join("\n");

  suggestionsContainer.style.display = anyInvalidFishDisplayed ? "flex" : "none";
  invalidFishText.style.display = anyInvalidFishDisplayed ? "block" : "none";
} 