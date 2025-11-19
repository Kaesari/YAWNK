
    // Global Variables
    let allPlayers = []; // Store all players fetched from the API
    let filteredPlayers = []; // Players after applying search and filter
    let paginatedPlayers = []; // Players for the current page
    const pageSize = 10; // Players per page
    let currentPage = 1;
    let totalPages = 1;

    const tableBodies = {
            Goalkeepers: document.getElementById("goalkeepersTableBody"),
            Defenders: document.getElementById("defendersTableBody"),
            Midfielders: document.getElementById("midfieldersTableBody"),
            Forwards: document.getElementById("forwardsTableBody"),
    };
        
    const tables = {
            Goalkeepers: document.getElementById("goalkeepersTable"),
            Defenders: document.getElementById("defendersTable"),
            Midfielders: document.getElementById("midfieldersTable"),
            Forwards: document.getElementById("forwardsTable"),
    };



    // Update the table with players for the current page
    const updateTable = () => {
        Object.values(tableBodies).forEach((tableBody) => (tableBody.innerHTML = "")); // Clear all tables

        // Sort the players by price in descending order (highest to lowest)
        // const sortedPlayers = filteredPlayers.sort((a, b) => b.price - a.price);

        // Get players for the current page
        const startIndex = (currentPage - 1) * pageSize;
        const endIndex = startIndex + pageSize;
        paginatedPlayers = filteredPlayers.slice(startIndex, endIndex);

        const sortedPlayers = paginatedPlayers.sort((a, b) => b.price - a.price);

        let playerCount = 0;

        sortedPlayers.forEach((player) => {
            // data-playerid="${selectedPlayer.id}"
            // console.log(player)
            playerCount++;
            const row = `
                <tr class="player-selection-row" 
                    data-name="${player.name}" 
                    data-image="${player.team_shirt}" 
                    data-team_shirt="${player.team_shirt}"
                    data-position="${player.position}" 
                    data-playerid="${player.id}"
                    data-price="${player.price}"
                    data-fixture="${player.fixture}"
                    data-form="${player.form || 'N/A'}"
                    data-tsb="${player.tsb || '0%'}"
                    data-team="${player.team}" 
                    data-teamlogo="${player.teamLogo}" 
                    data-fixture-team1="${player.fixture_data.team1}"
                    data-fixture-team1logo="${player.fixture_data.team1Logo}"
                    data-fixture-team2="${player.fixture_data.team2}"
                    data-fixture-team2logo="${player.fixture_data.team2Logo}"
                    data-fixture-time="${player.fixture_data.time}">
                    <td class="text-start ps-4">
                        <div class="d-flex align-items-center">
                            <img src="${player.team_shirt}" 
                                 alt="${player.name}" 
                                 class="me-3 rounded-circle" 
                                 style="width: 20px; height: 20px;" 
                                 onerror="this.onerror=null; this.src='{% static 'images/default3.png' %}';">
                            <div>
                                <span class="fw-bold" style="font-size: 0.6rem;">${player.name}</span>
                            </div>
                        </div>
                    </td>
                    <td><span class="badge text-bg-warning" style="font-size: 0.6rem; color: white;">${player.fixture}</span></td>
                    <td class="text-center fw-bold" style="font-size: 0.6rem;">${player.total_points}</td>
                    <td class="text-center fw-bold" style="font-size: 0.6rem;">£${player.price}m</td>
                </tr>`;

            const tableBody = tableBodies[player.position];
            if (tableBody) tableBody.innerHTML += row;
        });

        // Update player count and pagination info
        playerCountButton.textContent = `${playerCount} players shown`;
        paginationInfo.textContent = `${currentPage} of ${totalPages}`;
    };

    // Update pagination button states
    const updatePaginationButtons = () => {
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages || totalPages === 0;
    };

    // Toggle visibility of tables based on view filter
    const toggleTables = (selectedView) => {
        Object.keys(tables).forEach((position) => {
            if (selectedView === "All" || selectedView === position) {
                tables[position].style.display = "table"; // Show the table
            } else {
                tables[position].style.display = "none"; // Hide the table
            }
        });
    };

    // Apply search and view filters
    const applyFilters = (selectedView = viewFilter.value) => {
        const searchQuery = searchInput.value.toLowerCase();
        // const selectedView = viewFilter.value;

        // Filter all players based on search and view
        filteredPlayers = allPlayers.filter((player) => {
            const matchesSearch = player.name.toLowerCase().includes(searchQuery);
            const matchesView = selectedView === "All" || player.position === selectedView;
            return matchesSearch && matchesView;
        });

        // Reset pagination and update table
        totalPages = Math.ceil(filteredPlayers.length / pageSize);
        currentPage = 1;
        updateTable();
        updatePaginationButtons();
        toggleTables(selectedView); // Update table visibility
    };

    document.addEventListener("DOMContentLoaded", function () {
        // DOM Elements
        const playerCountButton = document.getElementById("playerCountButton");
        const prevButton = document.getElementById("prevButton");
        const nextButton = document.getElementById("nextButton");
        const paginationInfo = document.getElementById("paginationInfo");
        const searchInput = document.getElementById("searchInput");
        const viewFilter = document.getElementById("viewFilter");

        // Fetch all players
        const fetchAllPlayers = async () => {
            try {
                // Show loading state
                Object.values(tableBodies).forEach((tableBody) => {
                    tableBody.innerHTML = `<tr><td colspan="4" class="text-center">Loading players...</td></tr>`;
                });
                playerCountButton.textContent = "Loading players...";

                // Fetch players
                const response = await fetch(`/api/get-all-players/`); // Replace with your endpoint for fetching all players
                const data = await response.json();

                if (response.ok && data.players) {
                    allPlayers = data.players; // Store all players globally
                    filteredPlayers = [...allPlayers]; // Initially, all players are included
                    totalPages = Math.ceil(filteredPlayers.length / pageSize);
                    currentPage = 1;

                    // Show the first page of results
                    updateTable();
                    updatePaginationButtons();
                } else {
                    throw new Error("Failed to load players.");
                }
            } catch (error) {
                console.error("Error fetching players:", error);
                Object.values(tableBodies).forEach((tableBody) => {
                    tableBody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Failed to load players.</td></tr>`;
                });
                playerCountButton.textContent = "Failed to load players.";
            }
        };


        // Event listeners for search and dropdown
        searchInput.addEventListener("input", () => {
            applyFilters();
        });

        viewFilter.addEventListener("change", () => {
            applyFilters();
        });

        // Event listeners for pagination buttons
        prevButton.addEventListener("click", () => {
            if (currentPage > 1) {
                currentPage--;
                updateTable();
                updatePaginationButtons();
            }
        });

        nextButton.addEventListener("click", () => {
            if (currentPage < totalPages) {
                currentPage++;
                updateTable();
                updatePaginationButtons();
            }
        });

        // Initial fetch of all players
        fetchAllPlayers();
    });

