// let teamPresent = false;
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

    let totalBudget = 100.0; // Total available budget
    let remainingBudget = totalBudget; // Remaining budget
    let players = []; // Players will be dynamically populated

    // Fetch players dynamically based on teamId
    async function fetchPlayersByTeam(teamId) {
        try {
            const response = await fetch(`/api/get-saved-team/`);
            const data = await response.json();
            // console.log("Players fetched from API:", data.team);
            if (data && data.team) {
                // players = data.team.map((player) => ({
                players = data.team
                    .filter(player => {
                        const coordinates = JSON.parse(player.position_coordinates || "{}");
                        return !(
                            ["GKP", "DEF", "FWD", "MID"].includes(player.position) || 
                            coordinates.top === "" || 
                            coordinates.left === ""
                        );
                    })    
                    .filter(player => {
                        // Filter by gameweek
                        const current_gameweek= document.getElementById("current_gameweek").textContent.trim();
                        return player.gameweek === parseInt(current_gameweek,0);  // Ensure prev_gameweek is an integer
                    })
                    .map(player => ({
                        id: player.player_id,
                        name: player.name,
                        position: player.position,
                        price: player.price,
                        form: player.form || "N/A",
                        total_points: player.total_points,
                        tsb: player.tsb || "0%",
                        fixture: player.fixture,
                        team: player.team,
                        is_captain: player.is_captain,
                        is_vicecaptain: player.is_vicecaptain,
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
        budgetDisplay.textContent = `£${remainingBudget.toFixed(1)}m`;
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

        // Shuffle players in each position group to ensure randomness
        Object.keys(groupedPlayers).forEach((position) => {
            groupedPlayers[position] = groupedPlayers[position].sort(() => 0.5 - Math.random());
        });

        remainingBudget = totalBudget; // Reset budget
        updateBudgetDisplay();
        pitchFormation.innerHTML = ""; // Clear the pitch

        const usedPlayers = new Set();
        const teamPlayerCount = {}; // Track team limits

        // Keep track of available backup players in case a position is missing
        let backupPlayers = [...players].sort(() => 0.5 - Math.random()); // Fallback players list

        formation.forEach((slot) => {
            let selectedPlayer = null;

            // Try to get a player from the correct position
            if (groupedPlayers[slot.position] && groupedPlayers[slot.position].length > 0) {
                for (let i = 0; i < groupedPlayers[slot.position].length; i++) {
                    const potentialPlayer = groupedPlayers[slot.position][i];

                    if (usedPlayers.has(potentialPlayer.name)) continue;
                    if (teamPlayerCount[potentialPlayer.team] && teamPlayerCount[potentialPlayer.team] >= 3) continue;
                    if (potentialPlayer.price > remainingBudget) continue;

                    selectedPlayer = potentialPlayer;
                    groupedPlayers[slot.position].splice(i, 1); // Remove from available list
                    break;
                }
            }

            // If no suitable player is found, use a backup player from another position
            if (!selectedPlayer) {
                for (let i = 0; i < backupPlayers.length; i++) {
                    const potentialBackup = backupPlayers[i];

                    if (usedPlayers.has(potentialBackup.name)) continue;
                    if (teamPlayerCount[potentialBackup.team] && teamPlayerCount[potentialBackup.team] >= 3) continue;
                    if (potentialBackup.price > remainingBudget) continue;

                    // Ensure the backup player matches the required position
                    if (potentialBackup.position !== slot.position) continue;

                    selectedPlayer = potentialBackup;
                    backupPlayers.splice(i, 1); // Remove from available backups
                    break;
                }
            }

            if (!selectedPlayer) {
                console.warn("No suitable player for position:", slot.position);

                // Try to assign any leftover player to the empty position
                for (let i = 0; i < backupPlayers.length; i++) {
                    const leftoverPlayer = backupPlayers[i];

                    if (usedPlayers.has(leftoverPlayer.name)) continue; // Skip already used players
                    if (teamPlayerCount[leftoverPlayer.team] && teamPlayerCount[leftoverPlayer.team] >= 3) continue; // Skip if team limit is reached
                    if (leftoverPlayer.price > remainingBudget) continue; // Skip if player exceeds budget

                    // Assign the leftover player to the empty position
                    selectedPlayer = leftoverPlayer;
                    backupPlayers.splice(i, 1); // Remove from the backup list
                    break;
                }

                // If no leftover player is found, add a placeholder
                if (!selectedPlayer) {
                    console.warn("No affordable player or leftover player for position:", slot.position);

                    // Create a placeholder for the position
                    const placeholderDiv = document.createElement("div");
                    placeholderDiv.className = "position-absolute text-center";
                    placeholderDiv.style.top = slot.top;
                    placeholderDiv.style.left = slot.left;
                    placeholderDiv.style.transform = "translate(-50%, -50%)";
                    placeholderDiv.style.border = "1px solid white"; // Add white border
                    placeholderDiv.style.borderRadius = "10px"; // Add rounded corners

                    // Add the placeholder HTML
                    placeholderDiv.innerHTML = `
                        <div class="position-card d-flex justify-content-center align-items-center auto-reset-button">
                            <div class="position-content">
                                <i class="fas fa-user-plus"></i> <!-- User Icon -->
                                <span>${slot.position}</span>
                            </div>
                        </div>
                    `;

                    // Append the placeholder to the pitch
                    pitchFormation.appendChild(placeholderDiv);
                    return; // Exit the current iteration
                }
            }

            // Mark player as used
            usedPlayers.add(selectedPlayer.name);
            remainingBudget -= selectedPlayer.price;
            teamPlayerCount[selectedPlayer.team] = (teamPlayerCount[selectedPlayer.team] || 0) + 1;

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
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_91-110.webp"
                ],
                "Midfielders": [
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_14-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_91-110.webp"
                ],
                "Forwards": [
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_31-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_14-110.webp",
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_91-110.webp"
                ]
            };

            // Function to get a random default image based on player position
            function getRandomDefaultImage(position) {
                const images = defaultImagesByPosition[position] || [
                    "https://fplchallenge.premierleague.com/dist/img/shirts/standard/shirt_11-66.webp"
                ];
                return images[Math.floor(Math.random() * images.length)];
            }

            // Determine final image
            const finalImage = selectedPlayer.team_shirt || getRandomDefaultImage(selectedPlayer.position);

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
                    data-captain="${selectedPlayer.is_captain}"
                    data-vicecaptain="${selectedPlayer.is_vicecaptain}"
                    data-teamlogo="${selectedPlayer.teamLogo}" 
                    data-fixture-team1="${selectedPlayer.fixture_data.team1}"
                    data-fixture-team1logo="${selectedPlayer.fixture_data.team1Logo}"
                    data-fixture-team2="${selectedPlayer.fixture_data.team2}"
                    data-fixture-team2logo="${selectedPlayer.fixture_data.team2Logo}"
                    data-fixture-time="${selectedPlayer.fixture_data.time}">

                    <div class="position-relative">
                        <div class="price-tag">
                            <!-- Captain Badge (Conditionally Shown) -->
                            ${Boolean(selectedPlayer.is_captain) ? `<img src="{% static 'images/caption.png' %}" alt="Captain" style="height: 20px; width: auto; display: block; position: absolute; top: 5px; left: 5px;" />` : ''}
                            <!-- Vice-Captain Badge (Conditionally Shown) -->
                            ${Boolean(selectedPlayer.is_vicecaptain) ? `<img src="{% static 'images/vcaption.png' %}" alt="VCaptain" style="height: 20px; width: auto; display: block; position: absolute; top: 5px; right: 5px;" />` : ''}
                            £${selectedPlayer.price}
                        </div>
                        <img src="${finalImage}" 
                            alt="${selectedPlayer.name.split(" ")[0]}" 
                            onerror="this.onerror=null; this.src='${getRandomDefaultImage(selectedPlayer.position)}'; this.parentElement.parentElement.setAttribute('data-image', this.src);" 
                            class="player-image">
                        
                        <div class="bg-white position-absolute w-100 text-center" 
                            style="bottom: 18px; left: 0; font-size: 0.6rem; font-weight: bold; color: #4A4A4A; padding: 3px; z-index: 2; background: rgba(255, 255, 255, 0.8);">
                            ${selectedPlayer.name.split(" ")[0]}
                        </div>

                        <div class="position-absolute w-100 text-center" 
                            style="bottom: 0px; left: 0; font-size: 0.5rem; font-weight: bold; color: #000033; padding: 3px; border-bottom-left-radius: 2px; border-bottom-right-radius: 2px; z-index: 3; background: rgb(184,184,184);">
                            ${selectedPlayer.fixture}
                        </div>
                    </div>
                </div>
            `;

            // Add click event to open modal
            playerDiv.querySelector(".player-card-save").addEventListener("click", function () {
                showPlayerModal( 

                    this.getAttribute("data-captain"),
                    this.getAttribute("data-vicecaptain"),

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

            pitchFormation.appendChild(playerDiv);
            updateBudgetDisplay();
        });
    }

                // Function to show modal with player details
    function showPlayerModal(is_captain,is_vicecaptain,name, playerId, image, position, price, form, tsb, team, teamLogo, fixture) {
        const modal = document.getElementById("playerModal");
        const captainBadge = document.getElementById("captainBadge");
        const vicecaptainBadge = document.getElementById("vicecaptainBadge");

        const makeCaptainButton = document.getElementById("makeCaptainButton");
        const makeViceCaptainButton = document.getElementById("makeViceCaptainButton");
        const transferOutButton = document.getElementById("transferOutButton");

        makeCaptainButton.style.display = "block";  // Hide Make Captain button
        makeViceCaptainButton.style.display = "block";  // Hide Make Vice Captain button

        // Convert is_captain to boolean if it's a string
        const isCaptainBoolean = (is_captain === true || is_captain === "true" || is_captain === 1);

        // Convert is_captain to boolean if it's a string
        const isVcaptainBoolean = (is_vicecaptain === true || is_vicecaptain === "true" || is_vicecaptain === 1);

        // Initially hide the captain badge when the modal opens
        captainBadge.style.display = "none";  // Hide by default

        // Initially hide the captain badge when the modal opens
        vicecaptainBadge.style.display = "none";  // Hide by default
        transferOutButton.style.display = "none";  // Hide by default
        switchOutButton.style.display = "none";

        // Show the captain badge only if the player is the captain
        if (isCaptainBoolean) {
            captainBadge.style.display = "block";  // Show the badge if the player is the captain
            makeViceCaptainButton.disabled = true;
        }else{
            captainBadge.style.display = "none";  // Hide Captain Badge
            makeViceCaptainButton.disabled = false;  // Enable Make Captain button
        }

        // Show the captain badge only if the player is the captain
        if (isVcaptainBoolean) {
            vicecaptainBadge.style.display = "block";  // Show the badge if the player is the captain
            makeCaptainButton.disabled = true;
        }else{
            vicecaptainBadge.style.display = "none";  // Hide Vice-Captain Badge
            makeCaptainButton.disabled = false;  // Enable Make Vice-Captain button
        }
        
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
        if(teamPresent === true){
        saveTeamButton.disabled = false;
        saveTeamButton.textContent = "Update Team";
        saveTeamButton.classList.remove("btn-secondary");
        saveTeamButton.classList.add("btn-primary");
        // renderFormation(this.value);
        autoPickPlayers(formationSelect.value);}
    });

    // Execute renderFormation on load with the currently selected value or a default
    // renderFormation("4-3-3");

    // autoPickButton.addEventListener("click", function () {
    //     autoPickPlayers(formationSelect.value); // Trigger auto-pick based on the current formation
    // });

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

        } catch (error) {
            console.error("Error initializing team:", error);
        }
    }

    // Usage
    fetchPlayersByTeam(favoriteClubId).then(() => {
        // initializeTeam(favoriteClubId);
    });

    
});