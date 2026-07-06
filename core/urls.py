from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("case-studies/", views.case_studies, name="case_studies"),
    path("case-studies/<slug:slug>/", views.case_study_detail, name="case_study_detail"),
    path("skills/", views.skills, name="skills"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("contact/", views.contact, name="contact"),
]
