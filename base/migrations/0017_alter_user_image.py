# Generated by Django 4.2.7 on 2023-11-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_recommendation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='avatar.svg', null=True, upload_to='user/'),
        ),
    ]
