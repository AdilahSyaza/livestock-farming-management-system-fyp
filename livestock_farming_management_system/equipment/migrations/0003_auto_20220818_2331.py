# Generated by Django 3.2.8 on 2022-08-18 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_datejoined'),
        ('equipment', '0002_equimentusage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EquimentUsage',
            new_name='EquipmentUsage',
        ),
        migrations.AlterField(
            model_name='equipment',
            name='equipmentSerialID',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
