document.addEventListener("DOMContentLoaded", function() {
    // Look for the metadata element
    const metaEl = document.getElementById("quiz-metadata");
    if (!metaEl) return;

    const totalDuration = parseInt(metaEl.getAttribute("data-duration"));
    if (isNaN(totalDuration) || totalDuration <= 0) return;

    let timeLeft = totalDuration;

    const minutesEl = document.getElementById("minutes");
    const secondsEl = document.getElementById("seconds");
    const timerProgressBar = document.getElementById("timerProgressBar");
    const timerCard = document.getElementById("timerCard");
    const mobileTimerText = document.getElementById("mobileTimerText");
    const quizForm = document.getElementById("quizForm");

    function updateTimer() {
        // Calculate minutes and seconds
        let m = Math.floor(timeLeft / 60);
        let s = timeLeft % 60;

        // Pad with leading zeros
        m = m < 10 ? "0" + m : m;
        s = s < 10 ? "0" + s : s;

        if (minutesEl) minutesEl.textContent = m;
        if (secondsEl) secondsEl.textContent = s;
        if (mobileTimerText) mobileTimerText.textContent = `${m}:${s}`;

        // Update Progress Bar
        if (timerProgressBar) {
            const percent = (timeLeft / totalDuration) * 100;
            timerProgressBar.style.width = percent + "%";
        }

        // Visual threshold feedback
        if (timerCard) {
            if (timeLeft <= 30) {
                // Danger zone (30s remaining)
                timerCard.className = "card glass-card p-4 timer-danger";
                if (timerProgressBar) timerProgressBar.className = "progress-bar bg-danger";
            } else if (timeLeft <= 90) {
                // Warning zone (90s remaining)
                timerCard.className = "card glass-card p-4 timer-warning";
                if (timerProgressBar) timerProgressBar.className = "progress-bar bg-warning";
            } else {
                // Normal operation
                timerCard.className = "card glass-card p-4 timer-glow";
                if (timerProgressBar) timerProgressBar.className = "progress-bar bg-success";
            }
        }

        // Time Over trigger
        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            autoSubmit();
        } else {
            timeLeft--;
        }
    }

    function autoSubmit() {
        if (!quizForm) return;

        // Suppress standard HTML5 form validations so it completes immediately
        const inputs = quizForm.querySelectorAll('input[required]');
        inputs.forEach(input => input.removeAttribute('required'));
        
        // Show auto-submit notification on screen
        const container = document.querySelector(".container");
        if (container) {
            const alertDiv = document.createElement("div");
            alertDiv.className = "alert alert-danger alert-dismissible fade show alert-custom d-flex align-items-center gap-2 mb-4 sticky-top";
            alertDiv.innerHTML = `<i class="bi bi-clock-fill fs-5"></i><div>Time is up! Your answers are being auto-submitted...</div>`;
            container.prepend(alertDiv);
        }
        
        setTimeout(() => {
            quizForm.submit();
        }, 1000);
    }

    // Initialize & Start Timer Loop
    updateTimer();
    const countdownInterval = setInterval(updateTimer, 1000);
});
