# Generated by Django 5.1.6 on 2025-03-14 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0036_remove_productbillproduct_product_bill_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchoffer',
            name='expire_date',
            field=models.DateField(),
        ),
    ]
