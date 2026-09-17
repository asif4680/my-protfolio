from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# ---------------------------------------------------------------- singletons
class SingletonModel(models.Model):
    """Only one row ever exists — used for site-wide settings sections."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    site_name = models.CharField(max_length=100, default="Asif Keloth")
    tagline = models.CharField(max_length=160, default="UI/UX Designer & UI Developer")
    email = models.EmailField(default="hello@example.com")
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=120, default="Kochi, India")
    resume = models.FileField(upload_to="resume/", blank=True, null=True)
    logo_text = models.CharField(max_length=40, default="A")
    footer_note = models.CharField(max_length=200, default="Designed & built with care.")
    # SEO
    seo_title = models.CharField(max_length=70, blank=True,
                                 help_text="Default <title>. Falls back to site name.")
    seo_description = models.CharField(max_length=160, blank=True)
    seo_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"


class HeroSection(SingletonModel):
    eyebrow = models.CharField(max_length=80, default="UI/UX Designer & UI Developer")
    headline_line1 = models.CharField(max_length=80, default="Designing interfaces")
    headline_line2 = models.CharField(max_length=80, default="people love to use.")
    typed_roles = models.CharField(
        max_length=255,
        default="UI Designer,UX Designer,UI Developer,Design Systems Builder",
        help_text="Comma-separated roles for the typing animation.")
    statement = models.TextField(
        default="I turn complex problems into clear, elegant digital products — "
                "from first research sketch to production-ready interface.")
    cta_primary_label = models.CharField(max_length=40, default="View my work")
    cta_primary_url = models.CharField(max_length=200, default="/projects/")
    cta_secondary_label = models.CharField(max_length=40, default="Let's talk")
    cta_secondary_url = models.CharField(max_length=200, default="/contact/")
    portrait = models.ImageField(upload_to="hero/", blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=6)
    projects_shipped = models.PositiveIntegerField(default=48)
    happy_clients = models.PositiveIntegerField(default=32)

    class Meta:
        verbose_name = "Hero section"
        verbose_name_plural = "Hero section"

    def __str__(self):
        return "Hero section"

    @property
    def typed_roles_list(self):
        return [r.strip() for r in self.typed_roles.split(",") if r.strip()]


class AboutSection(SingletonModel):
    intro = models.TextField(
        default="I'm a designer-developer hybrid. I care about the pixel and the "
                "person behind the screen in equal measure.")
    philosophy = models.TextField(
        default="Good design is honest. It removes friction, respects attention, "
                "and earns trust one interaction at a time.")
    portrait = models.ImageField(upload_to="about/", blank=True, null=True)
    values = models.TextField(
        default="Clarity over cleverness|Users before aesthetics|Systems, not screens|Craft in the details",
        help_text="Values separated by | ")

    class Meta:
        verbose_name = "About section"
        verbose_name_plural = "About section"

    def __str__(self):
        return "About section"

    @property
    def values_list(self):
        return [v.strip() for v in self.values.split("|") if v.strip()]


# ------------------------------------------------------------------ ordered
class OrderedModel(models.Model):
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class ProcessStep(OrderedModel):
    """Design process shown on About page (a real sequence)."""
    title = models.CharField(max_length=80)
    description = models.TextField()

    def __str__(self):
        return self.title


class TimelineEntry(OrderedModel):
    KIND_CHOICES = [("work", "Experience"), ("education", "Education")]
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default="work")
    period = models.CharField(max_length=40, help_text="e.g. 2022 — Present")
    title = models.CharField(max_length=120)
    org = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Timeline entries"

    def __str__(self):
        return f"{self.title} · {self.org}"


class Certification(OrderedModel):
    title = models.CharField(max_length=140)
    issuer = models.CharField(max_length=120)
    date = models.CharField(max_length=40, help_text="e.g. 2023 or Jan 2023")
    credential_url = models.URLField(blank=True, help_text="Link to verify the credential")

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Certifications"

    def __str__(self):
        return f"{self.title} · {self.issuer}"


class SkillCategory(OrderedModel):
    name = models.CharField(max_length=60)

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.name


class Skill(OrderedModel):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE,
                                 related_name="skills")
    name = models.CharField(max_length=60)
    level = models.PositiveIntegerField(default=90, help_text="0-100")

    def __str__(self):
        return self.name


class Service(OrderedModel):
    title = models.CharField(max_length=80)
    description = models.TextField()
    icon = models.CharField(max_length=40, default="layout",
                            help_text="Icon key: layout, users, layers, code, "
                                      "smartphone, grid, pen, monitor")

    def __str__(self):
        return self.title


class ClientLogo(OrderedModel):
    name = models.CharField(max_length=80)
    logo = models.ImageField(upload_to="clients/", blank=True, null=True)

    def __str__(self):
        return self.name


class Testimonial(OrderedModel):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=120)
    quote = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SocialLink(OrderedModel):
    PLATFORMS = [
        ("dribbble", "Dribbble"), ("behance", "Behance"), ("linkedin", "LinkedIn"),
        ("github", "GitHub"), ("twitter", "X / Twitter"), ("instagram", "Instagram"),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    url = models.URLField()

    def __str__(self):
        return self.get_platform_display()


# ----------------------------------------------------------------- projects
class ProjectCategory(OrderedModel):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Project categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(OrderedModel):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL,
                                 null=True, related_name="projects")
    year = models.CharField(max_length=10, default="2025")
    client = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=120, default="UI/UX Designer")
    summary = models.CharField(max_length=240)
    cover = models.ImageField(upload_to="projects/", blank=True, null=True)
    accent_hue = models.PositiveIntegerField(
        default=252, help_text="0-360; tints the placeholder cover when no image is set")
    featured = models.BooleanField(default=False)
    live_url = models.URLField(blank=True)
    prototype_url = models.URLField(blank=True, help_text="Figma / prototype embed link")

    # Case-study style sections (all optional; empty sections are hidden)
    overview = models.TextField(blank=True)
    problem = models.TextField(blank=True)
    research = models.TextField(blank=True)
    persona = models.TextField(blank=True, verbose_name="User persona")
    wireframes = models.TextField(blank=True)
    design_process = models.TextField(blank=True)
    high_fidelity = models.TextField(blank=True, verbose_name="High-fidelity UI")
    design_system = models.TextField(blank=True)
    results = models.TextField(blank=True)
    lessons = models.TextField(blank=True, verbose_name="Lessons learned")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.slug])

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Converts raw Behance, Figma, or prototype URLs into embed-safe iframe URLs."""
        if not self.prototype_url:
            return ""
        url = self.prototype_url.strip()
        import re, urllib.parse
        # Behance: https://www.behance.net/gallery/243507527/... -> https://www.behance.net/embed/project/243507527?ilo0=1
        behance_match = re.search(r'behance\.net/(?:gallery|embed/project)/(\d+)', url)
        if behance_match:
            project_id = behance_match.group(1)
            return f"https://www.behance.net/embed/project/{project_id}?ilo0=1"
        # Figma: convert share link to official embed wrapper
        if "figma.com" in url and "figma.com/embed" not in url:
            return f"https://www.figma.com/embed?embed_host=share&url={urllib.parse.quote(url, safe='')}"
        return url

    @property
    def is_behance(self):
        return bool(self.prototype_url and "behance.net" in self.prototype_url)

    @property
    def is_figma(self):
        return bool(self.prototype_url and "figma.com" in self.prototype_url)

    @property
    def sections(self):
        """Ordered (label, body) pairs for non-empty narrative sections."""
        spec = [
            ("Overview", self.overview), ("The problem", self.problem),
            ("Research", self.research), ("User persona", self.persona),
            ("Wireframes", self.wireframes), ("Design process", self.design_process),
            ("High-fidelity UI", self.high_fidelity), ("Design system", self.design_system),
            ("Results", self.results), ("Lessons learned", self.lessons),
        ]
        return [(label, body) for label, body in spec if body.strip()]


