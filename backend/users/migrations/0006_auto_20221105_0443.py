# Generated by Django 2.2.28 on 2022-11-04 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20221105_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Пароль'),
        ),
    ]
