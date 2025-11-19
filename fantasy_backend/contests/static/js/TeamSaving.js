
document.addEventListener("DOMContentLoaded", function () {
    const saveTeamButton = document.getElementById("saveTeamButton");

    // Fetch team status on page load
    fetch("/api/check-team-status/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (response.ok) {
                return response.json();
            }
            throw new Error("Failed to fetch team status.");
        })
        .then((data) => {
                // Construct URL based on user_id
                let url = "/api/get-saved-team/";
                fetch(url, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then((response) => {
                    if (response.ok) return response.json();
                    throw new Error("Failed to fetch saved team.");
                })
                .then((data) => {
                    // console.log("Fetched data:", data);
                    const current_gameweek= document.getElementById("current_gameweek").textContent.trim();

                    // Filter the players where gameweek is 27
                    const playersInGameweek = data.team.filter(player => player.gameweek === parseInt(current_gameweek,0));

                    // Check if there are any players for the specific gameweek
                    if (playersInGameweek.length > 0) {
                        // Disable the save button if the team already exists
                        saveTeamButton.disabled = true;
                        saveTeamButton.textContent = "Team Saved";
                        saveTeamButton.classList.add("btn-secondary"); // Optional: Update button styling
                        saveTeamButton.classList.remove("btn-primary");

                        // Disable the Auto Pick and Reset buttons
                        autoPickButton.disabled = true;
                        autoPickButton.classList.add("btn-secondary"); // Optional: Update styling
                        autoPickButton.classList.remove("btn-outline-secondary");

                        resetButton.disabled = true;
                        resetButton.classList.add("btn-secondary"); // Optional: Update styling
                        resetButton.classList.remove("btn-outline-secondary");
                    }
                })
                .catch((error) => {
                    console.error("Error loading saved team:", error);
                });

        })
        .catch((error) => {
            console.error("Error fetching team status:", error);
        });

    // Save Team Button Event Listener
    saveTeamButton.addEventListener("click", function () {
        // const pitchPositions = document.querySelectorAll(".position-absolute .player-card-save");
        const pitchPositions = document.querySelectorAll(".player-card-save");
        const teamData = [];
        const teamName = document.getElementById("teamName").textContent.trim();
        const teamId = document.getElementById("teamId").textContent.trim();
        const current_gameweek= document.getElementById("current_gameweek").textContent.trim();

        pitchPositions.forEach((playerCard) => {
            if (playerCard) {
                const positionContainer = playerCard.parentElement; // Get parent container (position-absolute)
                const positionCoordinates = {
                    top: positionContainer.style.top,
                    left: positionContainer.style.left,
                };

                const playerData = {
                    playerid: playerCard.getAttribute("data-playerid"),
                    name: playerCard.getAttribute("data-name"),
                    position: playerCard.getAttribute("data-position"),
                    team: playerCard.getAttribute("data-team") || "Unknown",
                    kickoff: playerCard.getAttribute("data-fixture-time") || "Unknown",
                    formation_name: document.getElementById("formation-select").value,
                    score: parseInt(playerCard.getAttribute("data-score") || "0"),
                    position_coordinates: JSON.stringify(positionCoordinates), // Add coordinates as JSON string
                    image_url: playerCard.getAttribute("data-team_shirt") || "", // Ensure image URL is passed
                };
                teamData.push(playerData);

                // console.log(playerData);
            }
        });


        if (teamData.length === 0) {
            showToast("No players selected to save.", "danger");
            return;
        }

        if (teamData.length !== 15) {
            showToast("Team must have 15 Players.", "danger");
            return;
        }

        // Send the team data to the backend
        fetch("/api/save-team/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ team_name: teamName,team_id: teamId, current_gameweek: current_gameweek, team: teamData }), // Ensure payload matches backend expectation
        })
            .then((response) => {
                // console.log("Response status:", response.status); // Debug log
                if (response.ok) {
                    return response.json();
                }
                throw new Error("Failed to save team.");
            })
            .then((data) => {
                // Show success toast and disable button
                showToast(data.message || "Team saved successfully!", "success");
                saveTeamButton.disabled = true;
                saveTeamButton.textContent = "Team Saved";
                saveTeamButton.classList.add("btn-secondary");
                saveTeamButton.classList.remove("btn-primary");

                // Disable the Auto Pick and Reset buttons
                autoPickButton.disabled = true;
                autoPickButton.classList.add("btn-secondary"); // Optional: Update styling
                autoPickButton.classList.remove("btn-outline-secondary");

                resetButton.disabled = true;
                resetButton.classList.add("btn-secondary"); // Optional: Update styling
                resetButton.classList.remove("btn-outline-secondary");

                // Show the modal
                const leagueOptionsModal = new bootstrap.Modal(document.getElementById("leagueOptionsModal"));
                leagueOptionsModal.show();

                // Redirect to a new page after success
                // window.location.href = "/api/manageteam/"; 
            })
            .catch((error) => {
                console.error(error);
                showToast("Error saving team. Please try again.", "danger");
            });
    });

    const dismissButton = document.getElementById("dismissButton");

    dismissButton.addEventListener("click", function () {
        // Redirect to /api/manageteam/
        window.location.href = "/api/manageteam/";
    });


    // Helper function to get CSRF token
    function getCSRFToken() {
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfTokenElement ? csrfTokenElement.value : "";
    }

    // Helper function to show toast messages
    function showToast(message, type) {
        const toastContainer = document.getElementById("toastContainer");
        if (!toastContainer) {
            console.error("Toast container not found.");
            return;
        }

        const toast = document.createElement("div");
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.role = "alert";
        toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
        toastContainer.appendChild(toast);

        const bootstrapToast = new bootstrap.Toast(toast);
        bootstrapToast.show();

        toast.addEventListener("hidden.bs.toast", () => {
            toastContainer.removeChild(toast);
        });
    }

});