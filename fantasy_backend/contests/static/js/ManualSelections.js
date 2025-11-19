
// Declare pitchPlayers globally, before any scripts
let pitchPlayers = new Set(); // This will track players already assigned to the pitch
let usedSubsPlayers = new Set(); // This will track players already assigned to the substitutes
let playerSection = 0;
let teamCounts = {}; // Track the number of selected players per team
let remainingBudget = 100; // Total budget in millions
let selectedPositionElement;
let playerIdRemoved = 0;
let teamPlayerIdRemoved = 0;
let RemovedPlayerPrice = 0;
let ReplaceLocationChanger = 0;
let selectedPlayers = new Set(); // To keep track of selected player IDs

document.addEventListener("DOMContentLoaded", function () {
    const pitchFormation = document.getElementById("pitch-formation");
    
    const tableBodies = {
        Goalkeepers: document.getElementById("goalkeepersTableBody"),
        Defenders: document.getElementById("defendersTableBody"),
        Midfielders: document.getElementById("midfieldersTableBody"),
        Forwards: document.getElementById("forwardsTableBody"),
    };
    const budgetDisplay = document.getElementById("budgetDisplay");
    const formationSelect = document.getElementById("formation-select");
    const resetButton = document.getElementById("resetButton");
    const AutoResetButton = document.getElementById("AutoResetButton");
    const autoPickButton = document.getElementById("autoPickButton");

    selectedPositionElement = null; // Currently selected pitch position
    // let remainingBudget = 100; // Total budget in millions

    // Update budget display
    const updateBudgetDisplay = () => {
        budgetDisplay.textContent = `£${remainingBudget.toFixed(1)}m`;
    };

    // Highlight selected pitch position
    const highlightPosition = (positionDiv, color = 'green') => {

        selectedPositionReplace = null;
        document.querySelectorAll(".pitch-position").forEach((div) => {
            div.style.border = ""; // Reset border for all positions
        });
        if (positionDiv) {
            positionDiv.style.border = `2px dashed ${color}`; // Highlight selected position
            selectedPositionElement = positionDiv;
        }
    };

    // Render formation on the pitch
    const renderFormation = (formationKey) => {
        pitchFormation.innerHTML = ""; // Clear the pitch

        const formations = {
            
            "4-4-2": [
                { position: "Goalkeepers", top: "14%", left: "50%" },

                { position: "Defenders", top: "35%", left: "10%" },
                { position: "Defenders", top: "35%", left: "35%" },
                { position: "Defenders", top: "35%", left: "65%" },
                { position: "Defenders", top: "35%", left: "90%" },

                { position: "Midfielders", top: "55%", left: "10%" },
                { position: "Midfielders", top: "55%", left: "35%" },
                { position: "Midfielders", top: "55%", left: "65%" },
                { position: "Midfielders", top: "55%", left: "90%" },

                { position: "Forwards", top: "75%", left: "25%" },
                { position: "Forwards", top: "75%", left: "75%" },

                { position: "Goalkeepers", top: "100%", left: "29%" },
                { position: "Defenders", top: "100%", left: "43%" },
                { position: "Midfielders", top: "100%", left: "57%" },
                { position: "Forwards", top: "100%", left: "71%" }
            ],

            "4-3-3": [
                { position: "Goalkeepers", top: "14%", left: "50%" },

                { position: "Defenders", top: "35%", left: "10%" },
                { position: "Defenders", top: "35%", left: "35%" },
                { position: "Defenders", top: "35%", left: "65%" },
                { position: "Defenders", top: "35%", left: "90%" },

                { position: "Midfielders", top: "55%", left: "15%" },
                { position: "Midfielders", top: "55%", left: "50%" },
                { position: "Midfielders", top: "55%", left: "85%" },

                { position: "Forwards", top: "75%", left: "15%" },
                { position: "Forwards", top: "75%", left: "50%" },
                { position: "Forwards", top: "75%", left: "85%" },

                { position: "Goalkeepers", top: "100%", left: "29%" },
                { position: "Defenders", top: "100%", left: "43%" },
                { position: "Midfielders", top: "100%", left: "57%" },
                { position: "Forwards", top: "100%", left: "71%" }
            ],

            "3-4-3": [
                { position: "Goalkeepers", top: "14%", left: "50%" },

                { position: "Defenders", top: "35%", left: "20%" },
                { position: "Defenders", top: "35%", left: "80%" },
                { position: "Defenders", top: "35%", left: "50%" },

                { position: "Midfielders", top: "55%", left: "15%" },
                { position: "Midfielders", top: "55%", left: "38%" },
                { position: "Midfielders", top: "55%", left: "63%" },
                { position: "Midfielders", top: "55%", left: "85%" },

                { position: "Forwards", top: "75%", left: "20%" },
                { position: "Forwards", top: "75%", left: "50%" },
                { position: "Forwards", top: "75%", left: "80%" },

                { position: "Goalkeepers", top: "100%", left: "29%" },
                { position: "Defenders", top: "100%", left: "43%" },
                { position: "Midfielders", top: "100%", left: "57%" },
                { position: "Forwards", top: "100%", left: "71%" }
            ], 

            "3-5-2": [
                { position: "Goalkeepers", top: "14%", left: "50%" },

                { position: "Defenders", top: "35%", left: "20%" },
                { position: "Defenders", top: "35%", left: "50%" },
                { position: "Defenders", top: "35%", left: "80%" },

                { position: "Midfielders", top: "55%", left: "10%" },
                { position: "Midfielders", top: "55%", left: "30%" },
                { position: "Midfielders", top: "55%", left: "50%" },
                { position: "Midfielders", top: "55%", left: "70%" },
                { position: "Midfielders", top: "55%", left: "90%" },

                { position: "Forwards", top: "75%", left: "25%" },
                { position: "Forwards", top: "75%", left: "75%" },

                { position: "Goalkeepers", top: "100%", left: "29%" },
                { position: "Defenders", top: "100%", left: "43%" },
                { position: "Midfielders", top: "100%", left: "57%" },
                { position: "Forwards", top: "100%", left: "71%" }
            ], 

            "4-5-1": [
                { position: "Goalkeepers", top: "14%", left: "50%" },

                { position: "Defenders", top: "35%", left: "10%" },
                { position: "Defenders", top: "35%", left: "35%" },
                { position: "Defenders", top: "35%", left: "65%" },
                { position: "Defenders", top: "35%", left: "90%" },

                { position: "Midfielders", top: "55%", left: "10%" },
                { position: "Midfielders", top: "55%", left: "30%" },
                { position: "Midfielders", top: "55%", left: "50%" },
                { position: "Midfielders", top: "55%", left: "70%" },
                { position: "Midfielders", top: "55%", left: "90%" },

                { position: "Forwards", top: "75%", left: "50%" },

                { position: "Goalkeepers", top: "100%", left: "29%" },
                { position: "Defenders", top: "100%", left: "43%" },
                { position: "Midfielders", top: "100%", left: "57%" },
                { position: "Forwards", top: "100%", left: "71%" }
            ],                    
            
            "5-3-2": [
                { position: "Goalkeepers", top: "14%", left: "50%" },

                { position: "Defenders", top: "35%", left: "10%" },
                { position: "Defenders", top: "35%", left: "30%" },
                { position: "Defenders", top: "35%", left: "50%" },
                { position: "Defenders", top: "35%", left: "70%" },
                { position: "Defenders", top: "35%", left: "90%" },

                { position: "Midfielders", top: "55%", left: "15%" },
                { position: "Midfielders", top: "55%", left: "50%" },
                { position: "Midfielders", top: "55%", left: "85%" },

                { position: "Forwards", top: "75%", left: "25%" },
                { position: "Forwards", top: "75%", left: "75%" },

                { position: "Goalkeepers", top: "100%", left: "29%" },
                { position: "Defenders", top: "100%", left: "43%" },
                { position: "Midfielders", top: "100%", left: "57%" },
                { position: "Forwards", top: "100%", left: "71%" }
            ],

            "5-4-1": [
                { position: "Goalkeepers", top: "14%", left: "50%" },

                { position: "Defenders", top: "35%", left: "10%" },
                { position: "Defenders", top: "35%", left: "30%" },
                { position: "Defenders", top: "35%", left: "50%" },
                { position: "Defenders", top: "35%", left: "70%" },
                { position: "Defenders", top: "35%", left: "90%" },

                { position: "Midfielders", top: "55%", left: "15%" },
                { position: "Midfielders", top: "55%", left: "38%" },
                { position: "Midfielders", top: "55%", left: "63%" },
                { position: "Midfielders", top: "55%", left: "85%" },

                { position: "Forwards", top: "75%", left: "50%" },

                { position: "Goalkeepers", top: "100%", left: "29%" },
                { position: "Defenders", top: "100%", left: "43%" },
                { position: "Midfielders", top: "100%", left: "57%" },
                { position: "Forwards", top: "100%", left: "71%" }
            ]

        };
        
        const formation = formations[formationKey];
        if (formation) {
            formation.forEach((slot, index) => {
                const positionDiv = document.createElement("div");
                positionDiv.className = "pitch-position position-absolute text-center";
                positionDiv.style.top = slot.top;
                positionDiv.style.left = slot.left;
                positionDiv.style.transform = "translate(-50%, -50%)";
                positionDiv.setAttribute("data-index", index);
                positionDiv.setAttribute("data-position", slot.position);

                // Conditionally apply a white border if the slot count is greater than 10
                if (index > 10) {
                    positionDiv.style.border = "1px solid white";  // Add white border
                    positionDiv.style.borderRadius = "10px";  // Add rounded corners
                }

                positionDiv.innerHTML = `
                    <div class="position-card d-flex justify-content-center align-items-center">
                        <div class="position-content">
                            <i class="fas fa-user-plus"></i> <!-- User Icon -->
                            <span>${slot.position}</span>
                        </div>
                    </div>
                `;

                // Add click event to highlight the position
                positionDiv.addEventListener("click", () => {
                    playerSection=2;
                    ReplaceLocationChanger = 1;
                    // console.log(teamCounts);
                    // console.log(teamCounts)
                    // console.log(pitchPlayers)
                    highlightPosition(positionDiv);
                    // console.log("Position clicked:", positionDiv.getAttribute('data-position'));
                    

                    // Check if the screen width is small (<= 768px)
                    if (window.innerWidth <= 768) {
                        var targetDiv = document.getElementById("targetDiv");
                        var targetDiv1 = document.getElementById("targetDiv1");
                        targetDiv.style.display = "none"; // Show the div
                        targetDiv1.style.display = "block"; // Show the div
                    }

                    applyFilters(positionDiv.getAttribute('data-position'));
                });

                pitchFormation.appendChild(positionDiv);
            });
        }
    }; 

    // Assign player to position
    const assignPlayerToPosition = (player) => {
      
        if (!selectedPositionElement && playerSection===0) {
            // alert("Please select a position on the pitch first!");
            showToast(`Please select a position on the pitch first!`, "warning");
            return;
        }

        // Count players from the same team
        if (!teamCounts[player.team]) {
            teamCounts[player.team] = 0;
        }

        // 🚨 **Check if team already has 3 players**
        if (teamCounts[player.team] >= 3) {
            // alert(`You cannot select more than 3 players from ${player.team}!`);
            showToast(`You cannot select more than 3 players from ${player.team}!`, "warning");
            return; // Prevent selection
        }

        if (selectedPlayers.has(player.id)) {
            // Show toast message for already selected player
            showToast(`${player.name} has already been selected!`, "warning");
            return; // Prevent selecting the same player again
        }

        const playerPrice = parseFloat(player.price);
        if (remainingBudget < playerPrice) {
            // Show toast message for insufficient budget
            showToast("Insufficient budget to add this player!", "warning");
            return;
        }

     if(playerSection===2){                
        // Deduct player price from the budget
        remainingBudget -= playerPrice;
        selectedPlayers.add(player.id);

        // console.log("Section "+playerSection);
        pitchPlayers.add(player.id);// Mark player as used in substitutes

        // console.log(pitchPlayers.size);
        if (pitchPlayers.size === 11) {
            // showToast(`Please select all the pitch players first!`, "warning");
            // return;
            const hidesubscontainer = document.getElementById("subs-container");
            hidesubscontainer.style.display = "block";
        }

        // ✅ **Update team count**
        teamCounts[player.team]++;

        updateBudgetDisplay();
        selectedPositionElement.innerHTML = `
            <div class="rounded text-center shadow-sm position-relative player-card-save" 
                style="font-family: Arial, sans-serif; cursor: pointer;"  
                data-name="${player.name}" 
                data-playerid="${player.id}"
                data-image="${player.team_shirt}" 
                data-position="${player.position}"  
                data-price="${player.price}"
                data-team_shirt="${player.team_shirt}"
                data-fixture="${player.fixture}"
                data-form="${player.form || 'N/A'}"
                data-tsb="${player.tsb || '0%'}"
                data-team="${player.team}" 
                data-teamlogo="${player.teamLogo}" 
                data-fixture-team1="${player.team1}"
                data-fixture-team1logo="${player.team1Logo}"
                data-fixture-team2="${player.team2}"
                data-fixture-team2logo="${player.team2Logo}"
                data-fixture-time="${player.time}">

                <!-- Image as Background -->
                <div class="position-relative">
                    <div class="price-tag">
                        £${player.price}
                    </div>
                    <img src="${player.image}" 
                        alt="${player.name.split(' ')[0]}" 
                        onerror="this.onerror=null; this.src='{% static 'images/default3.png' %}'; this.parentElement.parentElement.setAttribute('data-image', this.src);" 
                        class="player-image">
                    
                    <!-- First Overlayed Text (Positioned at Bottom) -->
                    <div class="bg-white position-absolute w-100 text-center" 
                        style="bottom: 18px; left: 0; font-size: 0.6rem; font-weight: bold; color: #4A4A4A; padding: 3px; z-index: 2; background: rgba(255, 255, 255, 0.8);">
                        ${player.name.split(" ")[0]}
                    </div>

                    <!-- Second Overlayed Text (Directly Below the First) -->
                    <div class="position-absolute w-100 text-center" 
                        style="bottom: 0px; left: 0; font-size: 0.5rem; font-weight: bold; color: #000033; padding: 3px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px; z-index: 3; background: rgb(184,184,184);">
                        ${player.fixture}
                    </div>
                </div>
            </div>

        `;


        // Add click event to the new player card for modal functionality
        selectedPositionElement.querySelector(".player-card-save").addEventListener("click", function (e) {
            // e.stopPropagation(); // Prevent event bubbling
            playerIdRemoved = this.getAttribute("data-playerid");
            teamPlayerIdRemoved = this.getAttribute("data-team");
            RemovedPlayerPrice = this.getAttribute("data-price");
            showPlayerModal(
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
        playerSection=0;

        // console.log(usedSubsPlayers);
        // console.log('Gap');
        // console.log(pitchPlayers);



        selectedPositionElement = null; // Reset selected position
    };

    // **Remove player and update team count**
    const removePlayer = (playerId, team, playerPrice) => {
        if (selectedPlayers.has(playerId)) {
            selectedPlayers.delete(playerId);
            pitchPlayers.delete(playerId);

            // Readd player price from the budget
            remainingBudget += Number(playerPrice);
            updateBudgetDisplay();

            if (teamCounts[team]) {
                teamCounts[team]--; // Reduce the count
            }
        }
    };

            // Show modal with player details For manual player
function showPlayerModal(name, playerId, image, position, price, form, tsb, team, teamLogo, fixture) {
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


// Close the modal
document.getElementById("closeModalButton").addEventListener("click", function () {
    // Hide the modal
    document.getElementById("playerModal").style.display = "none";

    // Check if there's a previously selected position and reset its border
    if (selectedPositionElement) {
        selectedPositionElement.style.border = ""; // Reset the border
        selectedPositionElement = null; // Clear the reference to the selected position
    }
});



document.getElementById("transferOutButton").addEventListener("click", function () {
    if (ReplaceLocationChanger === 1){
        document.getElementById("playerModal").style.display = "none";
    if (selectedPositionElement) {

        // Call the removePlayer function to remove the player from the set
        removePlayer(playerIdRemoved, teamPlayerIdRemoved, RemovedPlayerPrice);

        // console.log(teamCounts)
        // console.log(pitchPlayers)
        // console.log(playerIdRemoved)
        // console.log(teamPlayerIdRemoved)
        // console.log(selectedPositionElement)

        // Remove the player from the slot
        selectedPositionElement.innerHTML = `
            <div class="position-card d-flex justify-content-center align-items-center">
                <div class="position-content">
                    <i class="fas fa-user-plus"></i> <!-- User Icon -->
                    <span>${selectedPositionElement.getAttribute('data-position')}</span>
                </div>
            </div>
        `; // Resetting the HTML to default no player state

        // selectedPositionElement.style.border = "2px solid red"; // Using red for replacement indication
        highlightPosition(selectedPositionElement, 'red');

        // Resetting selectedPositionElement to ensure no selection is retained after replacement
    } else {
        console.log("No position selected.");
        alert("Please select a position on the pitch to replace a player.");
    } }
});

    // Handle manual player selection
    Object.values(tableBodies).forEach((tableBody) => {
        tableBody.addEventListener("click", (event) => {
            const row = event.target.closest(".player-selection-row");
            // Check if the screen width is small (<= 768px)
            if (window.innerWidth <= 768) {
                var targetDiv = document.getElementById("targetDiv");
                var targetDiv1 = document.getElementById("targetDiv1");
                targetDiv.style.display = "block"; // Show the div
                targetDiv1.style.display = "none"; // Show the div
            }
            if (!row) return;

            const player = {
                id: row.getAttribute("data-playerid"),
                name: row.getAttribute("data-name"),
                image: row.getAttribute("data-image"),
                team_shirt: row.getAttribute("data-team_shirt"),
                position: row.getAttribute("data-position"),
                price: row.getAttribute("data-price"),
                fixture: row.getAttribute("data-fixture"),
                form: row.getAttribute("data-form") || "N/A",
                tsb: row.getAttribute("data-tsb") || "0%",
                team: row.getAttribute("data-team") || "Unknown Team",
                teamLogo: row.getAttribute("data-teamlogo"),
                team1: row.getAttribute("data-fixture-team1") || "Team A",
                team1Logo: row.getAttribute("data-fixture-team1logo"),
                team2: row.getAttribute("data-fixture-team2") || "Team B",
                team2Logo: row.getAttribute("data-fixture-team2logo"),
                time: row.getAttribute("data-fixture-time") || "TBD"
            };

            // console.log(player);

            assignPlayerToPosition(player);
        });
    });

    const hidesubscontainer = document.getElementById("subs-container");
    
    // Reset button functionality
    resetButton.addEventListener("click", () => {
        // Clear all global tracking variables
        hidesubscontainer.style.display = "none";
        pitchPlayers.clear();
        usedSubsPlayers.clear();
        teamCounts = Object.create(null); // Ensure fresh reference
        playerSection = 0;
        selectedPlayers.clear();
        renderFormation(formationSelect.value); // Re-render formation
        remainingBudget = 100; // Reset budget
        updateBudgetDisplay();
    });

    document.getElementById('pitch-formation').addEventListener('click', function(event) {
        // Check if the clicked element or any of its parents have the 'auto-reset-button' class
        const target = event.target.closest('.auto-reset-button');
        if (target) {
            // console.log('Clicked Okobo:', target.querySelector('span').textContent);
            // Any other logic you want to execute on click

            // Clear all global tracking variables
            pitchPlayers.clear();
            usedSubsPlayers.clear();
            teamCounts = Object.create(null); // Ensure fresh reference
            playerSection = 0;
            selectedPlayers.clear();
            renderFormation(formationSelect.value); // Re-render formation
            remainingBudget = 100; // Reset budget
            updateBudgetDisplay();
            }
    });

    // Formation dropdown change event
    formationSelect.addEventListener("change", function () {
        renderFormation(this.value); // Re-render formation based on dropdown selection
    });

    // Render default formation on load
    // renderFormation(formationSelect.value);

    // Initialize budget display
    updateBudgetDisplay();
});