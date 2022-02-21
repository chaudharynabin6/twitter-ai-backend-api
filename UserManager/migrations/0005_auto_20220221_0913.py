# Generated by Django 3.2.9 on 2022-02-21 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManager', '0004_auto_20220221_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteruser',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='isAnalysing',
            field=models.BooleanField(default=False),
        ),
    ]