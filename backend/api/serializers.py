from rest_framework import serializers
from .models import (
    PersonalInfo, About, SocialLink, Contact, Project, 
    Skill, Experience, Certification, Education
)


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = [
            'id', 'name', 'title', 'subtitle', 'location', 'email', 
            'phone', 'linkedin', 'github', 'resume'
        ]


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'summary', 'vision', 'highlights']


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id', 'name', 'url', 'icon', 'color', 'order']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'long_description', 'image',
            'technologies', 'features', 'github_url', 'live_url', 
            'status', 'created_at', 'is_featured'
        ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'level', 'icon']


class ExperienceSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField()
    
    class Meta:
        model = Experience
        fields = [
            'id', 'title', 'company', 'location', 'start_date', 'end_date',
            'is_current', 'description', 'technologies', 'duration'
        ]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            'id', 'title', 'issuer', 'date_issued', 'credential_id',
            'description', 'verification_url', 'logo'
        ]


class EducationSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField()
    
    class Meta:
        model = Education
        fields = [
            'id', 'degree', 'institution', 'location', 'start_date', 'end_date',
            'is_current', 'gpa', 'description', 'coursework', 'duration'
        ]
