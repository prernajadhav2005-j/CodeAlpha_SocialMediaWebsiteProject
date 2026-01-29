document.addEventListener("click", function (e) {
  if (!e.target.classList.contains("follow-btn")) return;

  const btn = e.target;
  const userId = btn.dataset.userId;

  fetch("/accounts/toggle-follow/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value,
    },
    body: JSON.stringify({ user_id: userId }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "followed") {
        btn.classList.remove("btn-outline-success");
        btn.classList.add("btn-success");
        btn.textContent = "Following";
      }

      if (data.status === "unfollowed") {
        btn.classList.remove("btn-success");
        btn.classList.add("btn-outline-success");
        btn.textContent = "Follow";
      }
    });
});
