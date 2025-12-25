# Generated migration to update profile image URL and ensure correct data

from django.db import migrations


def update_profile_image(apps, schema_editor):
    PersonalInfo = apps.get_model('api', 'PersonalInfo')
    
    # Update profile image URL to use media path
    PersonalInfo.objects.filter(id=3).update(
        profile_image='/media/profile/profile.jpg'
    )


def reverse_profile_image(apps, schema_editor):
    PersonalInfo = apps.get_model('api', 'PersonalInfo')
    
    # Reverse - change back to original
    PersonalInfo.objects.filter(id=3).update(
        profile_image='/images/profile.jpg'
    )


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0014_fix_profile_image_url'),
    ]

    operations = [
        migrations.RunPython(update_profile_image, reverse_profile_image),
    ]
