# Generated by Django 5.1.6 on 2025-03-14 01:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_subscription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='branches',
            new_name='creatable_in_branches',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='duration',
            new_name='instance_duration',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='expire_date',
        ),
        migrations.AddField(
            model_name='bill',
            name='is_subscription',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill',
            name='subscription',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='subscription_bills_set', to='base.subscription'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='hours',
            field=models.DecimalField(decimal_places=2, default=30, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='price',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='sold_units',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='usable_in_branches',
            field=models.ManyToManyField(related_name='visit_branch_subscriptions_set', to='base.branch'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='half_hour_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='bill',
            name='hour_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.CreateModel(
            name='SubscriptionInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('instapay', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('visa', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('hours', models.DecimalField(decimal_places=2, max_digits=5)),
                ('expire_date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='branch_subscription_instances_set', to='base.branch')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions_set', to='base.child')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_subscription_instances_set', to=settings.AUTH_USER_MODEL)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscription_instances_set', to='base.subscription')),
            ],
        ),
    ]
