from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'contact', views.ContactViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'experience', views.ExperienceViewSet)
router.register(r'certifications', views.CertificationViewSet)
router.register(r'education', views.EducationViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('personal-info/', views.personal_info, name='personal-info'),
    path('about/', views.about_info, name='about-info'),
    path('social-links/', views.social_links, name='social-links'),
    path('portfolio-summary/', views.portfolio_summary, name='portfolio-summary'),
    path('health/', views.health_check, name='health-check'),
]
