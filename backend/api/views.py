from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from .models import (
    PersonalInfo, About, SocialLink, Contact, Project, 
    Skill, Experience, Certification, Education
)
from .serializers import (
    PersonalInfoSerializer, AboutSerializer, SocialLinkSerializer,
    ContactSerializer, ProjectSerializer, SkillSerializer,
    ExperienceSerializer, CertificationSerializer, EducationSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def personal_info(request):
    """
    Get personal information
    """
    try:
        personal_info = PersonalInfo.objects.filter(is_active=True).first()
        if personal_info:
            return Response(PersonalInfoSerializer(personal_info).data)
        return Response({'error': 'Personal info not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def about_info(request):
    """
    Get about information
    """
    try:
        about = About.objects.filter(is_active=True).first()
        if about:
            return Response(AboutSerializer(about).data)
        return Response({'error': 'About info not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def social_links(request):
    """
    Get social links
    """
    try:
        links = SocialLink.objects.filter(is_active=True).order_by('order')
        return Response(SocialLinkSerializer(links, many=True).data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling contact form submissions
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            
            # Send email notification
            try:
                subject = f"New Contact Form Submission: {contact.subject}"
                message = f"""
                New contact form submission from your portfolio website:
                
                Name: {contact.name}
                Email: {contact.email}
                Subject: {contact.subject}
                
                Message:
                {contact.message}
                
                Submitted at: {contact.created_at}
                """
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't fail the request
                print(f"Failed to send email: {e}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for displaying projects
    """
    queryset = Project.objects.filter(is_featured=True)
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Project.objects.all()
        featured_only = self.request.query_params.get('featured', None)
        if featured_only == 'true':
            queryset = queryset.filter(is_featured=True)
        return queryset.order_by('-created_at')


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for displaying skills
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        skills = self.get_queryset()
        # Group skills by category
        skills_by_category = {}
        for skill in skills:
            category = skill.get_category_display()
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(SkillSerializer(skill).data)
        
        return Response(skills_by_category)


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for displaying work experience
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [AllowAny]


class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for displaying certifications
    """
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [AllowAny]


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for displaying education
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([AllowAny])
def portfolio_summary(request):
    """
    API endpoint that returns a summary of all portfolio data
    """
    try:
        data = {
            'projects': ProjectSerializer(
                Project.objects.filter(is_featured=True)[:6], 
                many=True
            ).data,
            'skills_count': Skill.objects.count(),
            'experience_count': Experience.objects.count(),
            'certifications_count': Certification.objects.count(),
            'education': EducationSerializer(
                Education.objects.first()
            ).data if Education.objects.exists() else None,
            'latest_experience': ExperienceSerializer(
                Experience.objects.first()
            ).data if Experience.objects.exists() else None,
        }
        return Response(data)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch portfolio summary'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint
    """
    return Response({'status': 'healthy', 'message': 'Portfolio API is running!'})
