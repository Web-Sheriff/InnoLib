# Generated by Django 2.0.4 on 2018-04-19 17:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0023_auto_20180418_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='document',
            name='is_best_seller',
        ),
        migrations.RemoveField(
            model_name='document',
            name='publisher',
        ),
        migrations.RemoveField(
            model_name='document',
            name='year',
        ),
        migrations.AddField(
            model_name='audiovideo',
            name='publisher',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audiovideo',
            name='year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='edition',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='is_best_seller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='availabledocs',
            name='rights_date',
            field=models.DateField(blank=True, null=True, verbose_name=datetime.datetime(2018, 4, 19, 17, 52, 19, 724585, tzinfo=utc)),
        ),
    ]
