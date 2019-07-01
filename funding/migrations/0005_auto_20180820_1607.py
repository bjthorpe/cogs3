# Generated by Django 2.0.2 on 2018-08-20 16:07

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('funding', '0004_auto_20180807_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundingsource',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Grant attributable to Supercomputing Wales (in £)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalfundingsource',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Grant attributable to Supercomputing Wales (in £)'),
            preserve_default=False,
        ),
    ]
