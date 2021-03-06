# Generated by Django 3.0.8 on 2020-07-03 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RssModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_title', models.TextField()),
                ('feed_url', models.URLField(unique=True)),
                ('feed_user', models.CharField(max_length=50)),
                ('feed_update', models.DateTimeField(null=True)),
            ],
        ),
    ]
