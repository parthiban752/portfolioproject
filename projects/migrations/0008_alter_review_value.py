# Generated by Django 4.0.1 on 2022-02-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_tag_alter_project_image_review_project_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='value',
            field=models.CharField(choices=[('up', 'like'), ('down', 'unlike')], default='up', max_length=20),
        ),
    ]
