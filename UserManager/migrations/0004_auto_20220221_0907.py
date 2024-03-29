# Generated by Django 3.2.9 on 2022-02-21 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManager', '0003_alter_twitteruser_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='user_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='profile_image_url',
            field=models.URLField(blank=True, default='http://'),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='protected',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='url',
            field=models.URLField(blank=True, default='http://'),
        ),
    ]
