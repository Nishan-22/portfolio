from django.db import migrations
from django.contrib.auth import get_user_model
import os

def create_superuser(apps, schema_editor):
    User = get_user_model()
    
    # Get credentials from environment variables
    username = os.getenv('ADMIN_USERNAME', 'admin')
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_blogpost'),  # Adjust to your latest migration
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
