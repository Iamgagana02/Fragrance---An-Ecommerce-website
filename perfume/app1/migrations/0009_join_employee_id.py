# Generated by Django 5.0.2 on 2024-07-04 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_alter_join_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='join',
            name='employee_id',
            field=models.IntegerField(default=0),
        ),
    ]
