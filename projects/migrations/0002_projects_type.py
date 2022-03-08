# Generated by Django 4.0.1 on 2022-02-07 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='type',
            field=models.CharField(blank=True, choices=[('static', 'static application'), ('dynamic', 'dynamic application')], max_length=20, null=True),
        ),
    ]
