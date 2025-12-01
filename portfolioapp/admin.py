from django.contrib import admin
from .models import (
    ServiceRequest, ContactMessage, Project, Skill, ProjectSkill,
    Testimonial, SocialLink, AboutMe
)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'service_type', 'status', 'submitted_at']
    list_filter = ['service_type', 'status', 'preferred_timeline', 'submitted_at']
    search_fields = ['full_name', 'email', 'project_requirements']
    readonly_fields = ['submitted_at', 'updated_at']
    list_editable = ['status']
    date_hierarchy = 'submitted_at'

    fieldsets = (
        ('Client Information', {
            'fields': ('full_name', 'email')
        }),
        ('Service Details', {
            'fields': ('service_type', 'project_requirements', 'preferred_timeline', 'budget_range')
        }),
        ('Status', {
            'fields': ('status', 'agree_to_terms')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'status', 'submitted_at']
    list_filter = ['status', 'submitted_at']
    search_fields = ['full_name', 'email', 'subject', 'message']
    readonly_fields = ['submitted_at', 'updated_at']
    list_editable = ['status']
    date_hierarchy = 'submitted_at'

    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 1
    autocomplete_fields = ['skill']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'is_featured', 'order', 'created_at']
    list_filter = ['status', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['status', 'is_featured', 'order']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [ProjectSkillInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'detailed_description')
        }),
        ('Media', {
            'fields': ('image', 'thumbnail')
        }),
        ('Links', {
            'fields': ('code_link', 'demo_link')
        }),
        ('Display Settings', {
            'fields': ('status', 'order', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    list_editable = ['proficiency', 'order', 'is_active']
    ordering = ['order', 'name']


@admin.register(ProjectSkill)
class ProjectSkillAdmin(admin.ModelAdmin):
    list_display = ['project', 'skill']
    list_filter = ['project', 'skill']
    search_fields = ['project__name', 'skill__name']
    autocomplete_fields = ['project', 'skill']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['client_name', 'client_company', 'testimonial']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    autocomplete_fields = ['project']

    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_image')
        }),
        ('Testimonial', {
            'fields': ('testimonial', 'rating', 'project')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'order', 'is_active']
    list_filter = ['platform', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    readonly_fields = ['updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'bio', 'detailed_bio', 'profile_image')
        }),
        ('Professional Details', {
            'fields': ('years_of_experience', 'resume_file')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        return not AboutMe.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
