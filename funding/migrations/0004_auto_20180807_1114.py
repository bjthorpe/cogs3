# Generated by Django 2.0.2 on 2018-08-07 11:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('funding', '0003_historicalattribution_historicalfundingbody_historicalfundingsource_historicalpublication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalpublication',
            name='identifier',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='identifier',
        ),
        migrations.AddField(
            model_name='historicalpublication',
            name='url',
            field=models.CharField(max_length=128, null=True, validators=[django.core.validators.URLValidator(schemes=['http', 'https'])], verbose_name='URL of the publication'),
        ),
        migrations.AddField(
            model_name='publication',
            name='url',
            field=models.CharField(max_length=128, null=True, validators=[django.core.validators.URLValidator(schemes=['http', 'https'])], verbose_name='URL of the publication'),
        ),
    ]
