document.addEventListener("DOMContentLoaded", function () {

    const filterButtons = document.querySelectorAll(".filter-btn");

    const petCards = document.querySelectorAll(".pet-card-column");

    filterButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const selectedFilter = button.dataset.filter;

            // Update active button
            filterButtons.forEach(function (item) {
                item.classList.remove("active");
            });

            button.classList.add("active");

            // Filter the pet cards
            petCards.forEach(function (card) {

                const petType = card.dataset.petType || "";

                let shouldDisplay = false;

                if (selectedFilter === "all") {

                    shouldDisplay = true;

                } else if (selectedFilter === "other") {

                    shouldDisplay =
                        petType !== "dog" &&
                        petType !== "cat";

                } else {

                    shouldDisplay =
                        petType.includes(selectedFilter);

                }

                card.style.display = shouldDisplay ? "" : "none";

            });

        });

    });

});