# Generated by Django 2.0.4 on 2018-04-20 23:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0031_auto_20180421_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabledocs',
            name='rights_date',
            field=models.DateField(blank=True, null=True, verbose_name=datetime.datetime(2018, 4, 20, 23, 15, 21, 474436, tzinfo=utc)),
        ),
    ]
