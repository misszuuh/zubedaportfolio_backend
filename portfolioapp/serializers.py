from rest_framework import serializers
from .models import (
    ServiceRequest, ContactMessage, Project, Skill, ProjectSkill,
    Testimonial, SocialLink, AboutMe
)


class ServiceRequestSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ServiceRequest
        fields = '__all__'
        read_only_fields = ('status', 'submitted_at', 'updated_at')


class ContactMessageSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('status', 'submitted_at', 'updated_at')


class SkillSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Skill
        fields = '__all__'


class ProjectSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_icon = serializers.CharField(source='skill.icon', read_only=True)
    skill_category = serializers.CharField(source='skill.category', read_only=True)

    class Meta:
        model = ProjectSkill
        fields = ['id', 'skill', 'skill_name', 'skill_icon', 'skill_category']


class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    testimonial_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'detailed_description', 'image', 'thumbnail',
            'code_link', 'demo_link', 'status', 'status_display', 'order', 'is_featured',
            'skills', 'testimonial_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')

    def get_skills(self, obj):
        project_skills = obj.project_skills.all()
        return ProjectSkillSerializer(project_skills, many=True).data

    def get_testimonial_count(self, obj):
        return obj.testimonials.filter(is_active=True).count()


class ProjectListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    skills = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'thumbnail', 'code_link', 'demo_link',
            'status', 'status_display', 'is_featured', 'skills', 'created_at'
        ]

    def get_skills(self, obj):
        # Return only skill names for list view
        return [ps.skill.name for ps in obj.project_skills.all()]


class TestimonialSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True, allow_null=True)

    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'client_position', 'client_company', 'client_image',
            'testimonial', 'rating', 'project', 'project_name', 'is_featured',
            'is_active', 'created_at'
        ]
        read_only_fields = ('created_at',)


class SocialLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)

    class Meta:
        model = SocialLink
        fields = '__all__'


class AboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMe
        fields = '__all__'
        read_only_fields = ('updated_at',)