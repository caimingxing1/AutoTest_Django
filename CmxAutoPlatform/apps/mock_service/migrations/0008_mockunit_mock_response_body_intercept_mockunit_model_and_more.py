# Generated by Django 4.0.6 on 2023-04-28 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_service', '0007_mockproject_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockunit',
            name='mock_response_body_intercept',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='mockunit',
            name='model',
            field=models.CharField(blank=True, default='release', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='mockunit',
            name='response_headers',
            field=models.CharField(blank=True, default='{}', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='mockunit',
            name='state_code',
            field=models.IntegerField(default=200),
        ),
    ]
