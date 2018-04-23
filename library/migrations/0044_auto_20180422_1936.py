# Generated by Django 2.0.4 on 2018-04-22 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0043_auto_20180422_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='instructors_queue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='instructors', to='library.InstructorsQueue'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='professors_queue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='professors', to='library.ProfessorsQueue'),
        ),
        migrations.AlterField(
            model_name='student',
            name='students_queue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='students', to='library.StudentsQueue'),
        ),
        migrations.AlterField(
            model_name='ta',
            name='TAs_Queue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='TAs', to='library.TAsQueue'),
        ),
        migrations.AlterField(
            model_name='visitingprofessor',
            name='visiting_professors_queue',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='visiting_professors', to='library.VisitingProfessorsQueue'),
        ),
    ]