# Generated by Django 2.2.28 on 2024-03-11 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pub_review', '0013_auto_20240312_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='firstName',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nationality',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
