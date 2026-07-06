from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core import models as m


class Command(BaseCommand):
    help = "Seed the portfolio with sample content and an admin user (admin/admin1234)."

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin1234")
            self.stdout.write("Created superuser admin / admin1234")

        m.SiteSettings.load()
        m.HeroSection.load()
        m.AboutSection.load()

        # Process steps
        if not m.ProcessStep.objects.exists():
            steps = [
                ("Discover", "Stakeholder interviews, user research, and competitive analysis. I map what people actually need before touching a single pixel."),
                ("Define", "Personas, journey maps, and a sharp problem statement. Everyone agrees on the problem before we debate solutions."),
                ("Design", "Wireframes → high-fidelity UI → interactive prototype, with usability testing between each jump in fidelity."),
                ("Deliver", "A documented design system and clean, responsive HTML/CSS/JS handoff — or the build itself, done by me."),
                ("Measure", "Post-launch analytics review and a follow-up usability round. Design isn't done until the numbers say so."),
            ]
            for i, (t, d) in enumerate(steps):
                m.ProcessStep.objects.create(title=t, description=d, order=i)

        # Timeline
        if not m.TimelineEntry.objects.exists():
            work = [
                ("2023 — Present", "Senior Product Designer", "Northwind Labs",
                 "Leading design for a B2B analytics platform. Built the design system used by 4 product teams."),
                ("2021 — 2023", "UI/UX Designer", "Brightside Studio",
                 "Designed 20+ marketing sites, dashboards and mobile apps for startups across fintech and health."),
                ("2019 — 2021", "UI Developer", "Freelance",
                 "Translated designs into fast, accessible, responsive front-ends with HTML, CSS and vanilla JavaScript."),
            ]
            for i, (p, t, o, d) in enumerate(work):
                m.TimelineEntry.objects.create(kind="work", period=p, title=t, org=o,
                                               description=d, order=i)
            edu = [
                ("2015 — 2019", "B.Des, Communication Design", "National Institute of Design",
                 "Focus on interaction design and typography."),
                ("2020", "Google UX Design Certificate", "Coursera", ""),
            ]
            for i, (p, t, o, d) in enumerate(edu):
                m.TimelineEntry.objects.create(kind="education", period=p, title=t,
                                               org=o, description=d, order=i)

        # Certifications
        if not m.Certification.objects.exists():
            certs = [
                ("Google UX Design Certificate", "Coursera", "2020", ""),
                ("Advanced Figma for Product Teams", "Figma", "2022", ""),
                ("Accessible Web Design", "Interaction Design Foundation", "2023", ""),
            ]
            for i, (t, iss, d, u) in enumerate(certs):
                m.Certification.objects.create(title=t, issuer=iss, date=d,
                                                credential_url=u, order=i)

        # Skills
        if not m.SkillCategory.objects.exists():
            data = {
                "Design": [("UI Design", 96), ("UX Design", 92), ("Design Systems", 90),
                           ("User Research", 85), ("Wireframing", 94), ("Prototyping", 91),
                           ("Responsive Design", 95)],
                "Development": [("HTML", 96), ("CSS", 94), ("JavaScript", 86)],
                "Tools": [("Figma", 97), ("Adobe XD", 88), ("Photoshop", 84),
                          ("Illustrator", 82), ("VS Code", 90), ("Git & GitHub", 85)],
            }
            for i, (cat, skills) in enumerate(data.items()):
                c = m.SkillCategory.objects.create(name=cat, order=i)
                for j, (name, level) in enumerate(skills):
                    m.Skill.objects.create(category=c, name=name, level=level, order=j)

        # Services
        if not m.Service.objects.exists():
            services = [
                ("UI Design", "Interfaces that look considered and feel obvious — every state, every breakpoint.", "layout"),
                ("UX Design", "Research-driven flows that reduce friction and support real user goals.", "users"),
                ("Website Design", "Marketing sites and portfolios that load fast and convert calmly.", "monitor"),
                ("Landing Page Design", "Focused, single-purpose pages with a clear story and one job to do.", "pen"),
                ("Dashboard Design", "Dense data made legible: hierarchy, charts, and sensible defaults.", "grid"),
                ("Mobile App Design", "Native-feeling iOS and Android interfaces designed thumb-first.", "smartphone"),
                ("Design Systems", "Tokens, components, and documentation your whole team can build on.", "layers"),
                ("Responsive Frontend Development", "Semantic HTML, modern CSS, and vanilla JavaScript — accessible and quick.", "code"),
            ]
            for i, (t, d, icon) in enumerate(services):
                m.Service.objects.create(title=t, description=d, icon=icon, order=i)

        # Client logos
        if not m.ClientLogo.objects.exists():
            for i, name in enumerate(["Northwind", "Acme Health", "Finch Pay",
                                      "Loomly", "Cardinal", "Statlas"]):
                m.ClientLogo.objects.create(name=name, order=i)

        # Testimonials
        if not m.Testimonial.objects.exists():
            ts = [
                ("Priya Nair", "Product Manager, Finch Pay",
                 "Our onboarding completion rate went from 61% to 84% after the redesign. The research phase alone was worth the fee.", 5, True),
                ("Daniel Okoye", "Founder, Loomly",
                 "Rare combination: a designer who ships production-quality front-end code. The handoff was the code.", 5, True),
                ("Sara Kim", "Head of Design, Northwind Labs",
                 "The design system brought four bickering product teams onto one visual language in a quarter.", 5, False),
                ("Marco Ruiz", "CTO, Cardinal",
                 "Clear communicator, fast iterations, zero ego about feedback. The dashboard finally makes sense to customers.", 5, False),
                ("Anita Joseph", "Marketing Lead, Statlas",
                 "Our landing page bounce rate dropped by a third. Beautiful work, delivered ahead of schedule.", 4, False),
            ]
            for i, (n, r, q, rating, feat) in enumerate(ts):
                m.Testimonial.objects.create(name=n, role=r, quote=q, rating=rating,
                                             featured=feat, order=i)

        # Social links
        if not m.SocialLink.objects.exists():
            for i, (p, u) in enumerate([
                ("dribbble", "https://dribbble.com/"),
                ("behance", "https://www.behance.net/"),
                ("linkedin", "https://www.linkedin.com/"),
                ("github", "https://github.com/"),
            ]):
                m.SocialLink.objects.create(platform=p, url=u, order=i)

        # Categories + projects
        if not m.Project.objects.exists():
            cats = {}
            for i, name in enumerate(["Web App", "Mobile App", "Website", "Design System"]):
                cats[name] = m.ProjectCategory.objects.create(name=name, order=i)

            projects = [
                dict(
                    title="Finch Pay Onboarding", category=cats["Mobile App"],
                    year="2025", client="Finch Pay", featured=True, accent_hue=252,
                    summary="Rebuilding a fintech onboarding flow that lost 4 in 10 users before their first transaction.",
                    overview="Finch Pay is a peer-to-peer payments app for first-time digital banking users. New users were abandoning onboarding at an alarming rate, and support tickets pointed to confusion, not bugs.",
                    problem="Analytics showed a 39% drop-off across the 11-step signup. Users didn't know why documents were needed, how long verification would take, or whether their money was safe. The flow asked for trust before earning it.",
                    research="I ran 12 moderated usability sessions with target users, analyzed 3 months of funnel data, and audited 6 competitor flows. The pattern: every drop-off spike matched a moment where the app asked for something without explaining why.",
                    persona="Primary persona: 'Cautious Chitra', 28, first salary job, comfortable with UPI but wary of new financial apps. Goal: send money home without fees. Fear: being locked out of her own funds. She reads every permission dialog.",
                    wireframes="Low-fi wireframes cut the flow from 11 steps to 6 by merging related inputs and moving KYC after the first (limited) transaction. Each step gained a one-line 'why we ask' note and a progress indicator with time estimates.",
                    design_process="Three rounds of prototype testing. Round one killed a clever animated stepper (users read it as an ad). Round two validated the 'try before verify' model. Round three tuned microcopy with the compliance team.",
                    high_fidelity="The final UI uses a calm two-color palette, oversized input fields tested for one-handed use, and inline validation that celebrates progress instead of flagging errors in red first.",
                    design_system="Delivered 42 components as Figma variables plus a coded reference implementation — buttons, inputs, sheets, progress patterns — documented with do/don't examples.",
                    results="Onboarding completion rose from 61% to 84% in eight weeks. Time-to-first-transaction dropped from 2.1 days to 40 minutes. Support tickets about signup fell 57%.",
                    lessons="Trust is a design material. The biggest wins came from explaining, not simplifying — some steps got longer and still converted better.",
                ),
                dict(
                    title="Statlas Analytics Dashboard", category=cats["Web App"],
                    year="2024", client="Statlas", featured=True, accent_hue=200,
                    summary="A dense analytics product redesigned so non-analysts could answer their own questions.",
                    overview="Statlas sells web analytics to small e-commerce teams. Power users loved it; everyone else exported to spreadsheets. The company wanted the product itself to be the answer.",
                    problem="Customers could see every metric but couldn't find the one that mattered. Twenty-two chart types, no hierarchy, and settings buried three menus deep.",
                    research="Card sorting with 18 customers revealed three real jobs: 'is today normal?', 'what changed?', and 'is this campaign working?'. Nobody's job was 'browse charts'.",
                    persona="'Shop-owner Sam' checks metrics on a phone between packing orders. He needs a verdict, not a dataset.",
                    wireframes="Wireframes reorganized the product around the three jobs as landing views, with drill-down for analysts preserved one click deeper.",
                    design_process="Weekly design reviews with two pilot customers. A 'boring but obvious' variant beat the visually rich concept in every task-completion test.",
                    high_fidelity="Final screens lead with plain-language verdict cards ('Revenue is up 12% vs. a typical Tuesday'), backed by compact sparkline rows and a consistent 4pt grid.",
                    design_system="A charting sub-system: 8 chart primitives with fixed semantic colors, empty states, and loading skeletons — spec'd in Figma and shipped as CSS/JS reference components.",
                    results="Weekly active usage among non-analyst seats grew 2.3×. Spreadsheet exports fell by half. Churn in the smallest plan tier dropped 18%.",
                    lessons="Density wasn't the enemy; ambiguity was. Users happily read dense screens when every number carries a verdict.",
                ),
                dict(
                    title="Cardinal Design System", category=cats["Design System"],
                    year="2024", client="Cardinal", featured=True, accent_hue=150,
                    summary="One visual language for four product teams shipping in three frameworks.",
                    overview="Cardinal's four product teams had four button styles, three grids, and no shared vocabulary. I was brought in to build the system and the process around it.",
                    problem="Inconsistency was slowing everyone: designers redrew basics, engineers re-implemented them, QA re-tested them, and customers noticed the seams.",
                    research="A UI inventory catalogued 61 button variants and 14 shades of 'brand blue'. Interviews with each team surfaced the real blocker: nobody trusted a system they couldn't influence.",
                    design_process="Started with tokens (color, type, space, radius, elevation), then the 12 highest-traffic components. A fortnightly 'system council' with one member per team owned decisions — adoption became their idea.",
                    design_system="120 tokens, 34 documented components with usage guidance, accessibility notes, and code snippets. Contribution model included an RFC template and a deprecation policy.",
                    results="New-feature design time down 40%. Cross-product UI bugs down 63% in six months. All four teams migrated the core 12 components within two quarters.",
                    lessons="A design system is a social contract with a Figma file attached. Governance mattered more than any component.",
                ),
                dict(
                    title="Acme Health Patient Portal", category=cats["Web App"],
                    year="2023", client="Acme Health", featured=True, accent_hue=330,
                    summary="An accessible appointment and records portal designed with — not just for — older patients.",
                    overview="Acme Health needed a portal usable by patients aged 8 to 88, meeting WCAG 2.2 AA, on any device including shared library computers.",
                    problem="The legacy portal had a 12% task-completion rate for users over 60. Phone bookings were costing the clinic network a full-time team.",
                    research="Co-design workshops in two clinics with 15 patients aged 60+. Key findings: fear of 'breaking something', invisibility of system status, and login as the single biggest wall.",
                    persona="'Careful Kurian', 71, manages appointments for himself and his wife. Uses a tablet with enlarged text. Will phone the clinic the moment anything is unclear.",
                    wireframes="Wireframes enforced one action per screen, a persistent 'where am I / what's next' rail, and magic-link login that removed passwords entirely.",
                    high_fidelity="Final UI: 18px base type, 48px minimum targets, high-contrast mode as a first-class theme, and confirmation screens that read like a receptionist speaking.",
                    results="Task completion for 60+ users rose to 78%. Online bookings up 3.4×. The clinic reassigned half the phone team within a year.",
                    lessons="Designing for the most constrained users made the product better for everyone — the 'accessible' flow became everyone's favorite flow.",
                ),
                dict(
                    title="Loomly Marketing Site", category=cats["Website"],
                    year="2023", client="Loomly", featured=False, accent_hue=28,
                    summary="A fast, story-driven marketing site that cut bounce rate by a third.",
                    overview="Loomly, a scheduling tool for creators, needed a site that explained the product in one scroll and loaded instantly on mobile networks.",
                    problem="The old site led with features; visitors couldn't tell what the product did in the first five seconds.",
                    design_process="Message-first design: we wrote and tested the narrative before any visuals, then designed sections as beats in that story.",
                    high_fidelity="Semantic HTML, hand-tuned CSS, no framework. Largest Contentful Paint under 1.2s on 3G. Scroll-triggered product shots demonstrate the tool doing its job.",
                    results="Bounce rate down 34%, trial signups up 22%, and the site scores 99 on Lighthouse performance.",
                    lessons="Copy is the interface on a marketing site. Design amplified the message; it couldn't replace it.",
                ),
                dict(
                    title="Northwind Mobile Companion", category=cats["Mobile App"],
                    year="2025", client="Northwind Labs", featured=False, accent_hue=265,
                    summary="A read-only mobile companion that gives analysts their dashboards on the train.",
                    overview="Northwind's analysts wanted glanceable access to alerts and key metrics away from their desks — not the full product squeezed onto a phone.",
                    problem="A responsive port of the desktop app had been tried and abandoned: too dense, too slow, wrong mental model for mobile moments.",
                    research="Diary studies with 9 analysts mapped mobile moments: commute checks, meeting prep, and alert triage. All read-heavy, all under 90 seconds.",
                    wireframes="Wireframes framed the app as a feed of cards, each answering one question, with deep links back to desktop for real work.",
                    high_fidelity="Thumb-first layout, dark theme default, haptic-confirmed alert acknowledgements, and widgets for the two most-checked metrics.",
                    results="72% of analysts use it weekly; alert acknowledgement time dropped from hours to minutes.",
                    lessons="The best mobile version of a desktop product is often a different product with shared data.",
                ),
            ]
            for i, p in enumerate(projects):
                m.Project.objects.create(order=i, **p)

        # Case studies
        if not m.CaseStudy.objects.exists():
            cases = [
                dict(
                    title="Rescuing a checkout: from 68% abandonment to 41%",
                    subtitle="A end-to-end UX investigation of Finch Pay's payment flow.",
                    year="2025", featured=True, accent_hue=252,
                    summary="Cart abandonment at 68% was treated as a pricing problem. Research showed it was a confidence problem — and design fixed it.",
                    research="Funnel analytics located the cliff at the payment-method step. Session recordings showed rage-clicks on a disabled button; 10 user interviews revealed nobody understood why it was disabled. A hidden validation rule was silently failing.",
                    user_flow="The redesigned flow collapsed 5 screens into 3, moved account creation after purchase, and made every disabled state explain itself inline.",
                    journey_map="Mapping the emotional journey exposed a trust trough exactly at payment: no security cues, no order summary in view, no human-readable totals. Each trough got a specific intervention.",
                    design_decisions="Key call: keep the order summary sticky on mobile despite the space cost. Testing showed users scrolled up to re-check totals before paying — removing that scroll removed the hesitation.",
                    prototype="A high-fidelity Figma prototype was tested with 8 users across 3 rounds; final round hit 100% task completion with zero assists.",
                    before_after="Before: 5 screens, 14 fields, disabled buttons without explanations, 68% abandonment. After: 3 screens, 8 fields, self-explaining states, 41% abandonment — a 27-point recovery worth roughly $2.1M in annualized recovered revenue.",
                    outcome="Shipped in 6 weeks. Beyond the numbers, the support team reported checkout complaints 'basically disappeared' from their queue.",
                ),
                dict(
                    title="Making dense data legible for non-analysts",
                    subtitle="How Statlas turned chart browsers into decision makers.",
                    year="2024", featured=True, accent_hue=200,
                    summary="A jobs-to-be-done restructuring of an analytics product, told from first card sort to post-launch metrics.",
                    research="18 card-sorting sessions and 3 months of usage analytics converged on the same insight: users had 3 questions and the product answered none of them directly.",
                    user_flow="New IA: three job-based home views with progressive disclosure into the full analyst toolkit. No feature was removed; everything was re-ranked.",
                    journey_map="The journey map showed 'insight' arriving only after export to spreadsheets — the product's value was being realized outside the product.",
                    design_decisions="Verdict-first cards were controversial internally ('dumbing it down'). A/B evidence settled it: verdict cards doubled engagement with the underlying detailed charts.",
                    prototype="Clickable prototype validated with 2 pilot customers over 4 weekly sessions before a line of production code changed.",
                    before_after="Before: 22 chart types on one screen, 9% weekly engagement from non-analyst seats. After: 3 job-based views, 21% weekly engagement, spreadsheet exports halved.",
                    outcome="Churn in the entry tier fell 18% quarter over quarter. The 'is today normal?' view is now the most-visited screen in the product.",
                ),
            ]
            for i, c in enumerate(cases):
                m.CaseStudy.objects.create(order=i, **c)

        self.stdout.write(self.style.SUCCESS("Seed complete."))
