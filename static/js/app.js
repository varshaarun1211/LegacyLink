document.addEventListener("DOMContentLoaded", function () {
  const menuButton = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#nav");
  if (menuButton && nav) {
    menuButton.addEventListener("click", function () {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      nav.classList.toggle("nav-open", !isOpen);
    });
  }

  document.querySelectorAll("[data-api-form]").forEach(function (form) {
    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      const status = form.querySelector(".form-status");
      const button = form.querySelector('button[type="submit"]');
      const fields = Object.fromEntries(new FormData(form).entries());
      form.querySelectorAll(".field-error").forEach(function (e) { e.textContent = ""; });
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (status) status.textContent = "Sending...";
      if (button) { button.disabled = true; button.dataset.label = button.textContent; button.textContent = "Please wait..."; }
      try {
        const response = await fetch(form.dataset.apiForm, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Accept": "application/json" },
          credentials: "same-origin",
          body: JSON.stringify(fields)
        });
        const result = await response.json().catch(function () { return {}; });
        if (!response.ok) {
          if (result.errors) {
            Object.entries(result.errors).forEach(function (entry) {
              const target = form.querySelector('[data-error-for="' + entry[0] + '"]');
              if (target) target.textContent = Array.isArray(entry[1]) ? entry[1].join(" ") : String(entry[1]);
            });
          }
          throw new Error(result.message || "The request failed. Check your information and try again.");
        }
        if (status) status.textContent = result.message || form.dataset.success || "Done.";
        if (result.redirect_url) window.location.assign(result.redirect_url);
        else if (form.dataset.apiForm === "/api/register") form.reset();
      } catch (error) {
        if (status) status.textContent = error instanceof TypeError
          ? "The backend route is not available yet. Ask your teammate to implement it."
          : error.message;
      } finally {
        if (button) { button.disabled = false; button.textContent = button.dataset.label || "Submit"; }
      }
    });
  });

  const filterForm = document.querySelector("#directory-filters");
  if (filterForm) {
    filterForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const f = Object.fromEntries(new FormData(filterForm).entries());
      const cards = Array.from(document.querySelectorAll(".person"));
      let shown = 0;
      cards.forEach(function (card) {
        const match = (!f.q || card.dataset.name.includes(f.q.toLowerCase())) &&
          (!f.department || card.dataset.department.includes(f.department.toLowerCase())) &&
          (!f.graduation_year || card.dataset.year.includes(f.graduation_year.trim())) &&
          (!f.company || card.dataset.company.includes(f.company.toLowerCase()));
        card.hidden = !match;
        if (match) shown++;
      });
      document.querySelector("#directory-empty").hidden = shown > 0;
    });
  }

  document.querySelectorAll("[data-review-action]").forEach(function (button) {
    button.addEventListener("click", async function () {
      const card = button.closest("[data-review-id]");
      const action = button.dataset.reviewAction;
      if (!window.confirm("Confirm you want to " + action + " this fictional demo registration?")) return;
      const status = document.querySelector("#admin-status");
      try {
        const response = await fetch("/api/admin/" + card.dataset.reviewId + "/" + action, {
          method: "POST", headers: { "Accept": "application/json" }, credentials: "same-origin"
        });
        const result = await response.json().catch(function () { return {}; });
        if (!response.ok) throw new Error(result.message || "Admin route unavailable or access denied.");
        card.remove();
        status.textContent = result.message || "Registration " + action + "d.";
      } catch (error) {
        status.textContent = error instanceof TypeError
          ? "The backend admin route is not available yet."
          : error.message;
      }
    });
  });
});
