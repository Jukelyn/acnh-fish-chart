function displaySuggestions(invalidFish, suggestions) {
  const invalidFishList = document.getElementById("invalid-fish-list");
  const suggestionsContainer = document.getElementById("suggestions-container");
  const fishDataTextArea = document.getElementById("fish-data");
  const invalidFishText = document.getElementById("invalid-fish-text"); // Get the invalid fish text element

  let userInput = localStorage.getItem("userInput") || "";
  let userInputArray = userInput.split("\n");

  console.log("Initial user input:", userInput);

  userInputArray = userInputArray.filter((item) => item.trim() !== "");

  console.log("Cleaned user input array:", userInputArray);

  invalidFishList.innerHTML = ""; // Clear any previous invalid fish list
  let anyInvalidFishDisplayed = false; // Flag to track invalid fish

  invalidFish.forEach((fish, index) => {
    // Skip invalid fish that have already been ignored
    if (!userInputArray.includes(fish)) {
      console.log("Skipping already ignored fish:", fish);
      return;
    }

    console.log("Processing invalid fish:", fish);

    // Remove the invalid fish from 'userInputArray'
    userInputArray = userInputArray.filter((item) => item !== fish);

    console.log(
      "Updated user input array after removing invalid fish:",
      userInputArray
    );

    const suggestionList = suggestions[index];

    console.log("Suggestions for this invalid fish:", suggestionList);

    const allSuggestionsInUserInput = suggestionList.every((suggestion) =>
      userInputArray.includes(suggestion)
    );
    console.log(
      "Are all suggestions already in the user input?",
      allSuggestionsInUserInput
    );

    if (allSuggestionsInUserInput) {
      // If all suggestions are already in the user input, skip adding it
      userInputArray = userInputArray.filter((item) => item !== fish);
      userInput = userInputArray.join("\n");

      console.log(
        "Updated user input after removing invalid fish (all suggestions present):",
        userInput
      );

      localStorage.setItem("userInput", userInput);
      fishDataTextArea.value = userInput;
      return; // Skip adding invalid fish item to the list
    }

    const li = document.createElement("li");
    li.textContent = fish;

    console.log("Created list item for invalid fish:", li);

    // Add the "Ignore" button next to the invalid fish name
    const ignoreButton = document.createElement("button");
    ignoreButton.textContent = "Ignore";
    ignoreButton.classList.add("ignore_button_container");
    ignoreButton.style.marginLeft = "10px";

    ignoreButton.addEventListener("click", () => {
      console.log("Ignore button clicked for:", fish);

      // Remove the invalid fish from the user input array
      userInputArray = userInputArray.filter((item) => item !== fish);
      userInput = userInputArray.join("\n");

      console.log("Updated user input after ignoring invalid fish:", userInput);

      // Update 'userInput' in localStorage and textarea
      localStorage.setItem("userInput", userInput);
      fishDataTextArea.value = userInput;

      // Remove the invalid fish list item from the display
      li.remove();

      // Re-render suggestions with updated user input
      displaySuggestions(invalidFish, suggestions);
    });

    // Append the "Ignore" button to the invalid fish item
    li.appendChild(ignoreButton);

    // Create the "Did you mean?" text and the suggestions sublist
    const didYouMeanText = document.createElement("p");
    didYouMeanText.textContent = "Did you mean?";
    li.appendChild(didYouMeanText);

    const sublist = document.createElement("ul");

    suggestionList.forEach((suggestion) => {
      console.log("Processing suggestion:", suggestion);

      // Skip suggestions already in the user input list
      if (userInputArray.includes(suggestion)) return;

      const suggestionLi = document.createElement("li");
      suggestionLi.textContent = suggestion;
      suggestionLi.style.cursor = "pointer";

      suggestionLi.addEventListener("click", () => {
        console.log("Suggestion clicked:", suggestion);

        // Add the suggestion to user input and remove the invalid fish
        userInputArray.push(suggestion);
        userInputArray = userInputArray.filter((item) => item !== fish);

        console.log(
          "Updated user input after replacing invalid fish with suggestion:",
          userInputArray
        );

        userInput = userInputArray.join("\n");

        // Update 'userInput' in localStorage
        localStorage.setItem("userInput", userInput);
        fishDataTextArea.value = userInput;

        li.remove();

        // Re-render to reflect
        displaySuggestions(invalidFish, suggestions);
      });

      sublist.appendChild(suggestionLi);
    });

    li.appendChild(sublist);
    invalidFishList.appendChild(li);

    anyInvalidFishDisplayed = true; // There are invalid fish to display
  });

  userInput = userInputArray.join("\n");

  // Update 'userInput' in localStorage without the invalid fish
  localStorage.setItem("userInput", userInput);

  if (userInput) {
    console.log("Final user input:", userInput);
  }

  // Only show the suggestions container if there are invalid fish to display
  if (anyInvalidFishDisplayed) {
    suggestionsContainer.style.display = "flex";
    invalidFishText.style.display = "block";
  } else {
    localStorage.removeItem("userInput");
    suggestionsContainer.style.display = "none";
    invalidFishText.style.display = "none";
  }
}
