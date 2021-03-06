# Generated by Django 2.0.4 on 2018-04-04 22:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_auto_20180405_0140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='book',
            name='publisher',
        ),
        migrations.AddField(
            model_name='document',
            name='edition',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='publisher',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='availabledocs',
            name='rights_date',
            field=models.DateField(verbose_name=datetime.datetime(2018, 4, 4, 22, 41, 38, 290135, tzinfo=utc)),
        ),
    ]
