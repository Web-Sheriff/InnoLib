# Generated by Django 2.0.4 on 2018-04-18 13:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0020_auto_20180418_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabledocs',
            name='rights_date',
            field=models.DateField(blank=True, null=True, verbose_name=datetime.datetime(2018, 4, 18, 13, 20, 28, 861692, tzinfo=utc)),
        ),
    ]
