# Generated by Django 2.2.28 on 2024-03-14 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pub_review', '0018_auto_20240312_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]