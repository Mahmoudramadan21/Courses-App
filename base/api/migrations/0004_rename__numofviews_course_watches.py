# Generated by Django 5.0.1 on 2024-02-04 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_numofviews_course__numofviews'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='_numOfViews',
            new_name='watches',
        ),
    ]
