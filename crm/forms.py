from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from core import models as m


class StyledFormMixin:
    """Adds a consistent CSS class to every field widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "field-check")
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs.setdefault("class", "field-input")
                widget.clear_checkbox_label = "Remove current file"
            else:
                widget.attrs.setdefault("class", "field-input")


class DashboardLoginForm(StyledFormMixin, AuthenticationForm):
    pass


class DashboardPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass


class UsernameChangeForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username"]


class AboutForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.AboutSection
        fields = ["intro", "philosophy", "portrait", "values"]
        widgets = {
            "intro": forms.Textarea(attrs={"rows": 3}),
            "philosophy": forms.Textarea(attrs={"rows": 3}),
            "values": forms.Textarea(attrs={"rows": 2}),
        }
        help_texts = {"values": "Separate each value with a | character."}


class HeroForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.HeroSection
        fields = [
            "eyebrow", "headline_line1", "headline_line2", "typed_roles",
            "statement", "cta_primary_label", "cta_primary_url",
            "cta_secondary_label", "cta_secondary_url",
            "years_experience", "projects_shipped", "happy_clients",
        ]
        widgets = {"statement": forms.Textarea(attrs={"rows": 3})}
        help_texts = {"typed_roles": "Comma-separated roles for the typing animation."}


class SiteSettingsForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.SiteSettings
        fields = [
            "site_name", "tagline", "email", "phone", "location",
            "logo_text", "footer_note", "seo_title", "seo_description",
            "seo_keywords", "og_image",
        ]


class ResumeForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.SiteSettings
        fields = ["resume"]


class SkillCategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.SkillCategory
        fields = ["name", "order", "is_active"]


class SkillForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.Skill
        fields = ["name", "order", "is_active"]


class TimelineForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.TimelineEntry
        fields = ["period", "title", "org", "description", "order", "is_active"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class CertificationForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.Certification
        fields = ["title", "issuer", "date", "credential_url", "order", "is_active"]


class TestimonialForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.Testimonial
        fields = ["name", "role", "quote", "rating", "avatar", "featured", "order", "is_active"]
        widgets = {"quote": forms.Textarea(attrs={"rows": 3})}


class ProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.Project
        fields = [
            "title", "category", "role", "summary", "cover",
            "featured", "live_url", "prototype_url", "order", "is_active",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 2}),
        }


class ProjectCategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.ProjectCategory
        fields = ["name", "order", "is_active"]


class SocialLinkForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.SocialLink
        fields = ["platform", "url", "order", "is_active"]


class ServiceForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.Service
        fields = ["title", "description", "icon", "order", "is_active"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class ClientLogoForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = m.ClientLogo
        fields = ["name", "logo", "order", "is_active"]
