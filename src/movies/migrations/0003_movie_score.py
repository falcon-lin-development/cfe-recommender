# Generated by Django 4.2.4 on 2023-09-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_rating_avg_movie_rating_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
