# Generated by Django 2.2.3 on 2020-06-02 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20200601_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='title',
            field=models.CharField(default='title', max_length=70, verbose_name='标题'),
        ),
    ]
