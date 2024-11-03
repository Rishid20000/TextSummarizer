// Update slider value display
document.getElementById("slider").addEventListener("input", function() {
    document.getElementById("sliderValue").textContent = this.value + " words";
});

// Character counter
document.getElementById("text").addEventListener("input", function() {
    document.getElementById("charCount").textContent = this.value.length;
});

// Show loading animation
document.getElementById("summaryForm").addEventListener("submit", function() {
    document.querySelector(".loading").style.display = "block";
    document.querySelector(".btn-submit").disabled = true;
});

// Copy summary to clipboard
function copySummary() {
    const summaryText = document.getElementById("summarized");
    summaryText.select();
    document.execCommand("copy");
    
    const copyBtn = document.getElementById("copyBtn");
    copyBtn.innerHTML = '<i class="fas fa-check"></i>';
    setTimeout(() => {
        copyBtn.innerHTML = '<i class="far fa-copy"></i>';
    }, 2000);
}

// Dark mode toggle
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    const icon = document.querySelector(".dark-mode-toggle i");
    if (document.body.classList.contains("dark-mode")) {
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
    } else {
        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");
    }
}