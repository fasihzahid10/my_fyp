# Generated by Django 3.2.5 on 2021-09-17 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TradingCenter', '0004_auto_20210917_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts_turn',
            name='ending_date',
            field=models.DateTimeField(null=True),
        ),
    ]