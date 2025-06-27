history.scrollRestoration = "manual";

async function markAsRead(element) {
  const res = await fetch(`/articles/${element.id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ read: 1 }),
  });
  if (res.status == 200) element.classList.add("is-read");
}

function observe() {
  document.querySelectorAll(".article").forEach((article) => {
    const callback = (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting && entry.boundingClientRect.bottom < 0 && !article.classList.contains("is-read")) {
          markAsRead(article);
        }
      });
    };

    const observer = new IntersectionObserver(callback, { threshold: 0 });
    observer.observe(article);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  window.scrollTo(0, 0);
  observe();
});
