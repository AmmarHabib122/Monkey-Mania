from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model("base", "User")
    phone = "122"   # your phone number
    password = "122"   # your password
    if not User.objects.filter(phone_number=phone).exists():
        User.objects.create_superuser(
            phone_number=phone,
            password=password
        )

class Migration(migrations.Migration):

    dependencies = [
        ('base', 'the_last_migration_here'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
