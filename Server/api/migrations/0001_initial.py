# Generated by Django 4.0 on 2022-01-03 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoggerKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('settings', models.TextField()),
            ],
            options={
                'db_table': 'user_key',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('event_type', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('logger_key', models.ForeignKey(db_column='logger_key_id', on_delete=django.db.models.deletion.DO_NOTHING, to='api.loggerkey')),
            ],
            options={
                'db_table': 'event',
                'managed': True,
                'unique_together': {('timestamp', 'logger_key_id')},
            },
        ),
    ]
