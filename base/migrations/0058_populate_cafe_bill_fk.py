from django.db import migrations


class Migration(migrations.Migration):
    """
    Data migration: copies the cafe_bill relationship from the old M2M junction
    tables (base_cafebill_items, base_cafebill_returns) into the new FK columns
    on CafeBillItem and CafeBillReturn.

    M2M junction table columns:
      base_cafebill_items:   cafebill_id, cafebillitem_id
      base_cafebill_returns: cafebill_id, cafebillreturn_id
    """

    dependencies = [
        ('base', '0057_add_cafe_bill_fk_nullable'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                UPDATE base_cafebillitem
                SET cafe_bill_id = (
                    SELECT cafebill_id
                    FROM base_cafebill_items
                    WHERE cafebillitem_id = base_cafebillitem.id
                    LIMIT 1
                )
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql="""
                UPDATE base_cafebillreturn
                SET cafe_bill_id = (
                    SELECT cafebill_id
                    FROM base_cafebill_returns
                    WHERE cafebillreturn_id = base_cafebillreturn.id
                    LIMIT 1
                )
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
