# Generated by Django 2.0.4 on 2018-04-22 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinterface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
