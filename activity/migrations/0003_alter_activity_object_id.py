# Generated by Django 3.2.3 on 2021-10-07 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_alter_activity_activity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='object_id',
            field=models.CharField(max_length=200),
        ),
    ]
