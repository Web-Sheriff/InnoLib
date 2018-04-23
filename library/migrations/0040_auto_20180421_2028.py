# Generated by Django 2.0.4 on 2018-04-21 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0039_auto_20180421_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='user_card',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='copies', to='library.UserCard'),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='word',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='library',
            name='mail',
            field=models.EmailField(default='InnoLib@yandex.ru', max_length=64),
        ),
        migrations.AlterField(
            model_name='library',
            name='password',
            field=models.CharField(default='InnoTest', max_length=32),
        ),
    ]