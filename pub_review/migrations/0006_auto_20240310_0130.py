# Generated by Django 2.2.28 on 2024-03-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pub_review', '0005_auto_20240310_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='modify_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='modify_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
