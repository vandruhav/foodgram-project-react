# Generated by Django 2.2.28 on 2022-11-03 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20221103_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Пароль'),
        ),
    ]
