
function showToast(message, type = "danger") {
    const toastContainer = document.getElementById("toastContainer");

    // Create the toast element
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute("role", "alert");
    toast.setAttribute("aria-live", "assertive");
    toast.setAttribute("aria-atomic", "true");
    toast.setAttribute("data-bs-autohide", "true");
    toast.setAttribute("data-bs-delay", "3000");

    // Add the toast content
    toast.innerHTML = `
    <div class="d-flex">
        <div class="toast-body">
            ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    `;

    // Append the toast to the container
    toastContainer.appendChild(toast);

    // Initialize the toast using Bootstrap's JS
    const bootstrapToast = new bootstrap.Toast(toast);
    bootstrapToast.show();

    // Remove the toast from the DOM after it hides
    toast.addEventListener("hidden.bs.toast", () => {
        toast.remove();
    });
}
