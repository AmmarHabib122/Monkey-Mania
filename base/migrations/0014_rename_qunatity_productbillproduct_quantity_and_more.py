# Generated by Django 5.1.6 on 2025-03-01 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_bill_finished_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productbillproduct',
            old_name='qunatity',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='productbillreturnedproduct',
            old_name='qunatity',
            new_name='quantity',
        ),
        migrations.AlterField(
            model_name='productbill',
            name='bill_number',
            field=models.IntegerField(editable=False),
        ),
    ]
