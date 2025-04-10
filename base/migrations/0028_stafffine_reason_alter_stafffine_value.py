# Generated by Django 5.1.6 on 2025-03-09 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_stafffine_staffwithdraw'),
    ]

    operations = [
        migrations.AddField(
            model_name='stafffine',
            name='reason',
            field=models.CharField(default='dfs', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stafffine',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
