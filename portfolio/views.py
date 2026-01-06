from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Experience, Skill, Contact
from django.http import JsonResponse
from django.db.utils import OperationalError, ProgrammingError
from collections import defaultdict
import datetime

def get_skills_by_category():
    """Helper function to organize skills by category"""
    try:
        skills_by_category = defaultdict(list)
        skills = Skill.objects.all().order_by('category', 'name')
        
        # If no skills in database, return default skills
        if not skills.exists():
            return get_default_skills()
        
        for skill in skills:
            skills_by_category[skill.category].append(skill)
        
        return dict(skills_by_category)
    except (OperationalError, ProgrammingError):
        # Database tables don't exist yet, return defaults
        return get_default_skills()

def get_default_skills():
    """Return default skills if none exist in database"""
    return {
        'programming': [
            type('Skill', (), {'name': 'Python', 'proficiency': 85}),
            type('Skill', (), {'name': 'JavaScript', 'proficiency': 75}),
            type('Skill', (), {'name': 'SQL', 'proficiency': 80}),
        ],
        'framework': [
            type('Skill', (), {'name': 'Django', 'proficiency': 85}),
            type('Skill', (), {'name': 'Django REST Framework', 'proficiency': 80}),
            type('Skill', (), {'name': 'FastAPI', 'proficiency': 70}),
            type('Skill', (), {'name': 'Flask', 'proficiency': 75}),
            type('Skill', (), {'name': 'Streamlit', 'proficiency': 70}),
        ],
        'web': [
            type('Skill', (), {'name': 'HTML', 'proficiency': 90}),
            type('Skill', (), {'name': 'CSS', 'proficiency': 85}),
            type('Skill', (), {'name': 'Bootstrap', 'proficiency': 80}),
        ],
        'database': [
            type('Skill', (), {'name': 'PostgreSQL', 'proficiency': 75}),
            type('Skill', (), {'name': 'MySQL', 'proficiency': 70}),
            type('Skill', (), {'name': 'SQLite', 'proficiency': 80}),
        ],
        'tools': [
            type('Skill', (), {'name': 'Git', 'proficiency': 85}),
            type('Skill', (), {'name': 'Docker', 'proficiency': 65}),
            type('Skill', (), {'name': 'JWT Authentication', 'proficiency': 75}),
            type('Skill', (), {'name': 'REST APIs', 'proficiency': 85}),
            type('Skill', (), {'name': 'Power BI', 'proficiency': 70}),
            type('Skill', (), {'name': 'Matplotlib', 'proficiency': 75}),
            type('Skill', (), {'name': 'OpenAI API', 'proficiency': 70}),
            type('Skill', (), {'name': 'Swagger', 'proficiency': 70}),
        ]
    }

def get_default_projects():
    """Return default projects if none exist in database"""
    return [
        type('Project', (), {
            'title': 'Document Image Summary Application',
            'description': 'Built an AI-based app to extract and summarize text from PDFs/images using Streamlit and OpenAI. Deployed on Streamlit Cloud with support for batch document processing.',
            'technologies': 'Python, Streamlit, OpenAI API, PDF Processing, Image Processing',
            'github_link': 'https://github.com/sartaj05',
            'live_link': '',
            'is_featured': True,
            'created_date': datetime.date.today(),
            'tech_list': ['Python', 'Streamlit', 'OpenAI API', 'PDF Processing', 'Image Processing']
        }),
        type('Project', (), {
            'title': 'Article Management System',
            'description': 'Developed an article management backend with role-based access and JWT authentication. Integrated Swagger (drf-yasg) for interactive API documentation.',
            'technologies': 'Django, Django REST Framework, JWT, Swagger, PostgreSQL',
            'github_link': 'https://github.com/sartaj05',
            'live_link': '',
            'is_featured': True,
            'created_date': datetime.date.today(),
            'tech_list': ['Django', 'Django REST Framework', 'JWT', 'Swagger', 'PostgreSQL']
        }),
        type('Project', (), {
            'title': 'Library Management System',
            'description': 'Designed and developed a library system integrating key operations like book management, member tracking, and late fee calculations. Visualized borrowing trends using Matplotlib, enabling insightful reporting for library operations. Implemented robust backend logic to manage borrowing transactions and ensure data integrity.',
            'technologies': 'Python, Flask, SQLite, Matplotlib, Data Visualization',
            'github_link': 'https://github.com/sartaj05',
            'live_link': '',
            'is_featured': True,
            'created_date': datetime.date(2024, 9, 1),
            'tech_list': ['Python', 'Flask', 'SQLite', 'Matplotlib', 'Data Visualization']
        }),
        type('Project', (), {
            'title': 'Power BI Dashboard',
            'description': 'Developed a dynamic Power BI dashboard to visualize business performance and trends across multiple metrics. Integrated data sources using CSV and performed data transformation and cleaning with Python. Designed interactive reports and insights to assist in decision-making, helping stakeholders identify actionable strategies.',
            'technologies': 'Power BI, Excel, CSV, Python, Data Analysis',
            'github_link': 'https://github.com/sartaj05',
            'live_link': '',
            'is_featured': True,
            'created_date': datetime.date(2024, 7, 1),
            'tech_list': ['Power BI', 'Excel', 'CSV', 'Python', 'Data Analysis']
        }),
        type('Project', (), {
            'title': 'Tweet Application',
            'description': 'Created a basic Tweet app supporting post creation, editing, and deletion. Set up Django views, templates, and routing for smooth UI interaction.',
            'technologies': 'Django, Python, SQLite, HTML, CSS, JavaScript',
            'github_link': 'https://github.com/sartaj05',
            'live_link': '',
            'is_featured': False,
            'created_date': datetime.date(2024, 8, 1),
            'tech_list': ['Django', 'Python', 'SQLite', 'HTML', 'CSS', 'JavaScript']
        }),
        type('Project', (), {
            'title': 'Portfolio Website',
            'description': 'A responsive portfolio website built with Django featuring modern UI/UX, contact forms, and dynamic content management with glassmorphism design and smooth animations.',
            'technologies': 'Python, Django, HTML, CSS, JavaScript, Bootstrap, GSAP',
            'github_link': 'https://github.com/sartaj05',
            'live_link': '',
            'is_featured': False,
            'created_date': datetime.date.today(),
            'tech_list': ['Python', 'Django', 'HTML', 'CSS', 'JavaScript', 'Bootstrap', 'GSAP']
        })
    ]

