# Generated by Django 2.0.4 on 2018-04-18 13:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_auto_20180417_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabledocs',
            name='rights_date',
            field=models.DateField(verbose_name=datetime.datetime(2018, 4, 18, 13, 5, 52, 832703, tzinfo=utc)),
        ),
    ]