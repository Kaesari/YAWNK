
document.addEventListener("DOMContentLoaded", function () {
    const makeCaptainButton = document.getElementById("makeCaptainButton");
    const makeViceCaptainButton = document.getElementById("makeViceCaptainButton");

    if (!makeCaptainButton || !makeViceCaptainButton) {
        console.error("Captain or Vice Captain button not found.");
        return;
    }

    makeCaptainButton.addEventListener("click", function () {
        updateCaptainOrViceCaptain("captain");
    });

    makeViceCaptainButton.addEventListener("click", function () {
        updateCaptainOrViceCaptain("vice_captain");
    });

    function updateCaptainOrViceCaptain(role) {
        const playerId = document.getElementById("modalPlayerImage").getAttribute("data-playerid");

        if (!playerId) {
            console.error("Player ID not found!");
            return;
        }

        fetch("/api/update-captain/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                role: role,
                player_id: playerId
            })
        })
        .then(response => response.json())
        .then(data => {
            // console.log("Server Response:", data);
            // alert(`${role.replace("_", " ")} updated successfully!`);

            showToast(data.message || `${role.replace("_", " ")} updated successfully!`, "success");

            // console.log(role);

            
            // Dynamically show the captain image if player is updated as captain
            if (data.captain === playerId) {
                document.getElementById("captainBadge").style.display = "block";  // Show the badge
            }

            if (role === 'captain') {
                document.getElementById("captainBadge").style.display = "block";  // Show the badge
            }

            if (role === 'vice_captain') {
                document.getElementById("vicecaptainBadge").style.display = "block";  // Show the badge
            }

            // Refresh the page to reflect the updated data
            location.reload();  // Reloads the page
        })
        .catch(error => console.error("Error:", error));
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

    function getCSRFToken() {
        let csrfToken = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];

        return csrfToken || "";
    }
});
