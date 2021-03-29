# Generated by Django 3.1.5 on 2021-03-29 18:37

import ads.utilities
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=ads.utilities.get_ads_image_upload_path)),
                ('video', models.FileField(blank=True, null=True, upload_to=ads.utilities.get_ads_video_upload_path)),
                ('is_active', models.BooleanField(default=False)),
                ('starting_date', models.DateField()),
                ('ending_date', models.DateField()),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('is_event', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
