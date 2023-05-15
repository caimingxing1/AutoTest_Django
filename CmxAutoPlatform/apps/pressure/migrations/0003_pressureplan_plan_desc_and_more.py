# Generated by Django 4.0.6 on 2023-05-06 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pressure', '0002_pressureplan_project_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pressureplan',
            name='plan_desc',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='项目描述'),
        ),
        migrations.AlterField(
            model_name='pressureplan',
            name='pressure_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='压测类型'),
        ),
        migrations.AlterField(
            model_name='pressureplan',
            name='project_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='项目名称'),
        ),
    ]