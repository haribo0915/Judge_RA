# Generated by Django 2.2.7 on 2019-12-25 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Judge', '0005_auto_20191218_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='chek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='defunct',
            field=models.BooleanField(null=True),
        ),
    ]