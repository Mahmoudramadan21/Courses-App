# Generated by Django 5.0.1 on 2024-02-04 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_course_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='numOfViews',
            new_name='_numOfViews',
        ),
    ]