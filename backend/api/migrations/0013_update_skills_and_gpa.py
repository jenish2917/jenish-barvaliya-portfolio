# Generated migration to update skills and GPA according to latest resume

from django.db import migrations


def update_skills_and_gpa(apps, schema_editor):
    Skill = apps.get_model('api', 'Skill')
    Education = apps.get_model('api', 'Education')
    
    # Clear existing skills
    Skill.objects.all().delete()
    
    # Updated skills according to resume
    skills_data = [
        # Programming Languages
        {'name': 'Python', 'category': 'programming', 'level': 90, 'icon': '🐍'},
        {'name': 'Java', 'category': 'programming', 'level': 80, 'icon': '☕'},
        {'name': 'C', 'category': 'programming', 'level': 75, 'icon': '⚡'},
        {'name': 'JavaScript', 'category': 'programming', 'level': 85, 'icon': '🟨'},
        {'name': 'SQL', 'category': 'programming', 'level': 80, 'icon': '🗃️'},
        
        # Machine Learning & Data Science
        {'name': 'Scikit-learn', 'category': 'ml_ai', 'level': 90, 'icon': '🤖'},
        {'name': 'Pandas', 'category': 'data_science', 'level': 95, 'icon': '🐼'},
        {'name': 'NumPy', 'category': 'data_science', 'level': 90, 'icon': '🔢'},
        {'name': 'Polars', 'category': 'data_science', 'level': 75, 'icon': '⚡'},
        {'name': 'Matplotlib', 'category': 'data_science', 'level': 85, 'icon': '📊'},
        {'name': 'Seaborn', 'category': 'data_science', 'level': 85, 'icon': '📈'},
        {'name': 'Natural Language Processing', 'category': 'ml_ai', 'level': 80, 'icon': '🗣️'},
        
        # Deep Learning Frameworks
        {'name': 'TensorFlow', 'category': 'ml_ai', 'level': 85, 'icon': '🧠'},
        {'name': 'Keras', 'category': 'ml_ai', 'level': 80, 'icon': '🔥'},
        
        # Web Technologies & Automation
        {'name': 'Django', 'category': 'web_dev', 'level': 85, 'icon': '🐍'},
        {'name': 'React.js', 'category': 'web_dev', 'level': 80, 'icon': '⚛️'},
        {'name': 'Selenium', 'category': 'tools', 'level': 75, 'icon': '🔧'},
        {'name': 'Playwright', 'category': 'tools', 'level': 70, 'icon': '🎭'},
        {'name': 'REST APIs', 'category': 'web_dev', 'level': 85, 'icon': '🔗'},
        
        # Development Tools & Platforms
        {'name': 'Git', 'category': 'tools', 'level': 85, 'icon': '📝'},
        {'name': 'GitHub', 'category': 'tools', 'level': 85, 'icon': '🐙'},
        {'name': 'Jupyter Notebooks', 'category': 'tools', 'level': 90, 'icon': '📓'},
    ]
    
    # Create skill objects
    for skill_data in skills_data:
        Skill.objects.create(**skill_data)
    
    # Update GPA in Education
    education = Education.objects.first()
    if education:
        education.gpa = "9.44/10.0"
        education.save()


def reverse_skills_and_gpa(apps, schema_editor):
    # Reverse migration - restore previous data if needed
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0012_update_portfolio_data_latest'),
    ]

    operations = [
        migrations.RunPython(update_skills_and_gpa, reverse_skills_and_gpa),
    ]
