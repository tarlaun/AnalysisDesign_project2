# Generated by Django 3.2.9 on 2021-11-15 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20211115_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='type',
        ),
        migrations.AddField(
            model_name='account',
            name='user_type',
            field=models.SmallIntegerField(choices=[(1, 'Doctor'), (2, 'Patient')], default=2, verbose_name='user_type'),
        ),
    ]