# Generated by Django 2.0.2 on 2018-03-24 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='identity_provider',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='logo_path',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
