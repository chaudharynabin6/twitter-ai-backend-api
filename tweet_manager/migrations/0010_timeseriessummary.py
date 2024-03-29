# Generated by Django 3.2.9 on 2022-02-22 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManager', '0005_auto_20220221_0913'),
        ('tweet_manager', '0009_totalsummary'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSeriesSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.SmallIntegerField(default=0)),
                ('positive', models.PositiveBigIntegerField(default=0)),
                ('negative', models.PositiveBigIntegerField(default=0)),
                ('total', models.PositiveBigIntegerField(default=0)),
                ('twitter_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='twitter_user_for_time_series_summary', to='UserManager.twitteruser')),
            ],
        ),
    ]
