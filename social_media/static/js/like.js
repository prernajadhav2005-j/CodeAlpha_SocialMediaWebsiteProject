document.addEventListener("click", function (e) {
  if (!e.target.closest(".like-btn")) return;

  const btn = e.target.closest(".like-btn");
  const postId = btn.dataset.id;
  const likeCountSpan = document.getElementById(
    `like-count-${postId}`
  );

  fetch(`/posts/toggle-like/${postId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value,
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "liked") {
        likeCountSpan.textContent = data.likes_count;
      }

      if (data.status === "unliked") {
        likeCountSpan.textContent = data.likes_count;
      }
    })
    .catch((err) => console.error(err));
});
