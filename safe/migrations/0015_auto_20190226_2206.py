# Generated by Django 2.1.5 on 2019-02-26 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safe', '0014_auto_20180813_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='safe',
            name='reportfreq',
            field=models.IntegerField(default=1, verbose_name='Reporting Frequency (number of scan periods)'),
        ),
        migrations.AlterField(
            model_name='safe',
            name='scanfreq',
            field=models.IntegerField(default=300, verbose_name='Scan Frequency in Seconds'),
        ),
    ]
