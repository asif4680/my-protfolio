from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from . import models
from .forms import ContactForm


def home(request):
    return render(request, "home.html", {
        "hero": models.HeroSection.load(),
        "about": models.AboutSection.load(),
        "featured_projects": models.Project.objects.filter(
            is_active=True, featured=True)[:4],
        "skill_categories": models.SkillCategory.objects.filter(
            is_active=True).prefetch_related("skills"),
        "services": models.Service.objects.filter(is_active=True)[:4],
        "experience": models.TimelineEntry.objects.filter(
            is_active=True, kind="work"),
        "education": models.TimelineEntry.objects.filter(
            is_active=True, kind="education")[:3],
        "certifications": models.Certification.objects.filter(is_active=True)[:3],
    })


def about(request):
    return render(request, "about.html", {
        "about": models.AboutSection.load(),
        "hero": models.HeroSection.load(),
        "process_steps": models.ProcessStep.objects.filter(is_active=True),
        "experience": models.TimelineEntry.objects.filter(is_active=True, kind="work"),
        "education": models.TimelineEntry.objects.filter(is_active=True, kind="education"),
        "certifications": models.Certification.objects.filter(is_active=True),
    })


def projects(request):
    qs = models.Project.objects.filter(is_active=True)
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("category", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) |
                       Q(client__icontains=q))
    if cat:
        qs = qs.filter(category__slug=cat)
    return render(request, "projects.html", {
        "projects": qs,
        "query": q,
    })


def project_detail(request, slug):
    project = get_object_or_404(models.Project, slug=slug, is_active=True)
    nxt = (models.Project.objects.filter(is_active=True, order__gt=project.order)
           .exclude(pk=project.pk).first()
           or models.Project.objects.filter(is_active=True).exclude(pk=project.pk).first())
    return render(request, "project_detail.html", {"project": project, "next_project": nxt})


def case_studies(request):
    return render(request, "case_studies.html", {
        "case_studies": models.CaseStudy.objects.filter(is_active=True),
    })


def case_study_detail(request, slug):
    cs = get_object_or_404(models.CaseStudy, slug=slug, is_active=True)
    return render(request, "case_study_detail.html", {"cs": cs})


def skills(request):
    return render(request, "skills.html", {
        "skill_categories": models.SkillCategory.objects.filter(
            is_active=True).prefetch_related("skills"),
        "services": models.Service.objects.filter(is_active=True),
    })


def testimonials(request):
    return render(request, "testimonials.html", {
        "testimonials": models.Testimonial.objects.filter(is_active=True),
    })


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Message sent — I'll reply within one business day.")
        return redirect("contact")
    return render(request, "contact.html", {"form": form})
