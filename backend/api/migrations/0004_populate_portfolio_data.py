from django.db import migrations
from django.apps import apps


def populate_portfolio_data(apps, schema_editor):
    # Get model classes
    PersonalInfo = apps.get_model('api', 'PersonalInfo')
    About = apps.get_model('api', 'About')
    SocialLink = apps.get_model('api', 'SocialLink')
    Project = apps.get_model('api', 'Project')
    Skill = apps.get_model('api', 'Skill')
    Experience = apps.get_model('api', 'Experience')
    Education = apps.get_model('api', 'Education')
    Certification = apps.get_model('api', 'Certification')
    
    # Create Personal Info
    PersonalInfo.objects.get_or_create(
        defaults={
            'name': 'Jenish Barvaliya',
            'title': 'AI/ML Engineer & Data Science Specialist',
            'subtitle': 'Information Technology Student & Machine Learning Engineer',
            'location': 'Surat, Gujarat, India',
            'email': 'jenishbarvaliya2012@gmail.com',
            'phone': '+91 9510007247',
            'linkedin': 'https://linkedin.com/in/jenish-barvaliya',
            'github': 'https://github.com/jenish2917',
            'resume': '/resume.pdf',
            'is_active': True
        }
    )
    
    # Create About
    About.objects.get_or_create(
        defaults={
            'summary': '''Results-driven Information Technology student specializing in Machine Learning and Data Science with hands-on internship
experience developing AI-driven solutions. Proficient in architecting and deploying end-to-end ML projects using Python,
TensorFlow, and Scikit-learn. Demonstrated expertise in data pipeline development, model optimization, and predictive
analytics. Seeking challenging international opportunities to apply strong foundation in data analysis and machine learning to
solve complex business problems and deliver measurable impact in technology-driven organizations.''',
            'vision': '''To leverage artificial intelligence and machine learning technologies to create impactful solutions that drive innovation 
and solve real-world problems, while continuously expanding my expertise in emerging technologies.''',
            'highlights': [
                "AI/ML Engineer Intern with proven track record at Elite Technocrats",
                "Proficient in Python, TensorFlow, Scikit-learn, and Django",
                "Strong background in data pipeline development and NLP",
                "Experience with full-stack web development using React.js",
                "9.34/10.0 CGPA - Academic Excellence",
                "Active contributor to open-source ML/AI projects"
            ],
            'is_active': True
        }
    )
    
    # Create Social Links
    social_links_data = [
        {'name': 'GitHub', 'url': 'https://github.com/jenish2917', 'icon': 'Github', 'color': '#ffffff', 'order': 1},
        {'name': 'LinkedIn', 'url': 'https://linkedin.com/in/jenish-barvaliya', 'icon': 'Linkedin', 'color': '#0077b5', 'order': 2},
        {'name': 'Email', 'url': 'mailto:jenishbarvaliya2012@gmail.com', 'icon': 'Mail', 'color': '#ea4335', 'order': 3},
        {'name': 'Twitter', 'url': 'https://twitter.com/jenish_barvaliya', 'icon': 'Twitter', 'color': '#1da1f2', 'order': 4},
    ]
    
    for link_data in social_links_data:
        SocialLink.objects.get_or_create(name=link_data['name'], defaults=link_data)


def reverse_populate_portfolio_data(apps, schema_editor):
    # Get model classes
    PersonalInfo = apps.get_model('api', 'PersonalInfo')
    About = apps.get_model('api', 'About')
    SocialLink = apps.get_model('api', 'SocialLink')
    
    # Delete the data
    PersonalInfo.objects.all().delete()
    About.objects.all().delete()
    SocialLink.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_auto_20250810_1629'),
    ]

    operations = [
        migrations.RunPython(populate_portfolio_data, reverse_populate_portfolio_data),
    ]
