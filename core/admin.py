from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.db import models
from django.utils.html import format_html
from .models import Project, ProjectImage, Skill, Contact

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'date_created', 'preview_image')
    list_filter = ('category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    
    def preview_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 30px;"/>', obj.featured_image.url)
        return "No image"
    preview_image.short_description = 'Preview'

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption', 'order')
    list_filter = ('project',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order')
    list_editable = ('order',)
    ordering = ('order', 'name')
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_sent', 'ip_address')
    list_filter = ('date_sent',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('date_sent', 'ip_address')
    exclude = ('honeypot',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('System Information', {
            'fields': ('date_sent', 'ip_address'),
            'classes': ('collapse',)
        })
    )
    
from django.contrib import admin

admin.site.site_header = 'Portfolio Administration'  
admin.site.site_title = 'Zain portfolio'     
admin.site.index_title = 'Welcome Zain'