class ProjectImage(OrderedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return f"{self.project.title} image {self.order}"


# -------------------------------------------------------------- case studies
class CaseStudy(OrderedModel):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=10, default="2025")
    cover = models.ImageField(upload_to="casestudies/", blank=True, null=True)
    accent_hue = models.PositiveIntegerField(default=200)
    featured = models.BooleanField(default=False)

    summary = models.CharField(max_length=240)
    research = models.TextField(blank=True)
    user_flow = models.TextField(blank=True)
    journey_map = models.TextField(blank=True)
    design_decisions = models.TextField(blank=True)
    prototype = models.TextField(blank=True)
    before_after = models.TextField(blank=True, verbose_name="Before & after")
    outcome = models.TextField(blank=True, verbose_name="Final outcome")

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Case studies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("case_study_detail", args=[self.slug])

    def __str__(self):
        return self.title

    @property
    def sections(self):
        spec = [
            ("Research", self.research), ("User flow", self.user_flow),
            ("Journey map", self.journey_map), ("Design decisions", self.design_decisions),
            ("Prototype", self.prototype), ("Before & after", self.before_after),
            ("Final outcome", self.outcome),
        ]
        return [(label, body) for label, body in spec if body.strip()]


# ------------------------------------------------------------------- inbox
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'no subject'}"
