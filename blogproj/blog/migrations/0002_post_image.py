# Generated by Django 5.1.5 on 2025-04-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='blog_pics'),
        ),
    ]
