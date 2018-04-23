# Generated by Django 2.0.4 on 2018-04-22 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0047_auto_20180422_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='TAsQueue',
            field=models.ManyToManyField(to='library.TA'),
        ),
        migrations.AlterField(
            model_name='document',
            name='instructorsQueue',
            field=models.ManyToManyField(to='library.Instructor'),
        ),
        migrations.AlterField(
            model_name='document',
            name='professorsQueue',
            field=models.ManyToManyField(to='library.Professor'),
        ),
        migrations.AlterField(
            model_name='document',
            name='studentsQueue',
            field=models.ManyToManyField(to='library.Student'),
        ),
        migrations.AlterField(
            model_name='document',
            name='visitingProfessorsQueue',
            field=models.ManyToManyField(to='library.VisitingProfessor'),
        ),
    ]
