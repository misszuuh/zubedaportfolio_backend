#!/usr/bin/env python
"""
Test script to verify email configuration
"""
import os
import sys
import django

# Set up Django environment
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Test email sending functionality"""
    print("Testing email configuration...")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD)} (hidden)")
    print("\nSending test email...")

    try:
        send_mail(
            subject='Portfolio Contact Form - Test Email',
            message='This is a test email from your Portfolio Django backend. If you receive this, your email configuration is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['zubedanrdn@gmail.com'],
            fail_silently=False,
        )
        print("✓ Email sent successfully!")
        print("Check your inbox at zubedanrdn@gmail.com")
        return True
    except Exception as e:
        print(f"✗ Email sending failed!")
        print(f"Error: {str(e)}")
        return False

if __name__ == '__main__':
    test_email()
