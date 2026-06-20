from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0056_sql_populate_product_name'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                UPDATE base_product p
                SET price = (
                    SELECT bp.price
                    FROM base_branchproduct bp
                    WHERE bp.product_id = p.id
                      AND bp.price IS NOT NULL
                    ORDER BY bp.id
                    LIMIT 1
                )
                WHERE p.price IS NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
