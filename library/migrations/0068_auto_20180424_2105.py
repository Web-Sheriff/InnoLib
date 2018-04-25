# Generated by Django 2.0.1 on 2018-04-24 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0067_auto_20180424_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiovideo',
            name='year',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='copy',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copies', to='library.Document'),
        ),
        migrations.AlterField(
            model_name='document',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='library.Library'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='library.Library'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fine',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(default='User', max_length=32),
        ),
        migrations.AlterField(
            model_name='usercard',
            name='library',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_cards', to='library.Library'),
        ),
    ]