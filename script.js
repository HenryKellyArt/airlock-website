/* ============================================================
   AIRLOCK site - vanilla JS
   Hamburger nav overlay + media lightbox. No dependencies.
   ============================================================ */
(function () {
  "use strict";

  /* ---------- Mobile nav ---------- */
  var body = document.body;
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("mobile-menu");

  function openMenu() {
    body.classList.add("menu-open");
    if (toggle) toggle.setAttribute("aria-expanded", "true");
    body.style.overflow = "hidden";
  }
  function closeMenu() {
    body.classList.remove("menu-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    body.style.overflow = "";
  }
  function toggleMenu() {
    if (body.classList.contains("menu-open")) closeMenu();
    else openMenu();
  }

  if (toggle) {
    toggle.addEventListener("click", toggleMenu);
  }
  if (menu) {
    // close when a menu link/button is tapped
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeMenu();
    });
  }
  // Esc closes the menu (and any open lightbox)
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" || e.key === "Esc") {
      closeMenu();
      closeLightbox();
    }
  });
  // if the viewport grows past the breakpoint, make sure the menu is closed
  var mq = window.matchMedia("(min-width: 820px)");
  function handleMq(e) { if (e.matches) closeMenu(); }
  if (mq.addEventListener) mq.addEventListener("change", handleMq);
  else if (mq.addListener) mq.addListener(handleMq);

  /* ---------- Lightbox (media.html) ---------- */
  var lightbox = document.getElementById("lightbox");
  var lightboxImg = lightbox ? lightbox.querySelector("img") : null;

  function openLightbox(src, alt) {
    if (!lightbox || !lightboxImg) return;
    lightboxImg.src = src;
    lightboxImg.alt = alt || "";
    lightbox.classList.add("open");
    lightbox.setAttribute("aria-hidden", "false");
    body.style.overflow = "hidden";
  }
  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove("open");
    lightbox.setAttribute("aria-hidden", "true");
    if (lightboxImg) lightboxImg.removeAttribute("src");
    body.style.overflow = "";
  }

  if (lightbox) {
    // Wire every gallery on the page (screenshots + work-in-progress both use .gallery).
    var galleries = document.querySelectorAll(".gallery");
    Array.prototype.forEach.call(galleries, function (gallery) {
      gallery.addEventListener("click", function (e) {
        var fig = e.target.closest("figure");
        if (!fig) return;
        var img = fig.querySelector("img");
        if (!img) return;
        // prefer a full-res source if provided, else the displayed src
        var full = img.getAttribute("data-full") || img.currentSrc || img.src;
        openLightbox(full, img.alt);
      });
    });
    lightbox.addEventListener("click", function (e) {
      // click on backdrop or the close button closes it
      if (e.target === lightbox || e.target.closest(".lightbox-close")) {
        closeLightbox();
      }
    });
  }

  /* ---------- Footer year (keeps copyright honest if left long-term) ---------- */
  var yearEl = document.getElementById("footer-year");
  if (yearEl) {
    var y = new Date().getFullYear();
    if (y > 2026) yearEl.textContent = y;
  }
})();