def get_default_experiences():
    """Return default experiences if none exist in database"""
    return [
        type('Experience', (), {
            'company': 'Createch Software Pvt. Ltd.',
            'position': 'Jr. Software Engineer',
            'duration': 'May 2024 - Present',
            'location': 'Ministry of Defence (ASDC)',
            'description': 'Working on enterprise-level solutions using cutting-edge technologies. Involved in developing scalable backend applications using Python, Django, and FastAPI. Contributing to innovative projects in the defense sector with focus on performance optimization and test-driven development.',
            'technologies': 'Python, Django, FastAPI, PostgreSQL, Git, Docker',
            'tech_list': ['Python', 'Django', 'FastAPI', 'PostgreSQL', 'Git', 'Docker']
        }),
        type('Experience', (), {
            'company': 'Mobiloitte Technologies',
            'position': 'Software Developer (Python/Django - AI/ML)',
            'duration': 'October 2024 - December 2024',
            'location': 'Internship',
            'description': 'Designed and developed scalable backend solutions using Python, Django, and RESTful APIs for web applications. Collaborated with front-end teams to integrate robust APIs and improve application performance. Worked on implementing secure authentication mechanisms using JWT.',
            'technologies': 'Python, Django, REST API, JWT, AI/ML, PostgreSQL',
            'tech_list': ['Python', 'Django', 'REST API', 'JWT', 'AI/ML', 'PostgreSQL']
        })
    ]

def index(request):
    # Get projects
    try:
        featured_projects = Project.objects.filter(is_featured=True)[:3]
        if not featured_projects.exists():
            featured_projects = get_default_projects()[:3]
    except (OperationalError, ProgrammingError):
        featured_projects = get_default_projects()[:3]
    
    # Get experience (most recent)
    try:
        recent_experience = Experience.objects.first()
        if not recent_experience:
            recent_experiences = get_default_experiences()
            recent_experience = recent_experiences[0]
    except (OperationalError, ProgrammingError):
        recent_experiences = get_default_experiences()
        recent_experience = recent_experiences[0]
    
    # Get skills
    skills_by_category = get_skills_by_category()
    
    context = {
        'featured_projects': featured_projects,
        'recent_experience': recent_experience,
        'skills_by_category': skills_by_category,
        'current_year': datetime.datetime.now().year,
    }
    return render(request, 'portfolio/index.html', context)

def about(request):
    skills_by_category = get_skills_by_category()
    
    context = {
        'skills_by_category': skills_by_category,
        'current_year': datetime.datetime.now().year,
    }
    return render(request, 'portfolio/about.html', context)

def projects(request):
    try:
        all_projects = Project.objects.all()
        
        # If no projects in database, use default
        if not all_projects.exists():
            all_projects = get_default_projects()
    except (OperationalError, ProgrammingError):
        all_projects = get_default_projects()
    
    context = {
        'projects': all_projects,
        'current_year': datetime.datetime.now().year,
    }
    return render(request, 'portfolio/projects.html', context)

def experience(request):
    try:
        experiences = Experience.objects.all().order_by('-order')
        
        # If no experiences in database, use default
        if not experiences.exists():
            experiences = get_default_experiences()
    except (OperationalError, ProgrammingError):
        experiences = get_default_experiences()
    
    context = {
        'experiences': experiences,
        'current_year': datetime.datetime.now().year,
    }
    return render(request, 'portfolio/experience.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, subject, message]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'message': 'All fields are required.'
                })
            else:
                messages.error(request, 'All fields are required.')
                return redirect('contact')
        
        try:
            # Try to save to database
            try:
                contact = Contact.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
            except (OperationalError, ProgrammingError):
                # Database not available, skip saving
                print("Database not available - contact message not saved")
            
            # Send email notification
            email_sent = False
            try:
                send_mail(
                    subject=f'Portfolio Contact: {subject}',
                    message=f'From: {name} ({email})\n\nMessage:\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['sartaj.ahamad0502@gmail.com'],
                    fail_silently=False,
                )
                email_sent = True
            except Exception as e:
                # Log the error but don't fail the request
                print(f"Email sending failed: {str(e)}")
            
            success_message = 'Thank you for your message! I\'ll get back to you soon.'
            if not email_sent:
                success_message += ' (Note: Email notification may be delayed)'
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': success_message
                })
            else:
                messages.success(request, success_message)
                return redirect('contact')
                
        except Exception as e:
            print(f"Contact form error: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'message': 'Sorry, there was an error sending your message. Please try again.'
                })
            else:
                messages.error(request, 'Sorry, there was an error. Please try again.')
                return redirect('contact')
    
    context = {
        'current_year': datetime.datetime.now().year,
    }
    return render(request, 'portfolio/contact.html', context)