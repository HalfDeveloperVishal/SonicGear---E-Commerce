document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.querySelector(".hamburger");
  const navLinks = document.querySelector(".nav-links");

  hamburger.addEventListener("click", function () {
    navLinks.classList.toggle("active");
  });
});

document.getElementById("search-input").addEventListener("input", function () {
  let query = this.value.trim();

  if (query.length > 0) {
    // Send AJAX request to the search view
    fetch(`/search/?q=${query}`)
      .then((response) => response.json())
      .then((data) => {
        let suggestionsList = document.getElementById("suggestions-list");
        suggestionsList.innerHTML = ""; // Clear previous suggestions
        if (data.results.length > 0) {
          suggestionsList.style.display = "block";
          data.results.forEach((item) => {
            let li = document.createElement("li");
            li.innerHTML = `<a href="${item.url}">${item.name}</a>`;
            suggestionsList.appendChild(li);
          });
        } else {
          suggestionsList.style.display = "none";
        }
      });
  } else {
    document.getElementById("suggestions-list").style.display = "none";
  }
});
