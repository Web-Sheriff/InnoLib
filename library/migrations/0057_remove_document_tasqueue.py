# Generated by Django 2.0.4 on 2018-04-22 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0056_document_tasqueue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='TAsQueue',
        ),
    ]
