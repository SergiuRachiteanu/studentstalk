# Generated by Django 3.2.9 on 2021-12-09 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]