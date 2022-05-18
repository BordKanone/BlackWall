# Generated by Django 3.2 on 2022-05-17 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_clientpurse_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientpurse',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail'),
        ),
        migrations.AddField(
            model_name='clientpurse',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Имя пользователя'),
        ),
        migrations.AddField(
            model_name='clientpurse',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Username'),
        ),
    ]
