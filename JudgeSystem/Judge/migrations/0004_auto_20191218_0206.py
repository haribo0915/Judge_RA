# Generated by Django 2.2.7 on 2019-12-17 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Judge', '0003_auto_20191218_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='source',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='ip',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='motto',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='solved_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='submit_num',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]