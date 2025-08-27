from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model("base", "User")
    phone = "122"   # your phone number
    password = "122"   # your password
    
    if not User.objects.filter(phone_number=phone).exists():
        user = User(
            phone_number=phone,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password(password)  # hash password
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_alter_bill_is_allowed_age'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
