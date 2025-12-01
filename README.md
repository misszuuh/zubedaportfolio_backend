# Portfolio Backend - Django REST API

A comprehensive Django REST Framework backend for managing your portfolio website with features for projects, skills, testimonials, contact forms, and service requests.

## Features

### 📋 **Models & Endpoints**

1. **Projects** - Showcase your work
   - CRUD operations for projects
   - Image upload support
   - Skills tagging
   - Featured projects
   - Status management (draft/published/archived)

2. **Skills** - Display your expertise
   - Categorized by type (Frontend, Backend, Mobile, etc.)
   - Proficiency levels
   - Custom icons/emojis

3. **Testimonials** - Client feedback
   - Star ratings
   - Client information
   - Featured testimonials
   - Link to projects

4. **Contact Forms** - User communication
   - Email notifications
   - Status tracking
   - Admin panel management

5. **Service Requests** - Project inquiries
   - Multiple service types
   - Budget and timeline tracking
   - Email notifications
   - Status workflow

6. **Social Links** - Social media profiles
   - Multiple platforms
   - Custom ordering

7. **About Me** - Personal information
   - Bio and detailed biography
   - Profile image
   - Resume upload
   - Contact information

### 🚀 **API Features**

- RESTful API design
- Pagination support
- Filtering and search
- Sorting/ordering
- Read-only endpoints for public data
- Admin-only write access
- CORS configured for React frontend

## Installation

### 1. **Prerequisites**

- Python 3.8+
- pip
- virtualenv (recommended)

### 2. **Setup**

```bash
# Navigate to backend directory
cd backend_myportfolio

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. **Environment Configuration**

Create a `.env` file in the backend_myportfolio directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email Configuration (Gmail example)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**Note:** For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

### 4. **Database Setup**

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### 5. **Create Media Directories**

```bash
mkdir -p media/projects media/projects/thumbnails media/testimonials media/profile media/resume
```

### 6. **Run Development Server**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### **Projects**

- `GET /api/projects/` - List all published projects
- `GET /api/projects/{id}/` - Get project details
- `GET /api/projects/featured/` - Get featured projects only

### **Skills**

- `GET /api/skills/` - List all active skills
- `GET /api/skills/{id}/` - Get skill details
- `GET /api/skills/by_category/` - Get skills grouped by category

### **Testimonials**

- `GET /api/testimonials/` - List all active testimonials
- `GET /api/testimonials/{id}/` - Get testimonial details
- `GET /api/testimonials/featured/` - Get featured testimonials only

### **Social Links**

- `GET /api/social-links/` - List all active social links
- `GET /api/social-links/{id}/` - Get social link details

### **About Me**

- `GET /api/about-me/` - List about me information
- `GET /api/about-me/info/` - Get about me information (singleton)

### **Form Submissions**

- `POST /api/service-request/` - Submit a service request
- `POST /api/contact-message/` - Submit a contact message

### **Query Parameters**

All list endpoints support:
- `?page=<number>` - Pagination
- `?search=<query>` - Search (where applicable)
- `?ordering=<field>` - Sorting (e.g., `-created_at` for descending)
- Filter parameters specific to each endpoint

## Admin Panel

Access the admin panel at `http://localhost:8000/admin/`

Features:
- ✅ Manage all content (projects, skills, testimonials, etc.)
- ✅ View and respond to service requests
- ✅ View and manage contact messages
- ✅ Upload images and files
- ✅ Rich filtering and search
- ✅ Inline editing for related models

## Project Structure

```
backend_myportfolio/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── portfolioapp/          # Main application
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views/viewsets
│   ├── urls.py            # App URL routing
│   ├── admin.py           # Admin configuration
│   └── migrations/        # Database migrations
├── media/                 # User uploaded files
├── static/                # Static files
├── staticfiles/           # Collected static files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Models Overview

### **ServiceRequest**
- Service type, client info, requirements
- Timeline and budget preferences
- Status workflow (pending → reviewed → in_progress → completed)
- Automatic email notifications

### **ContactMessage**
- Contact form submissions
- Status tracking (new → read → replied)
- Email notifications

### **Project**
- Project details and media
- Skills association (many-to-many)
- Featured flag, ordering
- Status management

### **Skill**
- Name, category, proficiency level
- Icon/emoji support
- Active/inactive toggle

### **Testimonial**
- Client information and feedback
- Star ratings (1-5)
- Optional project link
- Featured flag

### **SocialLink**
- Platform name and URL
- Custom ordering
- Active/inactive toggle

### **AboutMe** (Singleton)
- Personal and professional information
- Profile image and resume
- Contact details

## Development Tips

### **Adding Sample Data**

You can add sample data through the admin panel or Django shell:

```bash
python manage.py shell
```

```python
from portfolioapp.models import Skill, Project

# Create a skill
skill = Skill.objects.create(
    name="Python",
    category="backend",
    proficiency=90,
    icon="🐍"
)

# Create a project
project = Project.objects.create(
    name="Portfolio Website",
    description="My personal portfolio",
    status="published",
    is_featured=True
)
```

### **Testing API Endpoints**

Use tools like:
- **Browser**: Visit `http://localhost:8000/api/projects/`
- **cURL**: `curl http://localhost:8000/api/projects/`
- **Postman**: Import endpoints for testing
- **HTTPie**: `http localhost:8000/api/projects/`

### **Database Management**

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (⚠️ deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Deployment

### **Production Checklist**

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Configure proper email backend
5. Collect static files: `python manage.py collectstatic`
6. Use a production server (Gunicorn, uWSGI)
7. Set up proper file storage for media files
8. Enable HTTPS
9. Set strong `SECRET_KEY`

### **Example with Gunicorn**

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### **Import Errors**

If you get import errors, ensure:
- Virtual environment is activated
- All dependencies are installed: `pip install -r requirements.txt`

### **Database Errors**

- Delete `db.sqlite3` and run migrations again
- Check for migration conflicts: `python manage.py showmigrations`

### **Email Not Sending**

- Verify email settings in `.env`
- For Gmail, use App Password, not regular password
- Check firewall/port settings for SMTP

### **CORS Issues**

- Verify `CORS_ALLOWED_ORIGINS` in `.env` matches your frontend URL
- Ensure `corsheaders` is installed and configured

## License

This project is for personal use.

## Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Check DRF documentation: https://www.django-rest-framework.org/
- Contact: zubedanrdn@gmail.com
