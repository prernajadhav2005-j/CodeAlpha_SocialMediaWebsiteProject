// Show confirmation before logout
function confirmLogout() {
    return confirm("Are you sure you want to logout?");
}

// Auto-hide Django messages after 3 seconds
setTimeout(function () {
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => msg.style.display = 'none');
}, 3000);

// Like animation (visual only – backend handled by Django)
document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll(".like-btn");

    likeButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.style.transform = "scale(1.2)";
            setTimeout(() => {
                btn.style.transform = "scale(1)";
            }, 150);
        });
    });
});
