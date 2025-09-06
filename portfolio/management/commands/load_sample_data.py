from django.core.management.base import BaseCommand
from portfolio.models import Project, Experience, Skill

class Command(BaseCommand):
    help = 'Load sample data for portfolio'

    def handle(self, *args, **options):
        # Create sample projects
        projects_data = [
            {
                'title': 'Document Image Summary Application',
                'description': 'Built an AI-based app to extract and summarize text from PDFs/images using Streamlit and OpenAI. Deployed on Streamlit Cloud with support for batch document processing.',
                'technologies': 'Python, Streamlit, OpenAI API',
                'github_link': 'https://github.com/sartaj05/document-summary',
                'is_featured': True
            },
            {
                'title': 'Article Management System',
                'description': 'Developed an article management backend with role-based access and JWT authentication. Integrated Swagger (drf-yasg) for interactive API documentation.',
                'technologies': 'Django, DRF, JWT',
                'github_link': 'https://github.com/sartaj05/article-management',
                'is_featured': True
            },
            {
                'title': 'Tweet Application',
                'description': 'Created a basic Tweet app supporting post creation, editing, and deletion. Set up Django views, templates, and routing for smooth UI interaction.',
                'technologies': 'Django, Python, SQLite, HTML, CSS',
                'github_link': 'https://github.com/sartaj05/tweet-app',
                'is_featured': False
            }
        ]

        for project_data in projects_data:
            Project.objects.get_or_create(**project_data)

        # Create sample experiences
        experiences_data = [
            {
                'company': 'Createch Software Pvt. Ltd.',
                'position': 'Jr. Software Engineer',
                'duration': 'February 2025 – Present',
                'location': 'Delhi',
                'description': 'Developing scalable and efficient backend applications using Django, FastAPI, and JavaScript for enterprise solutions. Working extensively with PostgreSQL databases and implementing caching systems using Redis.',
                'technologies': 'Django, FastAPI, JavaScript, PostgreSQL, Redis, Pytest, SonarQube',
                'order': 1
            },
            {
                'company': 'Mobiloitte Technologies',
                'position': 'Software Developer (Python/Django - AI/ML)',
                'duration': 'October 2024 – December 2024',
                'location': 'Remote (Internship)',
                'description': 'Designed and developed scalable backend solutions using Python, Django, and RESTful APIs for web applications. Collaborated with front-end teams to integrate robust APIs and improve application performance.',
                'technologies': 'Python, Django, REST APIs, JWT',
                'order': 2
            }
        ]

        for exp_data in experiences_data:
            Experience.objects.get_or_create(**exp_data)

        # Create sample skills
        skills_data = [
            # Programming Languages
            {'name': 'Python', 'category': 'programming', 'proficiency': 90},
            {'name': 'JavaScript', 'category': 'programming', 'proficiency': 75},
            
            # Web Technologies
            {'name': 'HTML', 'category': 'web', 'proficiency': 85},
            {'name': 'CSS', 'category': 'web', 'proficiency': 80},
            
            # Databases
            {'name': 'PostgreSQL', 'category': 'database', 'proficiency': 85},
            {'name': 'SQLite', 'category': 'database', 'proficiency': 80},
            {'name': 'SQL', 'category': 'database', 'proficiency': 85},
            
            # Frameworks
            {'name': 'Django', 'category': 'framework', 'proficiency': 90},
            {'name': 'Django REST Framework', 'category': 'framework', 'proficiency': 85},
            {'name': 'FastAPI', 'category': 'framework', 'proficiency': 80},
            
            # Tools & Libraries
            {'name': 'Redis', 'category': 'tools', 'proficiency': 75},
            {'name': 'Git', 'category': 'tools', 'proficiency': 85},
            {'name': 'GitHub', 'category': 'tools', 'proficiency': 85},
            {'name': 'NumPy', 'category': 'tools', 'proficiency': 70},
            {'name': 'Pandas', 'category': 'tools', 'proficiency': 70},
            {'name': 'Pytest', 'category': 'tools', 'proficiency': 75},
            {'name': 'SonarQube', 'category': 'tools', 'proficiency': 65},
            
            # Other
            {'name': 'DSA', 'category': 'other', 'proficiency': 70},
            {'name': 'AI/ML', 'category': 'other', 'proficiency': 60},
            {'name': 'Hugging Face', 'category': 'other', 'proficiency': 55},
        ]

        for skill_data in skills_data:
            Skill.objects.get_or_create(**skill_data)

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )