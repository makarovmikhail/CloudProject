# Generated by Django 2.0.4 on 2018-04-22 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_predicts', models.IntegerField(default=7)),
                ('n_splits', models.IntegerField(default=3)),
            ],
        ),
    ]
