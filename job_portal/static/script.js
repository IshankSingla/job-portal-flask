// ========== 1. Auto-dismiss Bootstrap alerts after 4 seconds ==========
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(alert => {
    // Add fade out animation before closing
    alert.classList.remove('show');
    alert.classList.add('fade');

    setTimeout(() => {
      if (alert.parentNode) {
        alert.remove(); // Clean up after animation
      }
    }, 500); // delay for fade out
  });
}, 4000);

// ========== 2. Toggle password visibility ==========
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".toggle-password").forEach(button => {
    button.addEventListener("click", () => {
      const targetId = button.getAttribute("data-target");
      const input = document.getElementById(targetId);

      if (input && input.type === "password") {
        input.type = "text";
        button.innerHTML = '<i class="fa fa-eye-slash"></i>'; // Icon for hide
      } else if (input) {
        input.type = "password";
        button.innerHTML = '<i class="fa fa-eye"></i>'; // Icon for show
      }
    });
  });
});
