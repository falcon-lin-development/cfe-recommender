# Generated by Django 4.2.4 on 2023-09-07 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ['-timestamp']},
        ),
    ]