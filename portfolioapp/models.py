from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator


class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('api', 'API Development'),
        ('design', 'UI/UX Design'),
        ('consulting', 'Consulting'),
        ('devops', 'DevOps & Deployment'),
    ]

    TIMELINE_CHOICES = [
        ('asap', 'As soon as possible'),
        ('2-4 weeks', '2-4 weeks'),
        ('1-2 months', '1-2 months'),
        ('2-3 months', '2-3 months'),
        ('3+ months', '3+ months'),
        ('flexible', 'Flexible'),
    ]

    BUDGET_CHOICES = [
        ('Under $1,000', 'Under $1,000'),
        ('$1,000 - $2,500', '$1,000 - $2,500'),
        ('$2,500 - $5,000', '$2,500 - $5,000'),
        ('$5,000 - $10,000', '$5,000 - $10,000'),
        ('$10,000+', '$10,000+'),
        ('not-sure', 'Not sure / Need quote'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    project_requirements = models.TextField()
    preferred_timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, blank=True)
    budget_range = models.CharField(max_length=50, choices=BUDGET_CHOICES, blank=True)
    agree_to_terms = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

    def __str__(self):
        return f"{self.full_name} - {self.get_service_type_display()}"


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    detailed_description = models.TextField(blank=True, help_text="Detailed project description")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True, null=True)
    code_link = models.URLField(blank=True, validators=[URLValidator()])
    demo_link = models.URLField(blank=True, validators=[URLValidator()])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    order = models.IntegerField(default=0, help_text="Order in which projects appear")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('mobile', 'Mobile'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency level (0-100)"
    )
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name or emoji")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class ProjectSkill(models.Model):
    """Many-to-many relationship between Projects and Skills"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='project_skills')

    class Meta:
        unique_together = ['project', 'skill']
        verbose_name = 'Project Skill'
        verbose_name_plural = 'Project Skills'

    def __str__(self):
        return f"{self.project.name} - {self.skill.name}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=255)
    client_position = models.CharField(max_length=255, blank=True)
    client_company = models.CharField(max_length=255, blank=True)
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    testimonial = models.TextField()
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating (1-5 stars)"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials'
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('email', 'Email'),
        ('website', 'Website'),
        ('other', 'Other'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField(validators=[URLValidator()])
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name or emoji")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'platform']
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'

    def __str__(self):
        return f"{self.get_platform_display()}"


class AboutMe(models.Model):
    """Singleton model for About Me section"""
    title = models.CharField(max_length=255, default="About Me")
    bio = models.TextField(help_text="Short bio")
    detailed_bio = models.TextField(blank=True, help_text="Detailed biography")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Me'
        verbose_name_plural = 'About Me'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (Singleton pattern)
        if not self.pk and AboutMe.objects.exists():
            raise ValueError("Only one AboutMe instance is allowed")
        return super(AboutMe, self).save(*args, **kwargs)