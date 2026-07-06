from django.contrib import messages as flash
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core import models as m
from . import forms


# --------------------------------------------------------------------- auth
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = forms.DashboardLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        return redirect("dashboard:home")
    return render(request, "dashboard/login.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("dashboard:login")


class StaffRequired(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "dashboard:login"

    def test_func(self):
        return self.request.user.is_staff


def staff_required_view(view_func):
    """Function-view equivalent of StaffRequired, for the simple pages below."""
    from django.contrib.auth.decorators import login_required, user_passes_test
    return login_required(login_url="dashboard:login")(
        user_passes_test(lambda u: u.is_staff, login_url="dashboard:login")(view_func)
    )


@staff_required_view
def account_settings(request):
    return render(request, "dashboard/account.html", {
        "username_form": forms.UsernameChangeForm(instance=request.user),
        "password_form": forms.DashboardPasswordChangeForm(request.user),
        "active": "account",
    })


@staff_required_view
def username_change(request):
    username_form = forms.UsernameChangeForm(request.POST or None, instance=request.user)
    if request.method == "POST" and username_form.is_valid():
        username_form.save()
        flash.success(request, "Username updated.")
        return redirect("dashboard:account")
    return render(request, "dashboard/account.html", {
        "username_form": username_form,
        "password_form": forms.DashboardPasswordChangeForm(request.user),
        "active": "account",
    })


@staff_required_view
def password_change(request):
    password_form = forms.DashboardPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and password_form.is_valid():
        user = password_form.save()
        update_session_auth_hash(request, user)
        flash.success(request, "Password updated.")
        return redirect("dashboard:account")
    return render(request, "dashboard/account.html", {
        "username_form": forms.UsernameChangeForm(instance=request.user),
        "password_form": password_form,
        "active": "account",
    })


# ------------------------------------------------------------------- home
@staff_required_view
def home(request):
    return render(request, "dashboard/home.html", {
        "counts": {
            "projects": m.Project.objects.count(),
            "skills": m.Skill.objects.count(),
            "experience": m.TimelineEntry.objects.filter(kind="work").count(),
            "education": m.TimelineEntry.objects.filter(kind="education").count(),
            "certifications": m.Certification.objects.count(),
            "testimonials": m.Testimonial.objects.count(),
            "unread_messages": m.ContactMessage.objects.filter(is_read=False).count(),
        },
        "recent_messages": m.ContactMessage.objects.all()[:5],
        "active": "home",
    })


# --------------------------------------------------------- profile / site
@staff_required_view
def profile_edit(request):
    about = m.AboutSection.load()
    hero = m.HeroSection.load()
    about_form = forms.AboutForm(request.POST or None, request.FILES or None,
                                  instance=about, prefix="about")
    hero_form = forms.HeroForm(request.POST or None, request.FILES or None,
                                instance=hero, prefix="hero")
    if request.method == "POST":
        if about_form.is_valid() and hero_form.is_valid():
            about_form.save()
            hero_form.save()
            flash.success(request, "Profile & bio updated.")
            return redirect("dashboard:profile")
    return render(request, "dashboard/profile.html", {
        "about_form": about_form, "hero_form": hero_form, "active": "profile",
    })


@staff_required_view
def resume_edit(request):
    site = m.SiteSettings.load()
    form = forms.ResumeForm(request.POST or None, request.FILES or None, instance=site)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Resume updated.")
        return redirect("dashboard:resume")
    return render(request, "dashboard/resume.html", {"form": form, "site": site, "active": "resume"})


@staff_required_view
def site_settings_edit(request):
    site = m.SiteSettings.load()
    form = forms.SiteSettingsForm(request.POST or None, request.FILES or None, instance=site)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Site settings updated.")
        return redirect("dashboard:settings")
    return render(request, "dashboard/form.html", {
        "form": form, "title": "Site settings",
        "back_url": "dashboard:home", "active": "settings",
    })


# --------------------------------------------------------------- messages
@staff_required_view
def message_list(request):
    return render(request, "dashboard/messages.html", {
        "messages_list": m.ContactMessage.objects.all(), "active": "messages",
    })


@staff_required_view
def message_detail(request, pk):
    msg = get_object_or_404(m.ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=["is_read"])
    return render(request, "dashboard/message_detail.html", {"msg": msg, "active": "messages"})


@staff_required_view
def message_delete(request, pk):
    msg = get_object_or_404(m.ContactMessage, pk=pk)
    if request.method == "POST":
        msg.delete()
        flash.success(request, "Message deleted.")
        return redirect("dashboard:message_list")
    return render(request, "dashboard/confirm_delete.html", {
        "object": msg, "back_url": "dashboard:message_list", "active": "messages",
    })


# ------------------------------------------------------------------ skills
@staff_required_view
def skills_home(request):
    return render(request, "dashboard/skills.html", {
        "categories": m.SkillCategory.objects.prefetch_related("skills"), "active": "skills",
    })


@staff_required_view
def skill_category_add(request):
    form = forms.SkillCategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Skill category added.")
        return redirect("dashboard:skills")
    return render(request, "dashboard/form.html", {
        "form": form, "title": "Add skill category", "back_url": "dashboard:skills", "active": "skills",
    })


@staff_required_view
def skill_category_edit(request, pk):
    obj = get_object_or_404(m.SkillCategory, pk=pk)
    form = forms.SkillCategoryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Skill category updated.")
        return redirect("dashboard:skills")
    return render(request, "dashboard/form.html", {
        "form": form, "title": "Edit skill category", "back_url": "dashboard:skills", "active": "skills",
    })


@staff_required_view
def skill_category_delete(request, pk):
    obj = get_object_or_404(m.SkillCategory, pk=pk)
    if request.method == "POST":
        obj.delete()
        flash.success(request, "Skill category deleted.")
        return redirect("dashboard:skills")
    return render(request, "dashboard/confirm_delete.html", {
        "object": obj, "back_url": "dashboard:skills", "active": "skills",
    })


@staff_required_view
def skill_add(request, category_id):
    category = get_object_or_404(m.SkillCategory, pk=category_id)
    form = forms.SkillForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        skill = form.save(commit=False)
        skill.category = category
        skill.save()
        flash.success(request, "Skill added.")
        return redirect("dashboard:skills")
    return render(request, "dashboard/form.html", {
        "form": form, "title": f"Add skill to {category.name}", "back_url": "dashboard:skills", "active": "skills",
    })


@staff_required_view
def skill_edit(request, pk):
    obj = get_object_or_404(m.Skill, pk=pk)
    form = forms.SkillForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        flash.success(request, "Skill updated.")
        return redirect("dashboard:skills")
    return render(request, "dashboard/form.html", {
        "form": form, "title": "Edit skill", "back_url": "dashboard:skills", "active": "skills",
    })


@staff_required_view
def skill_delete(request, pk):
    obj = get_object_or_404(m.Skill, pk=pk)
    if request.method == "POST":
        obj.delete()
        flash.success(request, "Skill deleted.")
        return redirect("dashboard:skills")
    return render(request, "dashboard/confirm_delete.html", {
        "object": obj, "back_url": "dashboard:skills", "active": "skills",
    })


# --------------------------------------------------------- generic CRUD sets
class SimpleListView(StaffRequired, ListView):
    template_name = "dashboard/simple_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.extra)
        return ctx


class SimpleCreateView(StaffRequired, CreateView):
    template_name = "dashboard/form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.extra)
        return ctx


class SimpleUpdateView(StaffRequired, UpdateView):
    template_name = "dashboard/form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.extra)
        return ctx


class SimpleDeleteView(StaffRequired, DeleteView):
    template_name = "dashboard/confirm_delete.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.extra)
        return ctx


# ---- Experience (TimelineEntry, kind="work") ----
class ExperienceListView(SimpleListView):
    model = m.TimelineEntry
    extra = {"title": "Experience", "add_url": "dashboard:experience_add",
             "edit_url": "dashboard:experience_edit", "delete_url": "dashboard:experience_delete", "active": "experience"}

    def get_queryset(self):
        return m.TimelineEntry.objects.filter(kind="work")


class ExperienceCreateView(SimpleCreateView):
    model = m.TimelineEntry
    form_class = forms.TimelineForm
    success_url = reverse_lazy("dashboard:experience_list")
    extra = {"title": "Add experience", "back_url": "dashboard:experience_list", "active": "experience"}

    def form_valid(self, form):
        form.instance.kind = "work"
        flash.success(self.request, "Experience added.")
        return super().form_valid(form)


class ExperienceUpdateView(SimpleUpdateView):
    model = m.TimelineEntry
    form_class = forms.TimelineForm
    success_url = reverse_lazy("dashboard:experience_list")
    extra = {"title": "Edit experience", "back_url": "dashboard:experience_list", "active": "experience"}

    def get_queryset(self):
        return m.TimelineEntry.objects.filter(kind="work")

    def form_valid(self, form):
        flash.success(self.request, "Experience updated.")
        return super().form_valid(form)


class ExperienceDeleteView(SimpleDeleteView):
    model = m.TimelineEntry
    success_url = reverse_lazy("dashboard:experience_list")
    extra = {"back_url": "dashboard:experience_list", "active": "experience"}

    def get_queryset(self):
        return m.TimelineEntry.objects.filter(kind="work")

    def delete(self, request, *args, **kwargs):
        resp = super().delete(request, *args, **kwargs)
        flash.success(self.request, "Experience deleted.")
        return resp


# ---- Education (TimelineEntry, kind="education") ----
class EducationListView(SimpleListView):
    model = m.TimelineEntry
    extra = {"title": "Education", "add_url": "dashboard:education_add",
             "edit_url": "dashboard:education_edit", "delete_url": "dashboard:education_delete", "active": "education"}

    def get_queryset(self):
        return m.TimelineEntry.objects.filter(kind="education")


class EducationCreateView(SimpleCreateView):
    model = m.TimelineEntry
    form_class = forms.TimelineForm
    success_url = reverse_lazy("dashboard:education_list")
    extra = {"title": "Add education", "back_url": "dashboard:education_list", "active": "education"}

    def form_valid(self, form):
        form.instance.kind = "education"
        flash.success(self.request, "Education added.")
        return super().form_valid(form)


class EducationUpdateView(SimpleUpdateView):
    model = m.TimelineEntry
    form_class = forms.TimelineForm
    success_url = reverse_lazy("dashboard:education_list")
    extra = {"title": "Edit education", "back_url": "dashboard:education_list", "active": "education"}

    def get_queryset(self):
        return m.TimelineEntry.objects.filter(kind="education")

    def form_valid(self, form):
        flash.success(self.request, "Education updated.")
        return super().form_valid(form)


class EducationDeleteView(SimpleDeleteView):
    model = m.TimelineEntry
    success_url = reverse_lazy("dashboard:education_list")
    extra = {"back_url": "dashboard:education_list", "active": "education"}

    def get_queryset(self):
        return m.TimelineEntry.objects.filter(kind="education")

    def delete(self, request, *args, **kwargs):
        resp = super().delete(request, *args, **kwargs)
        flash.success(self.request, "Education deleted.")
        return resp


# ---- Certifications ----
class CertificationListView(SimpleListView):
    model = m.Certification
    extra = {"title": "Certifications", "add_url": "dashboard:certification_add",
             "edit_url": "dashboard:certification_edit", "delete_url": "dashboard:certification_delete", "active": "certifications"}


class CertificationCreateView(SimpleCreateView):
    model = m.Certification
    form_class = forms.CertificationForm
    success_url = reverse_lazy("dashboard:certification_list")
    extra = {"title": "Add certification", "back_url": "dashboard:certification_list", "active": "certifications"}

    def form_valid(self, form):
        flash.success(self.request, "Certification added.")
        return super().form_valid(form)


class CertificationUpdateView(SimpleUpdateView):
    model = m.Certification
    form_class = forms.CertificationForm
    success_url = reverse_lazy("dashboard:certification_list")
    extra = {"title": "Edit certification", "back_url": "dashboard:certification_list", "active": "certifications"}

    def form_valid(self, form):
        flash.success(self.request, "Certification updated.")
        return super().form_valid(form)


class CertificationDeleteView(SimpleDeleteView):
    model = m.Certification
    success_url = reverse_lazy("dashboard:certification_list")
    extra = {"back_url": "dashboard:certification_list", "active": "certifications"}

    def delete(self, request, *args, **kwargs):
        resp = super().delete(request, *args, **kwargs)
        flash.success(self.request, "Certification deleted.")
        return resp


# ---- Testimonials ----
class TestimonialListView(SimpleListView):
    model = m.Testimonial
    extra = {"title": "Testimonials", "add_url": "dashboard:testimonial_add",
             "edit_url": "dashboard:testimonial_edit", "delete_url": "dashboard:testimonial_delete", "active": "testimonials"}


class TestimonialCreateView(SimpleCreateView):
    model = m.Testimonial
    form_class = forms.TestimonialForm
    success_url = reverse_lazy("dashboard:testimonial_list")
    extra = {"title": "Add testimonial", "back_url": "dashboard:testimonial_list", "active": "testimonials"}

    def form_valid(self, form):
        flash.success(self.request, "Testimonial added.")
        return super().form_valid(form)


class TestimonialUpdateView(SimpleUpdateView):
    model = m.Testimonial
    form_class = forms.TestimonialForm
    success_url = reverse_lazy("dashboard:testimonial_list")
    extra = {"title": "Edit testimonial", "back_url": "dashboard:testimonial_list", "active": "testimonials"}

    def form_valid(self, form):
        flash.success(self.request, "Testimonial updated.")
        return super().form_valid(form)


class TestimonialDeleteView(SimpleDeleteView):
    model = m.Testimonial
    success_url = reverse_lazy("dashboard:testimonial_list")
    extra = {"back_url": "dashboard:testimonial_list", "active": "testimonials"}

    def delete(self, request, *args, **kwargs):
        resp = super().delete(request, *args, **kwargs)
        flash.success(self.request, "Testimonial deleted.")
        return resp


# ---- Projects ----
class ProjectListView(SimpleListView):
    model = m.Project
    extra = {"title": "Projects", "add_url": "dashboard:project_add",
             "edit_url": "dashboard:project_edit", "delete_url": "dashboard:project_delete", "active": "projects"}


class ProjectCreateView(SimpleCreateView):
    model = m.Project
    form_class = forms.ProjectForm
    success_url = reverse_lazy("dashboard:project_list")
    extra = {"title": "Add project", "back_url": "dashboard:project_list", "active": "projects"}

    def form_valid(self, form):
        flash.success(self.request, "Project added.")
        return super().form_valid(form)


class ProjectUpdateView(SimpleUpdateView):
    model = m.Project
    form_class = forms.ProjectForm
    success_url = reverse_lazy("dashboard:project_list")
    extra = {"title": "Edit project", "back_url": "dashboard:project_list", "active": "projects"}

    def form_valid(self, form):
        flash.success(self.request, "Project updated.")
        return super().form_valid(form)


class ProjectDeleteView(SimpleDeleteView):
    model = m.Project
    success_url = reverse_lazy("dashboard:project_list")
    extra = {"back_url": "dashboard:project_list", "active": "projects"}

    def delete(self, request, *args, **kwargs):
        resp = super().delete(request, *args, **kwargs)
        flash.success(self.request, "Project deleted.")
        return resp


# ---- Social links (shown inside Settings) ----
class SocialLinkListView(SimpleListView):
    model = m.SocialLink
    extra = {"title": "Social links", "add_url": "dashboard:social_link_add",
             "edit_url": "dashboard:social_link_edit", "delete_url": "dashboard:social_link_delete", "active": "social"}


class SocialLinkCreateView(SimpleCreateView):
    model = m.SocialLink
    form_class = forms.SocialLinkForm
    success_url = reverse_lazy("dashboard:social_link_list")
    extra = {"title": "Add social link", "back_url": "dashboard:social_link_list", "active": "social"}

    def form_valid(self, form):
        flash.success(self.request, "Social link added.")
        return super().form_valid(form)


class SocialLinkUpdateView(SimpleUpdateView):
    model = m.SocialLink
    form_class = forms.SocialLinkForm
    success_url = reverse_lazy("dashboard:social_link_list")
    extra = {"title": "Edit social link", "back_url": "dashboard:social_link_list", "active": "social"}

    def form_valid(self, form):
        flash.success(self.request, "Social link updated.")
        return super().form_valid(form)


class SocialLinkDeleteView(SimpleDeleteView):
    model = m.SocialLink
    success_url = reverse_lazy("dashboard:social_link_list")
    extra = {"back_url": "dashboard:social_link_list", "active": "social"}

    def delete(self, request, *args, **kwargs):
        resp = super().delete(request, *args, **kwargs)
        flash.success(self.request, "Social link deleted.")
        return resp
