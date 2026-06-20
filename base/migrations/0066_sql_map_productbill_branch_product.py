from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0065_productbill_notes_productbillproduct_branch_product_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                UPDATE base_productbillproduct
                SET branch_product_id = product_id
                WHERE product_type_id = (
                    SELECT id FROM django_content_type
                    WHERE app_label = 'base' AND model = 'branchproduct'
                );
            """,
            reverse_sql="""
                UPDATE base_productbillproduct
                SET branch_product_id = NULL
                WHERE product_type_id = (
                    SELECT id FROM django_content_type
                    WHERE app_label = 'base' AND model = 'branchproduct'
                );
            """,
        ),
        migrations.RunSQL(
            sql="""
                UPDATE base_productbillreturnedproduct
                SET branch_product_id = product_id
                WHERE product_type_id = (
                    SELECT id FROM django_content_type
                    WHERE app_label = 'base' AND model = 'branchproduct'
                );
            """,
            reverse_sql="""
                UPDATE base_productbillreturnedproduct
                SET branch_product_id = NULL
                WHERE product_type_id = (
                    SELECT id FROM django_content_type
                    WHERE app_label = 'base' AND model = 'branchproduct'
                );
            """,
        ),
    ]
