from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0053_alter_bill_subscription'),
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
