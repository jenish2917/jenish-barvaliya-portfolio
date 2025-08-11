# Generated migration to fix profile image URL

from django.db import migrations


def fix_profile_image_url(apps, schema_editor):
    PersonalInfo = apps.get_model('api', 'PersonalInfo')
    
    # Update profile image URL to use media path
    PersonalInfo.objects.filter(profile_image='/images/profile.jpg').update(
        profile_image='/media/profile/profile.jpg'
    )


def reverse_profile_image_url(apps, schema_editor):
    PersonalInfo = apps.get_model('api', 'PersonalInfo')
    
    # Reverse - change back to original
    PersonalInfo.objects.filter(profile_image='/media/profile/profile.jpg').update(
        profile_image='/images/profile.jpg'
    )


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0013_update_skills_and_gpa'),
    ]

    operations = [
        migrations.RunPython(fix_profile_image_url, reverse_profile_image_url),
    ]
