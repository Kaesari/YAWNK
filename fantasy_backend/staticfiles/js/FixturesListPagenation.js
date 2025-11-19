
document.addEventListener("DOMContentLoaded", function () {
    const fixtureContainer = document.getElementById("fixtureContainer");
    const prevButton = document.getElementById("fixtures-prev-button");
    const nextButton = document.getElementById("fixtures-next-button");
    const currentPageSpan = document.getElementById("fixtures-current-page");
    const totalPagesSpan = document.getElementById("fixtures-total-pages");

    // Ensure TEAM_SHIRTS is available in JavaScript
    const TEAM_SHIRTS = {
        "Arsenal": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t3.png" },
        "Aston Villa": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t7.png" },
        "Bournemouth": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t91.png" },
        "Brentford": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t94.png" },
        "Brighton": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t36.png" },
        "Chelsea": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t8.png" },
        "Crystal Palace": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t31.png" },
        "Everton": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t11.png" },
        "Fulham": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t54.png" },
        "Ipswich": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t40.png" },
        "Leicester": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t13.png" },
        "Liverpool": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t14.png" },
        "Man City": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t43.png" },
        "Man Utd": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t1.png" },
        "Newcastle": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t4.png" },
        "Nott'm Forest": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t17.png" },
        "Southampton": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t20.png" },
        "Spurs": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t6.png" },
        "West Ham": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t21.png" },
        "Wolves": { "logo": "https://resources.premierleague.com/premierleague/badges/70/t39.png" }
    };

    // Function to update fixtures dynamically
    const updateFixtures = (page) => {
        fetch(`/api/teamselection/?page=${page}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" },
        })
            .then((response) => response.json())
            .then((data) => {
                // console.log(data);
                // Update fixtures content
                let html = "";
                for (const day of data.matches) {
                    html += `<h5 class="fw-bold text-dark mt-4">${day.date}</h5>`;
                    html += '<div class="timeline mt-3">';
                    for (const match of day.matches) {
                        // Get team names
                        const homeTeamName = match.home_team.name;
                        const awayTeamName = match.away_team.name;

                        // Get logos from TEAM_SHIRTS dictionary
                        const homeTeamLogo = TEAM_SHIRTS[homeTeamName]?.logo || "default_logo.png";
                        const awayTeamLogo = TEAM_SHIRTS[awayTeamName]?.logo || "default_logo.png";

                        html += `
                        <div class="d-flex align-items-center mb-3 bg-white rounded p-2 shadow-sm">
                            <div class="me-2 text-center">
                                <span class="fw-bold">${match.formatted_time}</span>
                                <p class="text-muted small">${match.formatted_date}</p>
                            </div>
                            <div class="flex-grow-1 d-flex justify-content-center align-items-center">
                                <div class="d-flex align-items-center me-3">
                                    <img src="${homeTeamLogo}" 
                                        alt="${match.home_team.name}" 
                                        class="img-fluid"
                                        style="height: 24px; width: 24px; margin-right: 8px;">
                                    <span>${match.home_team.name}</span>
                                </div>
                                <span class="fw-bold mx-3">vs</span>
                                <div class="d-flex align-items-center ms-3">
                                    <span>${match.away_team.name}</span>
                                    <img src="${awayTeamLogo}" 
                                        alt="${match.away_team.name}" 
                                        class="img-fluid"
                                        style="height: 24px; width: 24px; margin-left: 8px;">
                                </div>
                            </div>
                        </div>`;
                    }
                    html += "</div>";
                }
                fixtureContainer.innerHTML = html;

                // Update pagination
                currentPageSpan.textContent = data.current_page;
                totalPagesSpan.textContent = data.total_pages;
                prevButton.disabled = !data.has_previous;
                nextButton.disabled = !data.has_next;
            })
            .catch((error) => console.error("Error fetching fixtures:", error));
    };

    // Event listeners for pagination buttons
    prevButton.addEventListener("click", () => {
        const currentPage = parseInt(currentPageSpan.textContent);
        if (currentPage > 1) updateFixtures(currentPage - 1);
    });

    nextButton.addEventListener("click", () => {
        const currentPage = parseInt(currentPageSpan.textContent);
        const totalPages = parseInt(totalPagesSpan.textContent);
        if (currentPage < totalPages) updateFixtures(currentPage + 1);
    });

    // Initial fetch for the first page
    updateFixtures(1);
});