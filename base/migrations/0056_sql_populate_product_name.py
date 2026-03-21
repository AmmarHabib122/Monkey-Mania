from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0059_remove_branchmaterial_available_units_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                UPDATE base_product
                SET name = layer2 || ' ' || layer3
                WHERE name IS NULL OR name = '';
            """,
            reverse_sql="""
                UPDATE base_product
                SET name = NULL
                WHERE name = layer2 || ' ' || layer3;
            """,
        ),
    ]
