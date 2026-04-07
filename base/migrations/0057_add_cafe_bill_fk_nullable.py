import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0056_remove_cafebill_products_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafebillitem',
            name='cafe_bill',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='items_fk',
                to='base.cafebill',
            ),
        ),
        migrations.AddField(
            model_name='cafebillreturn',
            name='cafe_bill',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='returns_fk',
                to='base.cafebill',
            ),
        ),
    ]
