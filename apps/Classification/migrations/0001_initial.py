# Generated by Django 4.1.2 on 2022-12-09 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskIdentification',
            fields=[
                ('task_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('time_creation', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
