# Generated by Django 3.2.9 on 2022-01-05 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_message_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='banstatus',
            field=models.BooleanField(default=False),
        ),
    ]
