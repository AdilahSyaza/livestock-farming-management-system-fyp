# Generated by Django 3.2.8 on 2022-08-30 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_datejoined'),
        ('animal', '0007_auto_20220823_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cattle',
            name='cattleDam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cattle_Dam', to='animal.cattle'),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='cattleLastUpdatedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='cattleSire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cattle_Sire', to='animal.cattle'),
        ),
        migrations.AlterField(
            model_name='sheep',
            name='sheepDam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sheep_Dam', to='animal.sheep'),
        ),
        migrations.AlterField(
            model_name='sheep',
            name='sheepLastUpdatedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AlterField(
            model_name='sheep',
            name='sheepSire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sheep_Sire', to='animal.sheep'),
        ),
    ]
