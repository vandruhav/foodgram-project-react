# Generated by Django 2.2.28 on 2022-11-04 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20221104_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]