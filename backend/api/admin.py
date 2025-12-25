from django.contrib import admin
from .models import (
    PersonalInfo, About, SocialLink, Contact, Project, 
    Skill, Experience, Certification, Education
)


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'email']
    
    def has_add_permission(self, request):
        # Only allow one PersonalInfo instance
        return not PersonalInfo.objects.exists()


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active']
    list_filter = ['is_active']
    
    def has_add_permission(self, request):
        # Only allow one About instance
        return not About.objects.exists()


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['order']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    actions = [mark_as_read]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'level', 'icon']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['category', '-level']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'company']
    search_fields = ['title', 'company']
    ordering = ['-start_date']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'date_issued', 'credential_id']
    list_filter = ['issuer', 'date_issued']
    search_fields = ['title', 'issuer']
    ordering = ['-date_issued']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'institution']
    search_fields = ['degree', 'institution']
    ordering = ['-start_date']
