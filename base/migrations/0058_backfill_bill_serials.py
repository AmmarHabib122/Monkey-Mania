from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('base', '0057_bill_notes_updated_by'),
    ]

    operations = [
        migrations.RunSQL(
            """
            UPDATE base_bill
            SET serial = id::text
            WHERE serial IS NULL
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
