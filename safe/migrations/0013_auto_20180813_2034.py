# Generated by Django 2.0.5 on 2018-08-13 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safe', '0012_auto_20180813_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='safe',
            name='scanfreq',
            field=models.IntegerField(default=3600, verbose_name='Scan Frequency in Seconds'),
        ),
    ]
