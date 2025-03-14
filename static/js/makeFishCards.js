function fetchFishData(fishName, containerId) {
  fetch(`/fish-info/${fishName}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error(`Fish not found: ${fishName}`);
        return;
      }

      const fishCard = document.createElement("div");
      fishCard.classList.add("fish-card");

      const fishImage = document.createElement("img");
      fishImage.src = data.image;
      fishImage.alt = data.name;

      const fishNameElement = document.createElement("div");
      fishNameElement.textContent = data.name;
      fishNameElement.classList.add("fish-card-info");

      const fishPrice = document.createElement("div");
      fishPrice.innerHTML = `Price: ${data.sellPrice} Bells`;
      fishPrice.classList.add("fish-card-info");

      const fishLocation = document.createElement("div");
      fishLocation.innerHTML = `Location: ${data.location}`;
      fishLocation.classList.add("fish-card-info");

      const fishSize = document.createElement("div");
      fishSize.innerHTML = `Size: ${data.size}`;
      fishSize.classList.add("fish-card-info");

      const fishTime = document.createElement("div");
      fishTime.innerHTML = `Time Available: ${data.time}`;
      fishTime.classList.add("fish-card-info");

      const nhMonths = document.createElement("div");
      nhMonths.innerHTML = `NH Months:<br>${data.nhMonths
        .map((month, index) => (month ? index + 1 : ""))
        .filter(Boolean)
        .join(", ")}`;
      nhMonths.classList.add("fish-card-info");

      const shMonths = document.createElement("div");
      shMonths.innerHTML = `SH Months:<br>${data.shMonths
        .map((month, index) => (month ? index + 1 : ""))
        .filter(Boolean)
        .join(", ")}`;
      shMonths.classList.add("fish-card-info");

      fishCard.append(
        fishImage,
        fishNameElement,
        fishPrice,
        fishLocation,
        fishSize,
        fishTime,
        nhMonths,
        shMonths
      );

      document.getElementById(containerId).appendChild(fishCard);
    })
    .catch((error) => {
      console.error("Error fetching fish data:", error);
    });
}

// Reusable function to fetch data for each fish in the list
function fetchFishForSection(fishList, containerId) {
  fishList.forEach((fishName) => {
    fetchFishData(fishName, containerId);
  });
}

let allFish = JSON.parse(document.getElementById('fish-data').getAttribute('data-fish-list-json'));
let uncaughtFish = JSON.parse(document.getElementById('fish-data').getAttribute('data-uncaught-fish-json'));

// should be sorted, but making sure
allFish = allFish.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));
uncaughtFish = uncaughtFish.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));

console.log(allFish);
console.log(uncaughtFish);

fetchFishForSection(allFish, "all_fish_list_container");
fetchFishForSection(uncaughtFish, "uncaught_list_container");
