
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll(".alert");
    flashMessages.forEach((msg) => {
        setTimeout(() => {
            msg.style.display = "none";
        }, 5000);
    });
});
