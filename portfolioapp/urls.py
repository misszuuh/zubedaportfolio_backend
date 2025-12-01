from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'skills', views.SkillViewSet, basename='skill')
router.register(r'testimonials', views.TestimonialViewSet, basename='testimonial')
router.register(r'social-links', views.SocialLinkViewSet, basename='social-link')
router.register(r'about-me', views.AboutMeViewSet, basename='about-me')

urlpatterns = [
    # API router (REST endpoints for CRUD operations)
    path('api/', include(router.urls)),

    # Form submission endpoints
    path('api/service-request/', views.submit_service_request, name='service-request'),
    path('api/contact-message/', views.submit_contact_message, name='contact-message'),
]