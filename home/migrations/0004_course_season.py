# Generated by Django 2.0.4 on 2018-05-08 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_merge_20180507_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='season',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
