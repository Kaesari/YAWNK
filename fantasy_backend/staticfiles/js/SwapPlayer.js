
let playerToReplace = null;
let replacementPlayer = null;
let isSwitchModeActive = false; // We use this to control switching mode

// Function to highlight selected position
function highlightPosition(positionDiv, color = 'green') {
    selectedPositionReplace = null;
    document.querySelectorAll(".pitch-position").forEach((div) => {
        div.style.border = ""; // Reset all
    });
    if (positionDiv) {
        positionDiv.style.border = `2px dashed ${color}`;
        selectedPositionElement = positionDiv;
    }
}

// Function called when a player on pitch is clicked
function onPlayerCardClick(playerCardElement) {
    playerIdRemoved = playerCardElement.getAttribute("data-playerid");
    teamPlayerIdRemoved = playerCardElement.getAttribute("data-team");
    RemovedPlayerPrice = playerCardElement.getAttribute("data-price");

    showPlayerModal(
        playerCardElement.getAttribute("data-name"), 
        playerCardElement.getAttribute("data-playerid"),
        playerCardElement.getAttribute("data-image"),
        playerCardElement.getAttribute("data-position"),
        playerCardElement.getAttribute("data-price") || "£0.0m",
        playerCardElement.getAttribute("data-form") || "N/A",
        playerCardElement.getAttribute("data-tsb") || "0%",
        playerCardElement.getAttribute("data-team") || "Unknown Team",
        playerCardElement.getAttribute("data-teamlogo"),
        {
            team1: playerCardElement.getAttribute("data-fixture-team1") || "Team A",
            team1Logo: playerCardElement.getAttribute("data-fixture-team1logo"),
            team2: playerCardElement.getAttribute("data-fixture-team2") || "Team B",
            team2Logo: playerCardElement.getAttribute("data-fixture-team2logo"),
            time: playerCardElement.getAttribute("data-fixture-time") || "TBD"
        }
    );
}

// Setup event listeners on pitch players
document.querySelectorAll(".pitch-position").forEach((positionDiv) => {
    positionDiv.addEventListener("click", function () {
        if (!isSwitchModeActive) {
            const playerCardElement = this.querySelector(".player-card-save");
            console.log(playerCardElement);
            if (playerCardElement) {
                console.log('Inside');
                console.log(playerCardElement);
                // onPlayerCardClick(playerCardElement); // Open modal
                selectedPositionElement = this; // Remember clicked element
            }
        }
    });
});

// "Switch" Button inside Modal
document.getElementById("switchOutButton").addEventListener("click", function () {
    if (ReplaceLocationChanger === 1) {
        document.getElementById("playerModal").style.display = "none"; // Close modal
        
        if (!playerToReplace) {
            // First click (store the player to replace)
            if (selectedPositionElement) {
                playerToReplace = {
                    element: selectedPositionElement,
                    playerId: playerIdRemoved,
                    team: teamPlayerIdRemoved,
                    price: RemovedPlayerPrice
                };
                highlightPosition(selectedPositionElement, 'red');
                showToast("Now select a replacement player", "info");
                isSwitchModeActive = true; // Start switch mode
            } else {
                showToast("No player selected.", "warning");
            }
        } else if (playerToReplace && !replacementPlayer) {
            // Second click (store the replacement player)
            if (selectedPositionElement) {
                replacementPlayer = {
                    element: selectedPositionElement,
                    playerId: playerIdRemoved,
                    team: teamPlayerIdRemoved,
                    price: RemovedPlayerPrice
                };
                // Perform swap
                swapPlayers(playerToReplace, replacementPlayer);
                
                // Reset all
                playerToReplace = null;
                replacementPlayer = null;
                isSwitchModeActive = false;
                highlightPosition(null);
                showToast("Players swapped successfully!", "success");
            } else {
                showToast("No replacement player selected.", "warning");
            }
        }
    }
});

// Function to swap players on the pitch
function swapPlayers(playerA, playerB) {
    const cardA = playerA.element.querySelector(".player-card-save");
    const cardB = playerB.element.querySelector(".player-card-save");

    if (!cardA || !cardB) {
        console.error("Player cards not found!");
        return;
    }

    const clonedCardA = cardA.cloneNode(true);
    const clonedCardB = cardB.cloneNode(true);

    // Swap in the DOM
    playerA.element.replaceChild(clonedCardB, cardA);
    playerB.element.replaceChild(clonedCardA, cardB);

    // ⭐⭐⭐ Now reattach the click listeners
    attachPlayerCardClick(clonedCardA);
    attachPlayerCardClick(clonedCardB);

    selectedPositionElement = null; // optional reset
}

