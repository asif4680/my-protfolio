from django.contrib import admin
from . import models

admin.site.site_header = "Studio Console"
admin.site.site_title = "Studio Console"
admin.site.index_title = "Portfolio content"


class SingletonAdmin(admin.ModelAdmin):
    """Hide add/delete; clicking the model opens the single row directly."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        from django.shortcuts import redirect
        from django.urls import reverse
        meta = self.model._meta
        return redirect(reverse(
            f"admin:{meta.app_label}_{meta.model_name}_change", args=[obj.pk]))


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Identity", {"fields": ("site_name", "tagline", "logo_text", "footer_note")}),
        ("Contact", {"fields": ("email", "phone", "location")}),
        ("Resume", {"fields": ("resume",)}),
        ("SEO", {"fields": ("seo_title", "seo_description", "seo_keywords", "og_image")}),
    )


@admin.register(models.HeroSection)
class HeroAdmin(SingletonAdmin):
    pass


@admin.register(models.AboutSection)
class AboutAdmin(SingletonAdmin):
    pass


class ProjectImageInline(admin.TabularInline):
    model = models.ProjectImage
    extra = 1


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "year", "featured", "is_active", "order")
    list_editable = ("featured", "is_active", "order")
    list_filter = ("category", "featured", "is_active")
    search_fields = ("title", "summary", "client")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    fieldsets = (
        ("Card", {"fields": ("title", "slug", "category", "year", "client", "role",
                             "summary", "cover", "accent_hue", "featured",
                             "live_url", "prototype_url", "order", "is_active")}),
        ("Case study sections", {"fields": (
            "overview", "problem", "research", "persona", "wireframes",
            "design_process", "high_fidelity", "design_system", "results", "lessons")}),
    )


@admin.register(models.CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "featured", "is_active", "order")
    list_editable = ("featured", "is_active", "order")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


class SkillInline(admin.TabularInline):
    model = models.Skill
    extra = 1


@admin.register(models.SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    inlines = [SkillInline]


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "rating", "featured", "order", "is_active")
    list_editable = ("featured", "order", "is_active")


@admin.register(models.ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(models.SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(models.ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(models.TimelineEntry)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ("title", "org", "kind", "period", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("kind",)


@admin.register(models.Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "date", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")

    def has_add_permission(self, request):
        return False
