# Generated by Django 4.0.6 on 2023-04-28 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock_service', '0008_mockunit_mock_response_body_intercept_mockunit_model_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockunit',
            name='mock_time',
            field=models.FloatField(default=0.0),
        ),
    ]
