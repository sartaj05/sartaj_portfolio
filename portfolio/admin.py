from django.contrib import admin
from .models import Project, Experience, Skill, Contact

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'technologies', 'is_featured', 'created_date']
    list_filter = ['is_featured', 'created_date']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'duration', 'order']
    list_editable = ['order']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency']
    list_filter = ['category']
    list_editable = ['proficiency']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_date', 'is_read']
    list_filter = ['is_read', 'created_date']
    list_editable = ['is_read']
    readonly_fields = ['created_date']