from django.shortcuts import render, get_object_or_404

from core.forms import ContactForm

from .models import Project, Contact, Skill
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect

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
        form = ContactForm(request.POST)
        if form.is_valid():
            honeypot = request.POST.get('honeypot', '').strip()
            if honeypot:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Message sent successfully!'
                })
            
            contact = form.save(commit=False)
            contact.ip_address = request.META.get('REMOTE_ADDR', '')
            contact.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Message sent successfully!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)       

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred while processing your request.',
            'errors': {'server': [str(e)]}
        }, status=500)
