import datetime
import logging
import time
from types import SimpleNamespace

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

logger = logging.getLogger(__name__)


def _current_year():
    return datetime.datetime.now().year


def _contact_context(**extra):
    context = {
        'current_year': _current_year(),
        'form_started': int(time.time()),
    }
    context.update(extra)
    return context


def _contact_error(request, message, status=400):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': message}, status=status)
    return render(request, 'portfolio/contact.html', _contact_context(form_error=message), status=status)


def get_default_skills():
    return {
        'programming': [
            SimpleNamespace(name='Python', proficiency=85),
            SimpleNamespace(name='JavaScript', proficiency=75),
            SimpleNamespace(name='SQL', proficiency=80),
        ],
        'framework': [
            SimpleNamespace(name='Django', proficiency=85),
            SimpleNamespace(name='Django REST Framework', proficiency=80),
            SimpleNamespace(name='FastAPI', proficiency=70),
            SimpleNamespace(name='Flask', proficiency=75),
            SimpleNamespace(name='Streamlit', proficiency=70),
        ],
        'web': [
            SimpleNamespace(name='HTML', proficiency=90),
            SimpleNamespace(name='CSS', proficiency=85),
            SimpleNamespace(name='Bootstrap', proficiency=80),
        ],
        'database': [
            SimpleNamespace(name='PostgreSQL', proficiency=75),
            SimpleNamespace(name='MySQL', proficiency=70),
            SimpleNamespace(name='SQLite', proficiency=80),
        ],
        'tools': [
            SimpleNamespace(name='Git', proficiency=85),
            SimpleNamespace(name='Docker', proficiency=65),
            SimpleNamespace(name='JWT Authentication', proficiency=75),
            SimpleNamespace(name='REST APIs', proficiency=85),
            SimpleNamespace(name='Power BI', proficiency=70),
            SimpleNamespace(name='Matplotlib', proficiency=75),
            SimpleNamespace(name='OpenAI API', proficiency=70),
            SimpleNamespace(name='Swagger', proficiency=70),
        ],
    }


def _project(title, description, technologies, featured=True, github_link='https://github.com/sartaj05', live_link=''):
    return SimpleNamespace(
        title=title,
        description=description,
        technologies=technologies,
        github_link=github_link,
        live_link=live_link,
        is_featured=featured,
        created_date=datetime.date.today(),
        tech_list=[item.strip() for item in technologies.split(',') if item.strip()],
    )


def get_default_projects():
    return [
        _project('Document Image Summary Application', 'Built an AI-based app to extract and summarize text from PDFs/images using Streamlit and OpenAI. Deployed on Streamlit Cloud with support for batch document processing.', 'Python, Streamlit, OpenAI API, PDF Processing, Image Processing'),
        _project('Article Management System', 'Developed an article management backend with role-based access and JWT authentication. Integrated Swagger for interactive API documentation.', 'Django, Django REST Framework, JWT, Swagger, PostgreSQL'),
        _project('Library Management System', 'Designed a library system for book management, member tracking, late-fee calculations, borrowing transactions, and reporting.', 'Python, Flask, SQLite, Matplotlib, Data Visualization'),
        _project('Power BI Dashboard', 'Developed a dynamic dashboard to visualize business performance and trends. Cleaned source data with Python and designed interactive reports for decision-making.', 'Power BI, Excel, CSV, Python, Data Analysis'),
        _project('Tweet Application', 'Created a basic Tweet app supporting post creation, editing, and deletion with Django views, templates, and routing.', 'Django, Python, SQLite, HTML, CSS, JavaScript', featured=False),
        _project('Portfolio Website', 'A responsive Django portfolio with modern UI, contact email delivery, SEO metadata, analytics hooks, and smooth animations.', 'Python, Django, HTML, CSS, JavaScript', featured=False),
    ]


def _experience(company, position, duration, location, description, technologies):
    return SimpleNamespace(
        company=company,
        position=position,
        duration=duration,
        location=location,
        description=description,
        technologies=technologies,
        tech_list=[item.strip() for item in technologies.split(',') if item.strip()],
    )


def get_default_experiences():
    return [
        _experience('Createch Software Pvt. Ltd.', 'Jr. Software Engineer', 'Feb 2024 - Present', 'Ministry of Defence (ASDC)', 'Working on enterprise-level solutions using Python, Django, and FastAPI. Contributing to scalable backend applications with a focus on performance and test-driven development.', 'Python, Django, FastAPI, PostgreSQL, Git, Docker'),
        _experience('Mobiloitte Technologies', 'Software Developer (Python/Django - AI/ML)', 'October 2024 - December 2024', 'Internship', 'Designed scalable backend solutions using Python, Django, and RESTful APIs. Collaborated with front-end teams and implemented secure JWT authentication.', 'Python, Django, REST API, JWT, AI/ML, PostgreSQL'),
    ]


def index(request):
    context = {
        'featured_projects': get_default_projects()[:3],
        'recent_experience': get_default_experiences()[0],
        'skills_by_category': get_default_skills(),
        'current_year': _current_year(),
    }
    return render(request, 'portfolio/index.html', context)


def about(request):
    return render(request, 'portfolio/about.html', {
        'skills_by_category': get_default_skills(),
        'current_year': _current_year(),
    })


def projects(request):
    return render(request, 'portfolio/projects.html', {
        'projects': get_default_projects(),
        'current_year': _current_year(),
    })


def experience(request):
    return render(request, 'portfolio/experience.html', {
        'experiences': get_default_experiences(),
        'current_year': _current_year(),
    })


def contact(request):
    if request.method != 'POST':
        return render(request, 'portfolio/contact.html', _contact_context())

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    if request.POST.get('website', '').strip():
        return _contact_error(request, 'Your message could not be sent. Please try again.')
    try:
        form_started = float(request.POST.get('form_started', '0'))
    except (TypeError, ValueError):
        form_started = 0
    if not form_started or time.time() - form_started < 2:
        return _contact_error(request, 'Please take a moment to review your message and try again.')
    if not all([name, email, subject, message]):
        return _contact_error(request, 'All fields are required.')
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        return _contact_error(request, 'Email delivery is not configured yet. Please use the direct email link below, or configure SMTP before deploying.', status=503)

    email_body = f'''New contact form submission from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
Sent from Portfolio Contact Form
'''
    try:
        send_mail(
            subject=f'Portfolio Contact: {subject}',
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_RECIPIENT],
            fail_silently=False,
        )
    except BadHeaderError:
        logger.error('Invalid header found when sending contact email')
        return _contact_error(request, 'Your message could not be sent. Please check the subject and try again.', status=400)
    except Exception:
        logger.exception('Failed to send contact email')
        return _contact_error(request, 'Your message could not be sent right now. Please email me directly.', status=503)

    success_msg = "Thank you for your message! I'll get back to you soon."
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': success_msg})
    return render(request, 'portfolio/contact.html', _contact_context(form_success=success_msg))


def robots_txt(request):
    content = '\n'.join([
        'User-agent: *',
        'Allow: /',
        f'Sitemap: {settings.SITE_URL}/sitemap.xml',
    ])
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    page_names = ['index', 'about', 'projects', 'experience', 'contact']
    urls = [f'  <url><loc>{settings.SITE_URL}{reverse(name)}</loc></url>' for name in page_names]
    content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    content += '\n'.join(urls)
    content += '\n</urlset>\n'
    return HttpResponse(content, content_type='application/xml')
