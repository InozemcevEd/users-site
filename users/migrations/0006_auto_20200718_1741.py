# Generated by Django 3.0.8 on 2020-07-18 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_myuser_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='age',
            field=models.PositiveIntegerField(default=0),
        ),
    ]