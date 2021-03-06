# Generated by Django 2.0.5 on 2018-07-28 15:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('safe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyholder_msg', models.TextField()),
                ('keyholder_msg_timestamp', models.DateTimeField()),
                ('seen_by_safeholder', models.DateTimeField()),
                ('safeholder_msg', models.TextField()),
                ('safeholder_msg_timestamp', models.DateTimeField()),
                ('relationship_active', models.BooleanField()),
                ('keyholder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('safeholder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Safe_Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='safe',
            name='id',
        ),
        migrations.RemoveField(
            model_name='safe',
            name='kh_msg_text',
        ),
        migrations.RemoveField(
            model_name='safe',
            name='kh_msg_timestamp',
        ),
        migrations.RemoveField(
            model_name='safe',
            name='locked',
        ),
        migrations.RemoveField(
            model_name='safe',
            name='lockee_msg_text',
        ),
        migrations.RemoveField(
            model_name='safe',
            name='lockee_msg_timestamp',
        ),
        migrations.RemoveField(
            model_name='safe',
            name='safe_key_fp',
        ),
        migrations.AddField(
            model_name='safe',
            name='auth_to_unlock',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='safe',
            name='bolt_engaged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='safe',
            name='displayproximity',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='safe',
            name='hardware_id',
            field=models.CharField(default='abcd-1234', max_length=64, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='safe',
            name='hinge_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='safe',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(1900, 1, 1, 0, 0)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='safe',
            name='lid_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='safe',
            name='proximityunit',
            field=models.CharField(default='H', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='safe',
            name='reportfreq',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='safe',
            name='safe_public_key',
            field=models.TextField(default=b'-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAx4HPSdzneCyYQfa4lggS\njTA7oCW6N95SPAL9CAPKymtHgI3TLw0+Bx9UrueA+XqeyL0xFS7jTFNdAZZHo0Hw\nK/2fOuyiCo77UmONaNjJKewGD+WXY79WC6Pwu151ze61sCP0Z6D3ZJXC+EdsDSqe\nH2CG4N23iC77dk2inCNNq4S/fYSTyXap519u3eYB5EiMHDQIIkqoBsffGsNQu2Wh\nmmM2DyvTO0GCgxTYgge+NRejZgUiU4KWdEuXUU4jpi/yJi/wS3RrAgOe7dXDjsLC\nCUsG4bXgCwwYKFpp44iOgvdgr5AM1MMh4kushakVwnv7Pyk7Akc/wfmVQcQJ3LKZ\n1LK4g4n/Q1nX67WZ13Lhu1CAX9GzkPuPGX8EjSmrRVVvG/u/jqksp8mCBalicUDF\nRXwkYC3HX/Sz7qC9fHwDNJV6LvV2+zTPPABWNwY2zokC/T54m0dyGTPZvc218OXE\n5yxcowcimDyUaz/NP24LcQiuI+cnFeVtl1Z9/wszVACPlwVHkixJCs9AC8smxAsC\nvWHFam+jGmTWu8L4r2D5qCL3ndrH+Fx1z1NE2aY8Xn2Y5Jpr775BPjiCkGM8GFWH\nZlEfRcDo240Ge6G8k93Kbstnu+PDgYTMibv0ML0EAV4aJrBLjn5RO96ZBMzM3enl\naBdjCtgT1gltuyXdBEN7X90CAwEAAQ==\n-----END PUBLIC KEY-----\n'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='safe',
            name='safeholder',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='safe',
            name='scanfreq',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='safe_events',
            name='safe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='safe.Safe'),
        ),
    ]
