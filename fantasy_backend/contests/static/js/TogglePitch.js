
document.getElementById("hideDivLink").addEventListener("click", function() {
    var targetDiv = document.getElementById("targetDiv");
    var targetDiv1 = document.getElementById("targetDiv1");
    targetDiv.style.display = "none"; // Hides the div
    targetDiv1.style.display = "block"; // Show the div
});

document.getElementById("showDivLink").addEventListener("click", function() {
    var targetDiv = document.getElementById("targetDiv");
    var targetDiv1 = document.getElementById("targetDiv1");
    targetDiv.style.display = "block"; // Show the div
    targetDiv1.style.display = "none"; // Hides the div
});
