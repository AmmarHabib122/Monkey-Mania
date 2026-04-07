import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_populate_cafe_bill_fk'),
    ]

    operations = [
        # Drop the M2M fields (and their junction tables) from CafeBill
        migrations.RemoveField(
            model_name='cafebill',
            name='items',
        ),
        migrations.RemoveField(
            model_name='cafebill',
            name='returns',
        ),
        # Make the FK non-nullable and rename related_name to 'items' / 'returns'
        migrations.AlterField(
            model_name='cafebillitem',
            name='cafe_bill',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='items',
                to='base.cafebill',
            ),
        ),
        migrations.AlterField(
            model_name='cafebillreturn',
            name='cafe_bill',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='returns',
                to='base.cafebill',
            ),
        ),
    ]
