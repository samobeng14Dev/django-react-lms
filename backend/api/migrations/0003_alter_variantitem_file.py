# Generated by Django 4.2.7 on 2025-04-05 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_course_file_alter_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variantitem',
            name='file',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
