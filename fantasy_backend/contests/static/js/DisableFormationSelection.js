
document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL
    const currentUrl = window.location.href;

    // Check if the URL contains an ID (e.g., 'https://pangasquadii.digitlogic.co.ke/api/team_selection/1/')
    const hasIdInUrl = currentUrl.match(/\/\d+\/$/); // This checks if there is an ID at the end of the URL

    // Get the formation select element
    const formationSelect = document.getElementById("formation-select");

    if (hasIdInUrl) {
        // Disable the formation select if ID is present in the URL
        formationSelect.disabled = true;
    } else {
        // Enable the formation select if no ID is found
        formationSelect.disabled = false;
    }
});

