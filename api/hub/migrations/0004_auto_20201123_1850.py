# Generated by Django 3.1.3 on 2020-11-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0003_auto_20201123_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]