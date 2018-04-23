# Generated by Django 2.0.4 on 2018-04-21 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0041_auto_20180421_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='TAsQueue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to='library.TA'),
        ),
        migrations.AlterField(
            model_name='document',
            name='instructorsQueue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to='library.Instructor'),
        ),
        migrations.AlterField(
            model_name='document',
            name='professorsQueue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to='library.Professor'),
        ),
        migrations.AlterField(
            model_name='document',
            name='studentsQueue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to='library.Student'),
        ),
        migrations.AlterField(
            model_name='document',
            name='visitingProfessorsQueue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to='library.VisitingProfessor'),
        ),
    ]