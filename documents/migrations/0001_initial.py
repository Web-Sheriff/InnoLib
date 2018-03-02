import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Copy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('is_checked_out', models.BooleanField()),
                ('booking_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('price_value', models.IntegerField()),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Editor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250)),
                ('second_name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_date', models.DateField()),
                ('editors', models.ManyToManyField(related_name='issues', to='documents.Editor')),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AudioVideo',
            fields=[
                ('document_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='documents.Document')),
            ],
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('document_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='documents.Document')),
                ('is_best_seller', models.BooleanField()),
                ('edition', models.IntegerField()),
                ('publisher', models.CharField(max_length=100)),
                ('publish_time', models.DateField()),
            ],
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='JournalArticles',
            fields=[
                ('document_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='documents.Document')),
            ],
            bases=('documents.document',),
        ),
        migrations.AddField(
            model_name='issue',
            name='journal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='issues',
                                    to='documents.Journal'),
        ),
        migrations.AddField(
            model_name='document',
            name='authors',
            field=models.ManyToManyField(related_name='documents', to='users.Author'),
        ),
        migrations.AddField(
            model_name='document',
            name='keywords',
            field=models.ManyToManyField(related_name='documents', to='documents.Keyword'),
        ),
        migrations.AddField(
            model_name='document',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents',
                                    to='library.Library'),
        ),
        migrations.AddField(
            model_name='copy',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='copies',
                                    to='documents.Document'),
        ),
        migrations.AddField(
            model_name='copy',
            name='user_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='copies',
                                    to='library.UserCard'),
        ),
        migrations.AddField(
            model_name='journalarticles',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='journal_articles',
                                    to='documents.Issue'),
        ),
]