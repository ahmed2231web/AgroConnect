# Generated by Django 5.1.3 on 2024-12-08 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_city_customuser_province_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(error_messages={'blank': 'City field is required', 'null': 'City field is required'}, max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='province',
            field=models.CharField(error_messages={'blank': 'Province field is required', 'null': 'Province field is required'}, max_length=20),
        ),
    ]
