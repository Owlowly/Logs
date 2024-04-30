# Generated by Django 4.1.9 on 2023-11-23 03:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_profile_total_followers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='users/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png']), django.core.validators.MaxValueValidator(6291456, message='File size must be no more than 6 MB')]),
        ),
    ]
