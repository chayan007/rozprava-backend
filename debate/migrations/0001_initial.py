# Generated by Django 3.1.4 on 2021-01-10 13:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activity', '0001_initial'),
        ('profiles', '0001_initial'),
        ('case', '0001_initial'),
        ('proof', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('comment', models.TextField()),
                ('inclination', models.SmallIntegerField(choices=[(1, 'For'), (0, 'Against')], default=1)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.case')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
                ('proofs', models.ManyToManyField(to='proof.Proof')),
                ('tags', models.ManyToManyField(to='activity.Tag')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
