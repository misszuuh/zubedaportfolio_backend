from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    ServiceRequest, ContactMessage, Project, Skill,
    Testimonial, SocialLink, AboutMe
)
from .serializers import (
    ServiceRequestSerializer, ContactMessageSerializer,
    ProjectSerializer, ProjectListSerializer, SkillSerializer,
    TestimonialSerializer, SocialLinkSerializer, AboutMeSerializer
)


# ViewSets for comprehensive CRUD operations
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing projects.
    List view returns published projects only.
    Supports filtering, searching, and ordering.
    """
    queryset = Project.objects.filter(status='published')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_featured', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'created_at', 'name']
    ordering = ['order', '-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects only"""
        featured = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing skills.
    Supports filtering by category.
    """
    queryset = Skill.objects.filter(is_active=True)
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    ordering_fields = ['order', 'name', 'proficiency']
    ordering = ['order', 'name']

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get skills grouped by category"""
        skills = self.get_queryset()
        categories = {}
        for skill in skills:
            category = skill.get_category_display()
            if category not in categories:
                categories[category] = []
            categories[category].append(SkillSerializer(skill).data)
        return Response(categories)


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing testimonials.
    List view returns active testimonials only.
    """
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating', 'is_featured', 'project']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured testimonials only"""
        featured = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)


class SocialLinkViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing social links"""
    queryset = SocialLink.objects.filter(is_active=True)
    serializer_class = SocialLinkSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['order']


class AboutMeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing About Me information"""
    queryset = AboutMe.objects.all()
    serializer_class = AboutMeSerializer

    @action(detail=False, methods=['get'])
    def info(self, request):
        """Get the About Me information (singleton)"""
        try:
            about_me = AboutMe.objects.first()
            if about_me:
                serializer = self.get_serializer(about_me)
                return Response(serializer.data)
            return Response(
                {'detail': 'About Me information not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Function-based views for form submissions
@api_view(['POST'])
def submit_service_request(request):
    """Handle service request form submission"""
    serializer = ServiceRequestSerializer(data=request.data)
    if serializer.is_valid():
        try:
            service_request = serializer.save()

            # Send email notification
            service_type = dict(ServiceRequest.SERVICE_TYPES).get(
                service_request.service_type,
                service_request.service_type
            )
            timeline = dict(ServiceRequest.TIMELINE_CHOICES).get(
                service_request.preferred_timeline,
                'Not specified'
            )
            budget = dict(ServiceRequest.BUDGET_CHOICES).get(
                service_request.budget_range,
                'Not specified'
            )

            subject = f"🛠️ New Service Request: {service_type}"
            message = f"""
═══════════════════════════════════════════════════
NEW SERVICE REQUEST
═══════════════════════════════════════════════════

SERVICE TYPE: {service_type}

FROM: {service_request.full_name}
EMAIL: {service_request.email}

───────────────────────────────────────────────────
PROJECT REQUIREMENTS:
───────────────────────────────────────────────────

{service_request.project_requirements}

───────────────────────────────────────────────────
PROJECT DETAILS:
───────────────────────────────────────────────────

Preferred Timeline: {timeline}
Budget Range: {budget}

───────────────────────────────────────────────────
SUBMITTED: {service_request.submitted_at.strftime('%B %d, %Y at %I:%M %p UTC')}
───────────────────────────────────────────────────

💡 TIP: Click "Reply" to respond directly to {service_request.full_name} at {service_request.email}
            """

            # Send notification email to you with Reply-To set to user's email
            email_sent = False
            email_error = None
            try:
                from django.core.mail import EmailMessage
                
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=['zubedanrdn@gmail.com'],
                    reply_to=[service_request.email],
                )
                email.send(fail_silently=False)
                email_sent = True
                print(f"✓ Service request email sent to zubedanrdn@gmail.com with Reply-To: {service_request.email}")
            except Exception as e:
                email_error = str(e)
                print(f"✗ Notification email failed: {e}")
                import traceback
                traceback.print_exc()

            # Send confirmation email to the user (don't let this fail the request)
            try:
                user_subject = f"Service Request Received - {service_type}"
                user_message = f"""Dear {service_request.full_name},

Thank you for submitting a service request for {service_type}!

I have received your request and will review the details carefully. You can expect to hear back from me within 24 hours with a detailed proposal and timeline.

Request Summary:
- Service Type: {service_type}
- Timeline: {timeline}
- Budget Range: {budget}

If you have any urgent questions in the meantime, feel free to reply to this email.

Best regards,
Zubeda Nurdin
zubedanrdn@gmail.com

---
This is an automated confirmation email. Your request has been logged and will be reviewed shortly.
                """

                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [service_request.email],
                    fail_silently=True,
                )
                print(f"✓ Confirmation email sent to {service_request.email}")
            except Exception as e:
                print(f"✗ User confirmation email failed: {e}")

            # Return success response
            return Response({
                'success': True,
                'message': 'Service request submitted successfully!',
                'email_sent': email_sent,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"✗ Error processing service request: {e}")
            import traceback
            traceback.print_exc()
            return Response({
                'success': False,
                'message': 'Failed to process your request. Please try again.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'success': False,
        'message': 'Invalid form data. Please check your inputs.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def submit_contact_message(request):
    """Handle contact form submission"""
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        try:
            contact_message = serializer.save()

            # Send email notification with user's email prominently displayed
            subject = f"📧 Contact Form: {contact_message.subject}"
            message = f"""
═══════════════════════════════════════════════════
NEW CONTACT FORM SUBMISSION
═══════════════════════════════════════════════════

FROM: {contact_message.full_name}
EMAIL: {contact_message.email}
SUBJECT: {contact_message.subject}

───────────────────────────────────────────────────
MESSAGE:
───────────────────────────────────────────────────

{contact_message.message}

───────────────────────────────────────────────────
SUBMITTED: {contact_message.submitted_at.strftime('%B %d, %Y at %I:%M %p UTC')}
───────────────────────────────────────────────────

💡 TIP: Click "Reply" to respond directly to {contact_message.full_name} at {contact_message.email}
            """

            # Send notification email to you with Reply-To set to user's email
            email_sent = False
            email_error = None
            try:
                from django.core.mail import EmailMessage
                
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=['zubedanrdn@gmail.com'],
                    reply_to=[contact_message.email],
                )
                email.send(fail_silently=False)
                email_sent = True
                print(f"✓ Email sent successfully to zubedanrdn@gmail.com with Reply-To: {contact_message.email}")
            except Exception as e:
                email_error = str(e)
                print(f"✗ Notification email failed: {e}")
                import traceback
                traceback.print_exc()

            # Send confirmation email to the user (don't let this fail the request)
            try:
                user_subject = "Message Received - Thank You for Contacting Me"
                user_message = f"""Dear {contact_message.full_name},

Thank you for reaching out to me!

I have received your message regarding "{contact_message.subject}" and I appreciate you taking the time to get in touch.

I will review your message carefully and get back to you as soon as possible, typically within 24-48 hours.

Your Message Summary:
- Subject: {contact_message.subject}
- Received: {contact_message.submitted_at.strftime('%B %d, %Y at %I:%M %p UTC')}

If your inquiry is urgent, feel free to reach out to me directly at zubedanrdn@gmail.com.

Best regards,
Zubeda Nurdin
Portfolio Developer
zubedanrdn@gmail.com

---
This is an automated confirmation email. Your message has been successfully logged.
                """

                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_message.email],
                    fail_silently=True,
                )
                print(f"✓ Confirmation email sent to {contact_message.email}")
            except Exception as e:
                print(f"✗ User confirmation email failed: {e}")

            # Return success response
            return Response({
                'success': True,
                'message': 'Your message has been sent successfully!',
                'email_sent': email_sent,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"✗ Error processing contact message: {e}")
            import traceback
            traceback.print_exc()
            return Response({
                'success': False,
                'message': 'Failed to process your message. Please try again.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'success': False,
        'message': 'Invalid form data. Please check your inputs.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
