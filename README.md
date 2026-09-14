# Premium Designer Portfolio — Django + Vanilla Frontend

An Awwwards-style portfolio for a UI/UX Designer & UI Developer.
Public site: pure HTML/CSS/JS (GSAP, Lenis, Swiper, AOS, Typed.js via CDN).
Backend: Django + SQLite used **only** as a hidden content-management system.

## Quick start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data      # sample content + admin user
python manage.py runserver
```

Open http://127.0.0.1:8000

## Content management (hidden CMS)

The CMS is Django admin, rebranded "Studio Console" and served at a
non-obvious URL that is never linked from the public site:

- URL: http://127.0.0.1:8000/dashboard/asif/
- Login: `admin` / `admin1234`  (change this immediately)

From there you can manage: hero section, about section, projects (with all
case-study sections + image galleries), case studies, skills, services,
testimonials, client logos, timeline (experience/education), design process
steps, social links, SEO settings, resume upload, and read contact-form
messages (read-only inbox).

To move the CMS somewhere else, change `CMS_URL_PREFIX` in `config/settings.py`.

## Pages

- `/` Home — hero with typing animation, animated counters, featured projects
  & case studies, skills, client logos, testimonial slider, contact CTA
- `/about/` — intro, philosophy, numbered design process, experience &
  education timelines, values, resume download
- `/projects/` — grid with category filter + live search
- `/projects/<slug>/` — full case-study layout (overview, problem, research,
  persona, wireframes, process, hi-fi UI, prototype embed, design system,
  final screens gallery, results, lessons, next-project link)
- `/case-studies/` and `/case-studies/<slug>/` — deep-dive UX write-ups
- `/skills/` — skill bars + 8 services
- `/testimonials/`, `/contact/` — working contact form saved to the inbox

## Frontend features

Smooth scrolling (Lenis), GSAP scroll reveals & parallax, hero line reveal,
Typed.js roles, custom morphing cursor with "View" state, magnetic buttons,
auto-hiding glass header, page-fade transitions, preloader, marquee,
animated skill bars & counters, Swiper testimonials, client-side project
filter/search, lazy images, mobile menu — all with `prefers-reduced-motion`
support and keyboard-accessible focus states.

## Production notes

- Set `DEBUG = False`, a real `SECRET_KEY`, and `ALLOWED_HOSTS` in
  `config/settings.py`
- Run `python manage.py collectstatic` and serve `staticfiles/` + `media/`
  via your web server
- Replace the seeded sample content and placeholder gradient covers with
  real project imagery via the CMS
