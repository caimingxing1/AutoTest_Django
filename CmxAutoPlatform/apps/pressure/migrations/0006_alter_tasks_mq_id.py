# Generated by Django 4.0.6 on 2023-05-09 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pressure', '0005_tasks_mq_id_alter_pressureplan_project_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='mq_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='任务的ID'),
        ),
    ]