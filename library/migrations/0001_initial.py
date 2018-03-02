
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_card_number', models.CharField(max_length=100)),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_cards',
                                              to='library.Library')),
                ('users', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_card',
                                              to='users.User')),
            ],
        ),
]