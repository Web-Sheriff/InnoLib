# Generated by Django 2.0.4 on 2018-04-23 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0062_auto_20180422_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercard',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_card', to='library.User'),
        ),
    ]
