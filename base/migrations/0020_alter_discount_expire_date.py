# Generated by Django 5.1.6 on 2025-03-04 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_discount_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire_date',
            field=models.DateField(),
        ),
    ]
