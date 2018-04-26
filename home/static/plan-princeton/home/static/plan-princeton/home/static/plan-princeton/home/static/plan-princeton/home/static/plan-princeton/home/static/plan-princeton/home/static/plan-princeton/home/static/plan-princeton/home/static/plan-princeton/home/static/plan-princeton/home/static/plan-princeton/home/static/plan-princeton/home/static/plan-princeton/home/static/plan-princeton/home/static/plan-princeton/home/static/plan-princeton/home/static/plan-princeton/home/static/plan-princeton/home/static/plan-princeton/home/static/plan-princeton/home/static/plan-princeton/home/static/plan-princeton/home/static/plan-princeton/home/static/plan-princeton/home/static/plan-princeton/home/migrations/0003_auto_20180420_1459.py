# Generated by Django 2.0.4 on 2018-04-20 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20180420_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.Area'),
        ),
        migrations.AlterField(
            model_name='course',
            name='prereqs',
            field=models.ManyToManyField(related_name='_course_prereqs_+', to='home.Course'),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='completed_by_semester',
            field=models.IntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='course_list',
            field=models.ManyToManyField(to='home.Course'),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='description',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='double_counting_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='explanation',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='max_common_with_major',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='max_counted',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='min_needed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='pdfs_allowed',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='req_list',
            name='req_lists_inside',
            field=models.ManyToManyField(related_name='_req_list_req_lists_inside_+', to='home.Req_List'),
        ),
    ]
