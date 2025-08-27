from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_superuser(apps, schema_editor):
    User = apps.get_model("base", "User")
    phone = "122"
    password = "122"

    if not User.objects.filter(phone_number=phone).exists():
        User.objects.create(
            phone_number=phone,
            password=make_password(password),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_alter_bill_is_allowed_age'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
