document.addEventListener("submit", function (e) {
  if (!e.target.classList.contains("comment-form")) return;

  e.preventDefault();

  const form = e.target;
  const postId = form.dataset.id;
  const input = form.querySelector("input[name='comment']");
  const text = input.value.trim();

  if (!text) return;

  fetch(`/posts/add-comment/${postId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": form.querySelector(
        "input[name=csrfmiddlewaretoken]"
      ).value,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Request failed");
      return res.json();
    })
    .then((data) => {
      if (data.status === "ok") {
        const commentsDiv = document.getElementById(
          `comments-${postId}`
        );

        commentsDiv.insertAdjacentHTML(
          "beforeend",
          `<small><b>${data.username}</b>: ${data.text}</small><br>`
        );

        input.value = "";
      }
    })
    .catch((err) => console.error("Comment error:", err));
});
