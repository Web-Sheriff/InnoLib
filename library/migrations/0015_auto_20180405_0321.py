# Generated by Django 2.0.4 on 2018-04-05 00:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_auto_20180405_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabledocs',
            name='rights_date',
            field=models.DateField(verbose_name=datetime.datetime(2018, 4, 5, 0, 21, 9, 190226, tzinfo=utc)),
        ),
    ]
