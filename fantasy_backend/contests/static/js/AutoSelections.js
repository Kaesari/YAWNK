
let pitchPlayersAuto = new Set(); // This tracks players on the pitch
let usedPlayers = new Set(); // This tracks players that have already been picked (either on the pitch or as substitutes)
let teamPlayerCount = {}; // To track the number of players selected from each team (both for pitch and substitutes)

let totalBudget = 100.0; // Total available budget
let remainingBudgetAuto = totalBudget; // Remaining budget
let teamPresent = false;
document.addEventListener("DOMContentLoaded", function () {
    // Define formations and their respective positions
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
    
    const formationSelect = document.getElementById("formation-select");
    const pitchFormation = document.getElementById("pitch-formation");
    const autoPickButton = document.getElementById("autoPickButton");
    const budgetDisplay = document.getElementById("budgetDisplay");
    const favoriteClubId = "{{ favorite_club_id }}"; // Pass from backend

    let players = []; // Players will be dynamically populated

    // Fetch players dynamically based on teamId
    async function fetchPlayersByTeam(teamId) {
        try {
            const response = await fetch(`/api/get-players-by-team/?team_id=${teamId}`);
            const data = await response.json();
            // console.log("Players fetched from API:", data.players);
            if (data && data.players) {
                players = data.players.map((player) => ({
                    id: player.id,
                    name: player.name,
                    position: player.position,
                    price: player.price,
                    form: player.form || "N/A",
                    total_points: player.total_points,
                    tsb: player.tsb || "0%",
                    fixture: player.fixture,
                    team: player.team,
                    team_short: player.team_short,
                    teamLogo: player.teamLogo,
                    image: player.image || "https://resources.premierleague.com/premierleague/photos/players/110x140/p204716.png", // Fallback image
                    team_shirt: player.team_shirt || "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_8-110.webp", // Fallback shirt
                    // Fixture Details
                    fixture_data: {
                        team1: player.fixture_data?.team1 || "Unknown",
                        team1Logo: player.fixture_data?.team1Logo,
                        team2: player.fixture_data?.team2 || "Unknown",
                        team2Logo: player.fixture_data?.team2Logo,
                        time: player.fixture_data?.time || "TBD"
                    },

                }));
                // console.log(players);
                // window.sub_players = players;
            } else {
                console.error("No players found for the selected team.");
            }
        } catch (error) {
            console.error("Error fetching players:", error);
        }
    }

    // Update the budget display
    function updateBudgetDisplay() {
        budgetDisplay.textContent = `£${remainingBudgetAuto.toFixed(1)}m`;
    }

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

    // Function to render a formation
    function renderFormation(formationKey) {
        pitchFormation.innerHTML = ""; // Clear the pitch
        const formation = formations[formationKey];

        if (formation) {
            formation.forEach((slot, index) => {
                const positionDiv = document.createElement("div");
                positionDiv.className = "position-absolute text-center";
                positionDiv.style.top = slot.top;
                positionDiv.style.left = slot.left;
                positionDiv.style.transform = "translate(-50%, -50%)";

                // Shortened position names for small screens
                const shortPositions = {
                    "Goalkeepers": "GPK",
                    "Defenders": "DEFF",
                    "Midfielders": "MID",
                    "Forwards": "FWD"
                };

                // Detect screen width
                const isSmallScreen = window.innerWidth <= 576;
                const positionText = isSmallScreen ? shortPositions[slot.position] || slot.position : slot.position;

                // Conditionally apply a white border if the slot count is greater than 10
                if (index > 10) {
                    positionDiv.style.border = "1px solid white";  // Add white border
                    positionDiv.style.borderRadius = "10px";  // Add rounded corners
                }

                positionDiv.innerHTML = `
                    <div class="position-card d-flex justify-content-center align-items-center auto-reset-button ">
                        <div class="position-content">
                            <i class="fas fa-user-plus"></i> <!-- User Icon -->
                            <span>${positionText}</span>
                        </div>
                    </div>
                `;

                // Add click event to highlight the position
                positionDiv.addEventListener("click", () => {

                    // Check if the screen width is small (<= 768px)
                    if (window.innerWidth <= 768) {
                            var targetDiv = document.getElementById("targetDiv");
                            var targetDiv1 = document.getElementById("targetDiv1");
                            targetDiv.style.display = "none"; // Show the div
                            targetDiv1.style.display = "block"; // Show the div
                    }

                    applyFilters(positionText);
                });

                pitchFormation.appendChild(positionDiv);
            });
        }

        // Update positions dynamically when screen resizes
        window.addEventListener("resize", () => {
            document.querySelectorAll(".position-content span").forEach((span) => {
                const fullText = {
                    "GPK": "Goalkeepers",
                    "DEFF": "Defenders",
                    "MID": "Midfielders",
                    "FWD": "Forwards"
                };
                const shortText = {
                    "Goalkeepers": "GPK",
                    "Defenders": "DEFF",
                    "Midfielders": "MID",
                    "Forwards": "FWD"
                };

                const isSmallScreen = window.innerWidth <= 576;
                span.textContent = isSmallScreen ? shortText[span.textContent] || span.textContent : fullText[span.textContent] || span.textContent;
            });
        });

    }

     // Auto-pick players while considering the budget
    function autoPickPlayers(formationKey) {
        const formation = formations[formationKey];
        if (!formation) {
            console.error("Formation not found:", formationKey);
            return;
        }

        // Group players by position
        const groupedPlayers = {};
        players.forEach((player) => {
            if (!groupedPlayers[player.position]) {
                groupedPlayers[player.position] = [];
            }
            groupedPlayers[player.position].push(player);
        });

        // Shuffle players in each position group
        Object.keys(groupedPlayers).forEach((position) => {
            groupedPlayers[position] = groupedPlayers[position].sort(() => 0.5 - Math.random());
        });

        remainingBudgetAuto = totalBudget; // Reset budget
        updateBudgetDisplay();
        pitchFormation.innerHTML = ""; // Clear the pitch

        // Track used players to avoid duplicates
        // const usedPlayers = new Set();
        // const teamPlayerCount = {}; // Track number of players selected for each team

        formation.forEach((slot) => {
            if (!groupedPlayers[slot.position] || groupedPlayers[slot.position].length === 0) {
                console.warn("No players available for position:", slot.position);
                return;
            }

            // Get a unique player within budget and team constraints
            let selectedPlayer = null;
            for (let i = 0; i < groupedPlayers[slot.position].length; i++) {
                const potentialPlayer = groupedPlayers[slot.position][i];

                // Skip players that are already selected
                if (usedPlayers.has(potentialPlayer.name)) continue;

                // Check if the team already has 3 players selected
                if (teamPlayerCount[potentialPlayer.team] && teamPlayerCount[potentialPlayer.team] >= 3) {
                    continue; // Skip this player if their team already has 3 players selected
                }

                if (potentialPlayer.price <= remainingBudgetAuto) {
                    selectedPlayer = potentialPlayer;
                    usedPlayers.add(selectedPlayer.name); // Mark as used
                    remainingBudgetAuto -= selectedPlayer.price; // Deduct budget

                    // Update team player count
                    teamPlayerCount[potentialPlayer.team] = (teamPlayerCount[potentialPlayer.team] || 0) + 1;
                    break;
                }
            }

            if (!selectedPlayer) {
                console.warn("No affordable player for position:", slot.position);
                return;
            }

            // Create player card
            const playerDiv = document.createElement("div");
            playerDiv.className = "position-absolute text-center";
            playerDiv.style.top = slot.top;
            playerDiv.style.left = slot.left;
            playerDiv.style.transform = "translate(-50%, -50%)";

            // Default images categorized by position
            const defaultImagesByPosition = {
                "Goalkeepers": [
                    "https://resources.premierleague.com/premierleague/photos/players/110x140/p463748.png",
                    "https://resources.premierleague.com/premierleague/photos/players/110x140/p462492.png",
                    "https://resources.premierleague.com/premierleague/photos/players/110x140/p248164.png"
                ],
                "Defenders": [
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_14-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_91-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_11-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_39-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_8-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_1-66.webp"
                ],
                "Midfielders": [
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_14-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_91-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_11-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_39-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_8-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_1-66.webp"
                ],
                "Forwards": [
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_14-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_91-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_11-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_39-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_8-66.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_1-66.webp"
                ]
            };

            // Function to get a random default image based on player position
            function getRandomDefaultImage(position) {
                const images = defaultImagesByPosition[position] || [
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_11-66.webp"
                ]; // Fallback to a general default image if position not found
                return images[Math.floor(Math.random() * images.length)];
            }

            // Determine the final image source before rendering
            const finalImage = selectedPlayer.team_shirt ? selectedPlayer.team_shirt : getRandomDefaultImage(selectedPlayer.position);

            playerDiv.innerHTML = `
                <div class="rounded text-center shadow-sm position-relative player-card-save" 
                    style="font-family: Arial, sans-serif; cursor: pointer;"  
                    data-name="${selectedPlayer.name}" 
                    data-playerid="${selectedPlayer.id}"
                    data-image="${selectedPlayer.team_shirt}" 
                    data-position="${selectedPlayer.position}"
                    data-price="${selectedPlayer.price}" 
                    data-team_shirt="${selectedPlayer.team_shirt}"
                    data-form="${selectedPlayer.form || 'N/A'}"
                    data-tsb="${selectedPlayer.tsb || '0%'}"
                    data-team="${selectedPlayer.team}" 
                    data-teamlogo="${selectedPlayer.teamLogo}" 
                    data-fixture-team1="${selectedPlayer.fixture_data.team1}"
                    data-fixture-team1logo="${selectedPlayer.fixture_data.team1Logo}"
                    data-fixture-team2="${selectedPlayer.fixture_data.team2}"
                    data-fixture-team2logo="${selectedPlayer.fixture_data.team2Logo}"
                    data-fixture-time="${selectedPlayer.fixture_data.time}">

                    <!-- Image as Background -->
                    <div class="position-relative">
                        <div class="price-tag">
                            £${selectedPlayer.price}
                        </div>
                        <img src="${finalImage}" 
                            alt="${selectedPlayer.name.split(" ")[0]}" 
                            onerror="this.onerror=null; this.src='${getRandomDefaultImage(selectedPlayer.position)}'; this.parentElement.parentElement.setAttribute('data-image', this.src);" 
                            class="player-image">
                        
                        <!-- First Overlayed Text (Positioned at Bottom) -->
                        <div class="bg-white position-absolute w-100 text-center" 
                            style="bottom: 18px; left: 0; font-size: 0.6rem; font-weight: bold; color: #4A4A4A; padding: 3px; z-index: 2; background: rgba(255, 255, 255, 0.8);">
                            ${selectedPlayer.name.split(" ")[0]}
                        </div>

                        <!-- Second Overlayed Text (Directly Below the First) -->
                        <div class="position-absolute w-100 text-center" 
                            style="bottom: 0px; left: 0; font-size: 0.5rem; font-weight: bold; color: #000033; padding: 3px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px; z-index: 3; background: rgb(184,184,184);">
                            ${selectedPlayer.fixture} <!-- Example field for upcoming fixture -->
                        </div>
                    </div>
                </div>
            `;

                    // Add click event to open the modal
            playerDiv.querySelector(".player-card-save").addEventListener("click", function () {
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


            // Add player to the pitch
            pitchFormation.appendChild(playerDiv);
            updateBudgetDisplay();
        });
    }

function showPlayerModal(name, playerId, image, position, price, form, tsb, team, teamLogo, fixture) {
    const modal = document.getElementById("playerModal");

    const makeCaptainButton = document.getElementById("makeCaptainButton");
    const makeViceCaptainButton = document.getElementById("makeViceCaptainButton");
    const transferOutButton = document.getElementById("transferOutButton");
    const switchOutButton = document.getElementById("switchOutButton");

    transferOutButton.style.display = "none";
    switchOutButton.style.display = "none";
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

    document.getElementById("closeModalButton").addEventListener("click", function () {
        document.getElementById("playerModal").style.display = "none";
    });

    document.getElementById("playerModal").addEventListener("click", function (e) {
        if (e.target === this) {
            this.style.display = "none";
        }
    });
    
    formationSelect.addEventListener("change", function () {
        const hidesubscontainer = document.getElementById("subs-container");
        hidesubscontainer.style.display = "none";
        renderFormation(this.value);
    });

    // Execute renderFormation on load with the currently selected value or a default
    // renderFormation("4-3-3");

    autoPickButton.addEventListener("click", function () {
        const hidesubscontainer = document.getElementById("subs-container");
        hidesubscontainer.style.display = "block";
        pitchPlayersAuto.clear();
        usedPlayers.clear();
        teamPlayerCount = Object.create(null); // Ensure fresh reference
        
        autoPickPlayers(formationSelect.value); // Trigger auto-pick based on the current formation
    });

    async function initializeTeam(favoriteClubId) {
        try {
            // Fetch players by team
            await fetchPlayersByTeam(favoriteClubId);

            // Fetch team status
            const response = await fetch("/api/check-team-status/", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("Failed to fetch team status.");
            }

            const data = await response.json();

            if (!data.team_exists) {
                renderFormation("4-4-2"); // Render the default formation
                updateBudgetDisplay(); // Initialize budget display
                // console.log('Sangulo');
            }else{ 

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
                    if (!playersInGameweek.length > 0) {
                        renderFormation("4-4-2"); // Render the default formation
                        updateBudgetDisplay(); // Initialize budget display
                    }else{
                         teamPresent = true;
                    }
                })
                .catch((error) => {
                    console.error("Error loading saved team:", error);
                });

            }

        } catch (error) {
            console.error("Error initializing team:", error);
        }
    }

    // Usage
    fetchPlayersByTeam(favoriteClubId).then(() => {
        initializeTeam(favoriteClubId);
    });

    
});