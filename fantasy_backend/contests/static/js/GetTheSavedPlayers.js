
// let saved_player_repo;
document.addEventListener("DOMContentLoaded", function () {
    fetchSavedPlayers();
});

function fetchSavedPlayers() {

    function getUserIdFromUrl() {
        const urlParts = window.location.pathname.split('/');
        const potentialUserId = urlParts[urlParts.length - 2]; // Get second-to-last part of URL

        // Check if the URL contains 'team_selection' and if the ID is numeric
        if (window.location.pathname.includes("team_selection") && /^\d+$/.test(potentialUserId)) {
            return potentialUserId;  // Return the user ID if conditions are met
        }
        
        return null;  // Return null if 'team_selection' is not in the URL or the ID is invalid
    }

    const userId = getUserIdFromUrl(); // Fetch the user_id from the URL (if any)


    // Construct URL based on user_id
    let url = "/api/get-saved-team/";
    if (userId) {
        url = `/api/get-saved-team/${userId}/`; // Use the user-specific endpoint if user_id is present
    }

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

        const current_gameweek= document.getElementById("current_gameweek").textContent.trim();

        // Filter the players where gameweek is 27
        const playersInGameweek = data.team.filter(player => player.gameweek === parseInt(current_gameweek,0));

        // Check if there are any players for the specific gameweek
        if (playersInGameweek.length > 0) {
            const hidesubscontainer = document.getElementById("subs-container");
            hidesubscontainer.style.display = "block";
            renderSavedPlayers(playersInGameweek);  // Render only players with gameweek 27
        }
    })
    .catch((error) => {
        console.error("Error loading saved team:", error);
    });
}

// Convert kickoff time string into a Date object safely
function parseKickoffTime(kickoffTime) {
    return kickoffTime !== "TBD" ? new Date(kickoffTime) : null;
}

// Find the earliest kickoff time
function getEarliestKickoff(times) {
    const now = new Date();

    // Convert valid times to Date objects and filter out "TBD"
    let validTimes = times
        .map(time => parseKickoffTime(time))
        .filter(time => time !== null)  // Remove invalid times
        .sort((a, b) => a - b);  // Sort by earliest first

    return validTimes.length > 0 ? validTimes[0] : null;  // Return the earliest, or null if none
}


