# Generated by Django 2.2.28 on 2024-03-12 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pub_review', '0017_auto_20240312_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pub_question',
            name='author',
        ),
        migrations.RemoveField(
            model_name='pub_question',
            name='pub',
        ),
        migrations.DeleteModel(
            name='Pub_Answer',
        ),
        migrations.DeleteModel(
            name='Pub_Question',
        ),
    ]