const old_password = document.getElementById("old_password");
const password_form = document.getElementById("change_password");
const errorElement = document.getElementById("error");
password_form.addEventListener("submit", (e) => {
  let messages = [];
  if (old_password.value == "" || old_password.value == null) {
    messages.push("Please type in your current password");
  }

  if (messages.length > 0) {
    e.preventDefault();
    errorElement.innerText = messages.join(", ");
  }
});

// work on this soon