function renderSavedPlayers(savedTeam) {
    const pitchFormation = document.getElementById("pitch-formation");
    const budgetDisplay = document.getElementById("budgetDisplay");
    const totalBudget = 100.0; // Initial budget
    const subsContainerInner = document.querySelector("#subs-container > div");

    pitchFormation.innerHTML = ""; // Clear the pitch
    subsContainerInner.innerHTML = ""; // Clear the sub slots

    let totalPlayerPrice = 0;

    // ✅ Check if any player's match has started
    let isAnyKickoffStarted = savedTeam.some(player => {
        const kickoffTimes = Array.isArray(player.kickoff) ? player.kickoff : [player.kickoff];
        const earliestKickoff = getEarliestKickoff(kickoffTimes);
        return earliestKickoff && earliestKickoff < new Date();
    });

    // console.log("⚽ Any Match Started?:", isAnyKickoffStarted);

    savedTeam.forEach((player, index) => {


        const positionMapping = {
            "Goalkeepers": "GKP",
            "Defenders": "DEF",
            "Midfielders": "MID",
            "Forwards": "FWD"
        };

        // Parse position coordinates
        const coordinates = JSON.parse(player.position_coordinates || "{}");

        // Extracting the kickoff time(s) from the player fixture data
        const kickoffTimes = Array.isArray(player.kickoff) ? player.kickoff : [player.kickoff];
            // const earliestKickoff = getEarliestKickoff(kickoffTimes);
            // const testKickoffTimes = [
            //     "2025-02-27T15:00:00Z",
            //     "2025-02-24T19:30:00Z",  // The earliest one
            //     "2025-03-01T12:00:00Z"
            // ];

            const earliestKickoff = getEarliestKickoff(kickoffTimes);
            // const earliestKickoff = getEarliestKickoff(testKickoffTimes);

            // console.log("Earliest Kickoff:", earliestKickoff);

            // Determine whether to show price or score
        // const displayValue = isAnyKickoffStarted ? `${player.score} pts` : `£${player.price}`;
        const displayValue = isAnyKickoffStarted ? `£${player.price}` : `£${player.price}`;



        // If the player's position is GKP, DEF, or MID (or coordinates are empty)
        if (["GKP", "DEF", "FWD", "MID"].includes(player.position) || coordinates.top === "" || coordinates.left === "") {
            // Create sub slot for this player
            const slot = document.createElement("div");
            slot.className = "sub-slot text-center";
            slot.style.width = "120px";
            slot.style.padding = "10px";
            slot.style.border = "1px dashed #ccc";
            slot.style.cursor = "pointer";
            slot.style.position = "relative";

            // Adjust the label and the placement
            const label = positionMapping[player.position] || player.position; // Use the mapped label, fall back to full if not found

            slot.innerHTML = `<div>${label}</div>`;

            // Add the player card to the slot

            slot.innerHTML += `
                <div class="rounded text-center shadow-sm position-relative player-card-save" 
                    style="font-family: Arial, sans-serif; cursor: pointer;"  
                    data-name="${player.name}" 
                    data-playerid="${player.player_id}"
                    data-image="${player.team_shirt}" 
                    data-team_shirt="${player.team_shirt}"
                    data-position="${player.position}"  
                    data-price="${player.price}"
                    data-fixture="${player.fixture}"
                    data-form="${player.form || 'N/A'}"
                    data-tsb="${player.tsb || '0%'}"
                    data-team="${player.team}" 
                    data-captain="${player.is_captain}"
                    data-vicecaptain="${player.is_vicecaptain}"
                    data-teamlogo="${player.teamLogo}" 
                    data-fixture-team1="${player.fixture_data.team1}"
                    data-fixture-team1logo="${player.fixture_data.team1Logo}"
                    data-fixture-team2="${player.fixture_data.team2}"
                    data-fixture-team2logo="${player.fixture_data.team2Logo}"
                    data-fixture-time="${player.fixture_data.time}">

                    <!-- Image as Background -->
                    <div class="position-relative">
                    <div class="price-tag">
                        <!-- Captain Badge (Conditionally Shown) -->
                        ${Boolean(player.is_captain) ? `<img src="{% static 'images/caption.png' %}" alt="Captain" style="height: 20px; width: auto; display: block; position: absolute; top: 5px; left: 5px;" />` : ''}
                        <!-- Vice-Captain Badge (Conditionally Shown) -->
                        ${Boolean(player.is_vicecaptain) ? `<img src="{% static 'images/vcaption.png' %}" alt="VCaptain" style="height: 20px; width: auto; display: block; position: absolute; top: 5px; right: 5px;" />` : ''}
                       
                        ${displayValue}

                    </div>
                        <img src="${player.image}" 
                            alt="${player.name.split(' ')[0]}" 
                            onerror="this.onerror=null; this.src='{% static 'images/default2.png' %}'; this.parentElement.parentElement.setAttribute('data-image', this.src);" 
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

            // Attach event listener to show modal on click
            slot.querySelector(".player-card-save").addEventListener("click", function () {
                
                showPlayerModal(

                    index,

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

            subsContainerInner.appendChild(slot); // Append to the subs section
        } else {

            const positionDiv = document.createElement("div");
            positionDiv.className = "position-absolute text-center";
            positionDiv.style.transform = "translate(-50%, -50%)";
            positionDiv.setAttribute("data-index", index);
            positionDiv.setAttribute("data-position", player.position);

            // console.log(player.team_shirt);
            // Otherwise, render in the pitch formation
            positionDiv.style.top = coordinates.top;
            positionDiv.style.left = coordinates.left;
            positionDiv.innerHTML = `
                <div class="rounded text-center shadow-sm position-relative player-card-save" 
                    style="font-family: Arial, sans-serif; cursor: pointer;"  
                    data-name="${player.name}" 
                    data-playerid="${player.player_id}"
                    data-image="${player.team_shirt}" 
                    data-team_shirt="${player.team_shirt}"
                    data-position="${player.position}"  
                    data-price="${player.price}"
                    data-fixture="${player.fixture}"
                    data-form="${player.form || 'N/A'}"
                    data-tsb="${player.tsb || '0%'}"
                    data-team="${player.team}" 
                    data-captain="${player.is_captain}"
                    data-vicecaptain="${player.is_vicecaptain}"
                    data-teamlogo="${player.teamLogo}" 
                    data-fixture-team1="${player.fixture_data.team1}"
                    data-fixture-team1logo="${player.fixture_data.team1Logo}"
                    data-fixture-team2="${player.fixture_data.team2}"
                    data-fixture-team2logo="${player.fixture_data.team2Logo}"
                    data-fixture-time="${player.fixture_data.time}">

                    <!-- Image as Background -->
                    <div class="position-relative">
                    <div class="price-tag">
                        <!-- Captain Badge (Conditionally Shown) -->
                        ${Boolean(player.is_captain) ? `<img src="{% static 'images/caption.png' %}" alt="Captain" style="height: 20px; width: auto; display: block; position: absolute; top: 5px; left: 5px;" />` : ''}
                        <!-- Vice-Captain Badge (Conditionally Shown) -->
                        ${Boolean(player.is_vicecaptain) ? `<img src="{% static 'images/vcaption.png' %}" alt="VCaptain" style="height: 20px; width: auto; display: block; position: absolute; top: 5px; right: 5px;" />` : ''}
                        ${displayValue}
                    </div>
                        <img src="${player.team_shirt}" 
                            alt="${player.name.split(' ')[0]}" 
                            onerror="this.onerror=null; this.src='{% static 'images/default1.png' %}'; this.parentElement.parentElement.setAttribute('data-image', this.src);" 
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


            // Attach event listener to show modal on click
            positionDiv.querySelector(".player-card-save").addEventListener("click", function () {
                showPlayerModal(

                    index,

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

            pitchFormation.appendChild(positionDiv); // Append to the pitch formation
        }

        totalPlayerPrice += parseFloat(player.price) || 0;
    });

    // Update budget
    const remainingBudget = totalBudget - totalPlayerPrice;
    budgetDisplay.textContent = `£${remainingBudget.toFixed(1)}m`;
}

// Function to show modal with player details
function showPlayerModal(show,is_captain,is_vicecaptain,name, playerId, image, position, price, form, tsb, team, teamLogo, fixture) {
    const modal = document.getElementById("playerModal");
    const captainBadge = document.getElementById("captainBadge");
    const vicecaptainBadge = document.getElementById("vicecaptainBadge");

    const makeCaptainButton = document.getElementById("makeCaptainButton");
    const makeViceCaptainButton = document.getElementById("makeViceCaptainButton");
    const transferOutButton = document.getElementById("transferOutButton");

    if (show<11){
        makeCaptainButton.style.display = "block";  // Hide Make Captain button
        makeViceCaptainButton.style.display = "block";  // Hide Make Vice Captain button
    } else{
        makeCaptainButton.style.display = "none";  // Hide Make Captain button
        makeViceCaptainButton.style.display = "none";  // Hide Make Vice Captain button                    
    }

    // Get the current URL
    const currentUrl = window.location.href;

    // Check if the URL contains an ID (e.g., 'https://pangasquadii.digitlogic.co.ke/api/team_selection/1/')
    const hasIdInUrl = currentUrl.match(/\/\d+\/$/); // This checks if there is an ID at the end of the URL


    if (hasIdInUrl) {
        // Disable the formation select if ID is present in the URL
        makeCaptainButton.style.display = "none";  // Hide Make Captain button
        makeViceCaptainButton.style.display = "none";  // Hide Make Vice Captain button 
    } 

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



// Close the modal
document.getElementById("closeModalButton").addEventListener("click", function () {
    document.getElementById("playerModal").style.display = "none";
});

// Close modal when clicking outside of it
document.getElementById("playerModal").addEventListener("click", function (e) {
    if (e.target === this) {
        this.style.display = "none";
    }
});

// If using HTMX, listen for page updates
document.body.addEventListener("htmx:afterSwap", function () {
    fetchSavedPlayers();
});

