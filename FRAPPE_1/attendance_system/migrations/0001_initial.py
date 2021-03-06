# Generated by Django 2.0.6 on 2018-11-19 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management_system', '0006_auto_20181110_0628'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=100)),
                ('was_alert', models.BooleanField(default=False)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_system.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='PendingAlerts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=100)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_system.Employee')),
            ],
        ),
    ]
