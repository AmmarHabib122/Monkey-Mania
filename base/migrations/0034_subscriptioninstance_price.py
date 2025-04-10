# Generated by Django 5.1.6 on 2025-03-14 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_rename_branches_subscription_creatable_in_branches_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptioninstance',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
            preserve_default=False,
        ),
    ]
