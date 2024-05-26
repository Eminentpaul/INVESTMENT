# Generated by Django 4.2.7 on 2023-11-27 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_investment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Successful', 'Successful'), ('Approved', 'Approved'), ('Confirmed', 'Comfirmed')], default='Pending', max_length=50),
        ),
    ]
