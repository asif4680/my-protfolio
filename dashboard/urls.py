from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/", views.account_settings, name="account"),
    path("account/username/", views.username_change, name="username_change"),
    path("account/password/", views.password_change, name="password_change"),

    path("profile/", views.profile_edit, name="profile"),
    path("resume/", views.resume_edit, name="resume"),
    path("settings/", views.site_settings_edit, name="settings"),

    path("messages/", views.message_list, name="message_list"),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("messages/<int:pk>/delete/", views.message_delete, name="message_delete"),

    path("skills/", views.skills_home, name="skills"),
    path("skills/category/add/", views.skill_category_add, name="skill_category_add"),
    path("skills/category/<int:pk>/edit/", views.skill_category_edit, name="skill_category_edit"),
    path("skills/category/<int:pk>/delete/", views.skill_category_delete, name="skill_category_delete"),
    path("skills/add/<int:category_id>/", views.skill_add, name="skill_add"),
    path("skills/<int:pk>/edit/", views.skill_edit, name="skill_edit"),
    path("skills/<int:pk>/delete/", views.skill_delete, name="skill_delete"),

    path("experience/", views.ExperienceListView.as_view(), name="experience_list"),
    path("experience/add/", views.ExperienceCreateView.as_view(), name="experience_add"),
    path("experience/<int:pk>/edit/", views.ExperienceUpdateView.as_view(), name="experience_edit"),
    path("experience/<int:pk>/delete/", views.ExperienceDeleteView.as_view(), name="experience_delete"),

    path("education/", views.EducationListView.as_view(), name="education_list"),
    path("education/add/", views.EducationCreateView.as_view(), name="education_add"),
    path("education/<int:pk>/edit/", views.EducationUpdateView.as_view(), name="education_edit"),
    path("education/<int:pk>/delete/", views.EducationDeleteView.as_view(), name="education_delete"),

    path("certifications/", views.CertificationListView.as_view(), name="certification_list"),
    path("certifications/add/", views.CertificationCreateView.as_view(), name="certification_add"),
    path("certifications/<int:pk>/edit/", views.CertificationUpdateView.as_view(), name="certification_edit"),
    path("certifications/<int:pk>/delete/", views.CertificationDeleteView.as_view(), name="certification_delete"),

    path("testimonials/", views.TestimonialListView.as_view(), name="testimonial_list"),
    path("testimonials/add/", views.TestimonialCreateView.as_view(), name="testimonial_add"),
    path("testimonials/<int:pk>/edit/", views.TestimonialUpdateView.as_view(), name="testimonial_edit"),
    path("testimonials/<int:pk>/delete/", views.TestimonialDeleteView.as_view(), name="testimonial_delete"),

    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path("projects/add/", views.ProjectCreateView.as_view(), name="project_add"),
    path("projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path("projects/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),

    path("social-links/", views.SocialLinkListView.as_view(), name="social_link_list"),
    path("social-links/add/", views.SocialLinkCreateView.as_view(), name="social_link_add"),
    path("social-links/<int:pk>/edit/", views.SocialLinkUpdateView.as_view(), name="social_link_edit"),
    path("social-links/<int:pk>/delete/", views.SocialLinkDeleteView.as_view(), name="social_link_delete"),
]
