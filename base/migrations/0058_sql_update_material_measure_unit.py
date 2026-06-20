from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0057_sql_populate_product_price'),
    ]

    operations = [
        migrations.RunSQL(
            sql="UPDATE base_material SET measure_unit = 'مللي/جرام';",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
