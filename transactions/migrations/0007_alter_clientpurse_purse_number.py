# Generated by Django 3.2 on 2022-05-18 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20220517_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientpurse',
            name='purse_number',
            field=models.CharField(max_length=255, unique=True, verbose_name='Номер кошелька'),
        ),
    ]
