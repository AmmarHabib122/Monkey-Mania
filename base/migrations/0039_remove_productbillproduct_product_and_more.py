# Generated by Django 5.1.6 on 2025-03-15 03:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0038_alter_branchoffer_sold_units'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productbillproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productbillreturnedproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productbillreturnedproduct',
            name='product_bill',
        ),
        migrations.AddField(
            model_name='productbillproduct',
            name='product_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productbillreturnedproduct',
            name='product_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productbillreturnedproduct',
            name='product_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productbillproduct',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='productbillreturnedproduct',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_product_bill_returned_products_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
