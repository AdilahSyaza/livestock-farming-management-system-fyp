# Generated by Django 3.2.8 on 2023-05-04 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_datejoined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reasonDeactivation',
            field=models.CharField(default='Not Applicable', max_length=150, null=True),
        ),
    ]