// Helper function to attach modal opening
function attachPlayerCardClick(playerCardElement) {
    playerCardElement.addEventListener("click", function () {
        playerIdRemoved = this.getAttribute("data-playerid");
        teamPlayerIdRemoved = this.getAttribute("data-team");
        RemovedPlayerPrice = this.getAttribute("data-price");

        // console.log(playerCardElement);

        showPlayerModal1(
            this.getAttribute("data-name"), 
            this.getAttribute("data-playerid"),
            this.getAttribute("data-image"),
            this.getAttribute("data-position"),
            this.getAttribute("data-price") || "£0.0m",
            this.getAttribute("data-form") || "N/A",
            this.getAttribute("data-tsb") || "0%",
            this.getAttribute("data-team") || "Unknown Team",
            this.getAttribute("data-teamlogo"),
            {
                team1: this.getAttribute("data-fixture-team1") || "Team A",
                team1Logo: this.getAttribute("data-fixture-team1logo"),
                team2: this.getAttribute("data-fixture-team2") || "Team B",
                team2Logo: this.getAttribute("data-fixture-team2logo"),
                time: this.getAttribute("data-fixture-time") || "TBD"
            }
        );
    });
}

// Function to show modal with player details
function showPlayerModal1(name, playerId, image, position, price, form, tsb, team, teamLogo, fixture) {
    const modal = document.getElementById("playerModal");
    const makeCaptainButton = document.getElementById("makeCaptainButton");
    const makeViceCaptainButton = document.getElementById("makeViceCaptainButton");
    const transferOutButton = document.getElementById("transferOutButton");

    transferOutButton.style.display = "block";
    switchOutButton.style.display = "block";
    makeCaptainButton.style.display = "none";  // Hide Make Captain button
    makeViceCaptainButton.style.display = "none";  // Hide Make Vice Captain button
    // console.log(fixture);
    // Check if modal exists
    if (!modal) {
        console.error("Modal element not found!");
        return;
    }

    // Set player details
    document.getElementById("modalPlayerName").textContent = name;
    document.getElementById("modalPlayerImage").src = image;
    document.getElementById("modalPlayerImage").onerror = function () {
        this.onerror = null;
        this.src = "https://via.placeholder.com/80"; // Fallback image
    };
    document.getElementById("modalPlayerPosition").textContent = position;
    document.getElementById("modalPlayerPrice").textContent = "£" + price + "m";
    document.getElementById("modalPlayerForm").textContent = form;
    document.getElementById("modalPlayerTSB").textContent = tsb;
    document.getElementById("modalTeamName").textContent = team;
    document.getElementById("modalTeamLogo").src = teamLogo;
    document.getElementById("modalPlayerImage").setAttribute("data-playerid", playerId);
    document.getElementById("modalTeamLogo").onerror = function () {
        this.onerror = null;
        this.src = "{% static 'images/default3.png' %}"; // Fallback team logo
    };

    // **Convert fixture?.time to a formatted date**
    let fixtureDate = "TBD"; // Default if no date is provided
    if (fixture && fixture?.time && fixture?.time !== "TBD") {
        try {
            let dateObj = new Date(fixture?.time);
            let options = { weekday: "long", day: "numeric", month: "long" };
            fixtureDate = dateObj.toLocaleDateString("en-GB", options); // Example: "Saturday 15 February"
        } catch (error) {
            console.error("Error parsing fixture time:", error);
        }
    }

    // Set fixture details
    document.getElementById("fixtureTeam1Name").textContent = fixture?.team1 || "Team A";
    document.getElementById("fixtureTeam1Logo").src = fixture?.team1Logo;
    document.getElementById("fixtureTeam1Logo").onerror = function () {
        this.onerror = null;
        this.src = "{% static 'images/default3.png' %}"; // Fallback team1 logo
    };

    document.getElementById("fixtureTeam2Name").textContent = fixture?.team2 || "Team B";
    document.getElementById("fixtureTeam2Logo").src = fixture?.team2Logo;
    document.getElementById("fixtureTeam2Logo").onerror = function () {
        this.onerror = null;
        this.src = "{% static 'images/default3.png' %}"; // Fallback team2 logo
    };

        // Hide team2Logo if the team name is "Unknown"
    if (fixture?.team2 === "Unknown" || fixture?.team2 === "None") {
        document.getElementById("fixtureTeam2Logo").style.display = "none";  // Hide logo
    } else {
        document.getElementById("fixtureTeam2Logo").style.display = "inline"; // Show logo
    }
    
    document.getElementById("fixtureTime").textContent = fixtureDate; // Now dynamically formatted
    document.getElementById("fixtureDate").textContent = fixtureDate;

    // Show modal
    modal.style.display = "block";
}