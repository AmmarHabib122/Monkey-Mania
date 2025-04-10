# Generated by Django 5.1.6 on 2025-02-26 01:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_branchmaterial_measure_unit_material_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchmaterial',
            name='consumption',
        ),
        migrations.CreateModel(
            name='BranchProductMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumption', models.DecimalField(decimal_places=6, max_digits=14)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_product_materials_set', to='base.branchmaterial')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_consumptions_set', to='base.branchproduct')),
            ],
        ),
    ]
