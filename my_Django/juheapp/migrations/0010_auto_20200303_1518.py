# Generated by Django 3.0.3 on 2020-03-03 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juheapp', '0009_auto_20200303_1515'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='user',
            name='emmmm',
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['nickname'], name='nickname'),
        ),
        migrations.AlterModelTable(
            name='user',
            table='juheapp_user',
        ),
    ]
