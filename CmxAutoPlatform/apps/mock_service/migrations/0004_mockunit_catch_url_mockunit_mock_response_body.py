# Generated by Django 4.0.6 on 2023-04-26 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_service', '0003_mockunit'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockunit',
            name='catch_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='mockunit',
            name='mock_response_body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
