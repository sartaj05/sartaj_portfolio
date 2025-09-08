from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Experience, Skill, Contact
from django.http import JsonResponse

def index(request):
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    recent_experience = Experience.objects.first()
    skills_by_category = {}
    
    for skill in Skill.objects.all():
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    context = {
        'featured_projects': featured_projects,
        'recent_experience': recent_experience,
        'skills_by_category': skills_by_category,
    }
    return render(request, 'portfolio/index.html', context)

def about(request):
    skills_by_category = {}
    for skill in Skill.objects.all():
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    context = {
        'skills_by_category': skills_by_category,
    }
    return render(request, 'portfolio/about.html', context)

def projects(request):
    all_projects = Project.objects.all()
    context = {
        'projects': all_projects,
    }
    return render(request, 'portfolio/projects.html', context)


def experience(request):
    experiences = Experience.objects.all().order_by('order')  # or '-order' for reverse
    
    # Process technologies for each experience
    for exp in experiences:
        if exp.technologies:
            exp.tech_list = [tech.strip() for tech in exp.technologies.split(',')]
        else:
            exp.tech_list = []
    
    context = {
        'experiences': experiences,
    }
    return render(request, 'portfolio/experience.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        else:
            messages.success(request, 'Thank you for your message! I\'ll get back to you soon.')
            return redirect('contact')
    
    return render(request, 'portfolio/contact.html')