# Generated by Django 2.0.4 on 2018-04-22 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0059_auto_20180422_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='TAsQueue',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='documents', to='library.TA'),
        ),
    ]
