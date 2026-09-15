/* ==========================================================================
   Portfolio — main.js
   Lenis smooth scroll · GSAP reveals · custom cursor · magnetic buttons ·
   counters · nav · testimonial swiper · project filter/search · typed hero
   ========================================================================== */

(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isTouch = window.matchMedia("(hover: none)").matches;

  /* ---------------------------------------------------------- preloader */
  /* Plays only on first entry to the site; skipped on later in-session
     navigation (base.html already hides it synchronously in that case). */
  const introKey = "introPlayed";
  const preloader = document.getElementById("preloader");

  if (sessionStorage.getItem(introKey) === "1") {
    window.addEventListener("load", heroIntro);
  } else {
    const fill = preloader && preloader.querySelector(".preloader__fill");
    let progress = 0;
    const tick = setInterval(() => {
      progress = Math.min(progress + Math.random() * 24, 92);
      if (fill) fill.style.width = progress + "%";
    }, 120);

    window.addEventListener("load", () => {
      clearInterval(tick);
      if (fill) fill.style.width = "100%";
      setTimeout(() => {
        preloader && preloader.classList.add("is-done");
        document.body.classList.add("is-loaded");
        sessionStorage.setItem(introKey, "1");
        heroIntro();
      }, reduceMotion ? 0 : 420);
    });
  }

  /* ------------------------------------------------------- lenis scroll */
  let lenis = null;
  if (window.Lenis && !reduceMotion) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    if (window.ScrollTrigger) lenis.on("scroll", ScrollTrigger.update);
  }

  /* ------------------------------------------------------------- GSAP */
  if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);

    // Image parallax
    if (!reduceMotion) {
      document.querySelectorAll("[data-parallax]").forEach((el) => {
        gsap.to(el, {
          yPercent: parseFloat(el.dataset.parallax) || -12,
          ease: "none",
          scrollTrigger: { trigger: el.parentElement, scrub: true },
        });
      });
    }

    // Animated counters
    document.querySelectorAll("[data-count]").forEach((el) => {
      const target = parseInt(el.dataset.count, 10) || 0;
      ScrollTrigger.create({
        trigger: el, start: "top 92%", once: true,
        onEnter: () => {
          gsap.fromTo(el, { innerText: 0 }, {
            innerText: target, duration: reduceMotion ? 0 : 1.6,
            ease: "power2.out", snap: { innerText: 1 },
          });
        },
      });
    });
  }

  /* ---------------------------------------------------- hero intro anim */
  function heroIntro() {
    if (!window.gsap) return;
    const lines = document.querySelectorAll(".hero__title .line > span");
    if (!lines.length) return;
    if (reduceMotion) return;
    gsap.from(lines, {
      yPercent: 110, duration: 1.1, ease: "power4.out", stagger: 0.12,
    });
    gsap.from(".hero [data-intro]", {
      y: 26, opacity: 0, duration: 0.9, ease: "power3.out",
      stagger: 0.1, delay: 0.35,
    });
  }

  /* ---------------------------------------------------------- Typed.js */
  const typedTarget = document.getElementById("typedRole");
  if (typedTarget && window.Typed) {
    const roles = JSON.parse(typedTarget.dataset.roles || "[]");
    if (roles.length) {
      new Typed("#typedRole", {
        strings: roles, typeSpeed: 55, backSpeed: 30, backDelay: 1600, loop: true,
      });
    }
  }

  /* --------------------------------------------------------------- AOS */
  if (window.AOS) {
    AOS.init({
      duration: 750, easing: "ease-out-cubic", once: true, offset: 60,
      disable: reduceMotion,
    });
  }

  /* ------------------------------------------------------------ header */
  const header = document.getElementById("siteHeader");
  let lastY = 0;
  window.addEventListener("scroll", () => {
    const y = window.scrollY;
    header.classList.toggle("is-scrolled", y > 24);
    header.classList.toggle("is-hidden", y > 420 && y > lastY);
    lastY = y;
  }, { passive: true });

  /* ------------------------------------------------------- mobile menu */
  const toggle = document.getElementById("navToggle");
  const menu = document.getElementById("mobileMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const open = menu.classList.toggle("is-open");
      toggle.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open);
      menu.setAttribute("aria-hidden", !open);
      document.body.style.overflow = open ? "hidden" : "";
      if (lenis) open ? lenis.stop() : lenis.start();
    });
    menu.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => toggle.click()));
  }

  /* --------------------------------------------------- magnetic buttons */
  if (!isTouch && !reduceMotion && window.gsap) {
    document.querySelectorAll(".magnetic").forEach((el) => {
      el.addEventListener("mousemove", (e) => {
        const r = el.getBoundingClientRect();
        gsap.to(el, {
          x: (e.clientX - r.left - r.width / 2) * 0.28,
          y: (e.clientY - r.top - r.height / 2) * 0.28,
          duration: 0.4, ease: "power3.out",
        });
      });
      el.addEventListener("mouseleave", () =>
        gsap.to(el, { x: 0, y: 0, duration: 0.6, ease: "elastic.out(1,0.4)" }));
    });
  }

  /* ------------------------------------------------- testimonial swiper */
  if (window.Swiper && document.querySelector(".testimonial-swiper")) {
    new Swiper(".testimonial-swiper", {
      slidesPerView: 1, spaceBetween: 24,
      pagination: { el: ".swiper-pagination", clickable: true },
      autoplay: { delay: 4500, disableOnInteraction: false },
      breakpoints: { 700: { slidesPerView: 2 }, 1080: { slidesPerView: 3 } },
    });
  }

  /* ------------------------------------------------------ project search */
  const cards = document.querySelectorAll("[data-project-card]");
  const searchInput = document.getElementById("projectSearch");
  const emptyState = document.getElementById("projectsEmpty");

  function applyFilter() {
    const q = (searchInput ? searchInput.value : "").trim().toLowerCase();
    let visible = 0;
    cards.forEach((card) => {
      const show = !q || card.dataset.search.includes(q);
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });
    if (emptyState) emptyState.hidden = visible !== 0;
    if (window.ScrollTrigger) ScrollTrigger.refresh();
  }
  if (searchInput) searchInput.addEventListener("input", applyFilter);

  /* -------------------------------------------------- page transitions */
  if (!reduceMotion) {
    document.querySelectorAll("a[href]").forEach((a) => {
      const url = new URL(a.href, location.href);
      const internal = url.origin === location.origin &&
        !a.hasAttribute("target") && !a.hasAttribute("download") &&
        !url.hash && url.pathname !== location.pathname;
      if (!internal) return;
      a.addEventListener("click", (e) => {
        e.preventDefault();
        document.body.classList.add("is-leaving");
        gsap.to("main, footer", { opacity: 0, y: -14, duration: 0.3, ease: "power2.in" });
        setTimeout(() => { location.href = a.href; }, 320);
      });
    });
  }

  /* ---------------------------------------------------------- footer year */
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  /* --------------------------------------------------------- lazy images */
  // Native lazy loading is set in templates; this upgrades with a soft fade.
  document.querySelectorAll("img[loading='lazy']").forEach((img) => {
    img.style.opacity = img.complete ? 1 : 0;
    img.style.transition = "opacity .6s ease";
    img.addEventListener("load", () => (img.style.opacity = 1));
  });
})();
