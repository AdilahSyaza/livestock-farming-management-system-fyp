# Generated by Django 3.2.8 on 2022-08-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldcattle',
            name='sc_pricePerKg',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='soldcattle',
            name='sc_salePrice',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='soldcattle',
            name='sc_saleWeight',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='soldsheep',
            name='ss_pricePerKg',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='soldsheep',
            name='ss_salePrice',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='soldsheep',
            name='ss_saleWeight',
            field=models.FloatField(default=0, null=True),
        ),
    ]
