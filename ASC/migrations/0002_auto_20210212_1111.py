# Generated by Django 3.1.6 on 2021-02-12 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASC', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.FileField(upload_to='images'),
        ),
    ]
