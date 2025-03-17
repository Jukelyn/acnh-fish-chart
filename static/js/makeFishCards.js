let sizes = {};
sizes["1"] = "Tiny";
sizes["2"] = "Small";
sizes["3"] = "Medium";
sizes["4"] = "Large";
sizes["5"] = "Very Large";
sizes["6"] = "Huge";

function mapMonthsToString(months) {
  // Sort the months in ascending order
  months.sort((a, b) => a - b);

  let result = [];
  let start = months[0];
  let end = months[0];

  for (let i = 1; i < months.length; i++) {
    if (months[i] === end + 1) {
      end = months[i];
    } else {
      // Otherwise, store the current range or single month
      if (start === end) {
        result.push(formatMonth(start));
      } else {
        result.push(formatMonth(start) + " - " + formatMonth(end));
      }
      // Start a new range
      start = months[i];
      end = months[i];
    }
  }

  // Push the last range or single month
  if (start === end) {
    result.push(formatMonth(start));
  } else {
    result.push(formatMonth(start) + " - " + formatMonth(end));
  }

  // Combine the ranges with ' & ' if there are multiple ranges
  return result.join(" & ");
}

function formatMonth(month) {
  const monthNames = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  return monthNames[month - 1];
}

// // Example usage
// console.log(mapMonthsToString([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])); // "All Year"
// console.log(mapMonthsToString([1, 2, 3, 4, 5, 9, 10, 11, 12])); // "Jan - May & Sep - Dec"
// console.log(mapMonthsToString([1, 2, 3, 4])); // "Jan - Apr"

function fetchFishData(fishName, containerId) {
  var currentHemisphere = localStorage.getItem("lastHemisphere");
  fetch(`/fish-info/${fishName}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
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
      fishNameElement.classList.add("fish-card-info", "fish-card-info-name");

      const fishTime = document.createElement("div");
      fishTime.innerHTML = `${data.time}`;
      fishTime.classList.add("fish-card-info", "fish-card-info-time");

      const fishRarity = document.createElement("div");
      fishRarity.innerHTML = `Rarity: [TBA]`;
      fishRarity.classList.add("fish-card-info", "fish-card-info-rarity");

      const fishPrice = document.createElement("div");
      fishPrice.innerHTML = `${data.sellPrice} Bells`;
      fishPrice.classList.add("fish-card-info", "fish-card-info-price");

      const fishSize = document.createElement("div");
      fishSize.innerHTML = `Size: ${sizes[data.size]}`;
      fishSize.classList.add("fish-card-info", "fish-card-info-size");

      const fishLocation = document.createElement("div");
      fishLocation.innerHTML = `${data.location}`;
      fishLocation.classList.add("fish-card-info", "fish-card-info-location");

      const nhMonths = document.createElement("div");
      nhMonths.innerHTML = `NH Months:<div style="text-align: center;">${mapMonthsToString(
        data.nhMonths
          .map((month, index) => (month ? index + 1 : ""))
          .filter(Boolean)
      )}</div>`;
      nhMonths.classList.add("fish-card-info", "fish-card-info-months");

      const shMonths = document.createElement("div");
      shMonths.innerHTML = `SH Months:<div style="text-align: center;">${mapMonthsToString(
        data.shMonths
          .map((month, index) => (month ? index + 1 : ""))
          .filter(Boolean)
      )}</div>`;
      shMonths.classList.add("fish-card-info", "fish-card-info-months");

      if (currentHemisphere === "NH") {
        nhMonths.style.display = "unset";
        shMonths.style.display = "none";
      } else {
        nhMonths.style.display = "none";
        shMonths.style.display = "unset";
      }

      const fishButton = document.createElement("button");
      fishButton.innerHTML =
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16"><path d="M13.485 3.379a1 1 0 0 1 1.415 1.415l-8 8a1 1 0 0 1-1.415 0l-4-4a1 1 0 0 1 1.415-1.415L6 10.085l7.485-7.486z"/></svg>';
      fishButton.classList.add("fish-card-button");
      fishButton.type = "submit";
      fishButton.addEventListener("click", function () {
        console.log("Check clicked for %s", data.name);
      });

      fishCard.append(
        fishImage,
        fishNameElement,
        fishRarity,
        fishPrice,
        fishTime,
        fishLocation,
        fishSize,
        nhMonths,
        shMonths,
        fishButton
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

let allFish = JSON.parse(
  document.getElementById("fish-data").getAttribute("data-fish-list-json")
);
let uncaughtFish = JSON.parse(
  document.getElementById("fish-data").getAttribute("data-uncaught-fish-json")
);

// should be sorted, but making sure
allFish = allFish.sort((a, b) =>
  a.toLowerCase().localeCompare(b.toLowerCase())
);
uncaughtFish = uncaughtFish.sort((a, b) =>
  a.toLowerCase().localeCompare(b.toLowerCase())
);

// console.log(allFish);
// console.log(uncaughtFish);
fetchFishForSection(allFish, "all_fish_list_container");
fetchFishForSection(uncaughtFish, "uncaught_list_container");
