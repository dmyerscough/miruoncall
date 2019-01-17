# Generated by Django 2.1.4 on 2019-01-14 06:09

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotations',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('annotation', models.TextField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incidents',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=25)),
                ('description', models.TextField(max_length=100)),
                ('summary', models.TextField(max_length=100)),
                ('status', models.TextField(max_length=12)),
                ('actionable', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField()),
                ('incident_id', models.TextField(max_length=20, unique=True)),
                ('urgency', models.TextField(max_length=15)),
                ('annotation', models.ForeignKey(blank=True, null=True, on_delete=False, to='oncall.Annotations')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('team_id', models.TextField()),
                ('summary', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_checked', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='incidents',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncall.Team'),
        ),
    ]
