from django.shortcuts import render, get_object_or_404

from portfolio import settings
from .models import Project, Contact, Skill
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import json

def Index(request):
    skills = Skill.objects.all().order_by('order')
    featured_projects = Project.objects.filter(is_featured=True)
    return render(request, 'index.html', {'featured_projects': featured_projects, 'skills': skills})

def Projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})

def ProjectDetail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'project_details.html', {'project': project})


@csrf_protect
@require_http_methods(["POST"])
def contact_submit(request):
    try:
        # Clean and validate input data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        honeypot = request.POST.get('honeypot', '').strip()

        errors = {}
        
        # Basic validation
        if len(name) < 2:
            errors['name'] = ['Name must be at least 2 characters long']
        if '@' not in email:
            errors['email'] = ['Please enter a valid email address']
        if len(message) < 10:
            errors['message'] = ['Message must be at least 10 characters long']

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        # Honeypot check
        if honeypot:
            return JsonResponse({
                'status': 'success',
                'message': 'Message sent successfully!'
            })

        # Create contact entry
        contact = Contact.objects.create(
            name=name,
            email=email,
            message=message,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            date_sent=timezone.now()
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Message sent successfully!'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred while processing your request.',
            'errors': {'server': [str(e)]}
        }, status=500)
