# Generated by Django 2.0.6 on 2018-11-09 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='has_admin_acc',
            field=models.BooleanField(default=False),
        ),
    ]
