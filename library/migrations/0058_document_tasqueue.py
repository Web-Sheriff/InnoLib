# Generated by Django 2.0.4 on 2018-04-22 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0057_remove_document_tasqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='TAsQueue',
            field=models.ManyToManyField(blank=True, default=None, related_name='documents', to='library.TA'),
        ),
    ]