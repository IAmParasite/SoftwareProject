# Generated by Django 2.2.3 on 2020-06-04 03:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicDiscuss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='title', max_length=70, verbose_name='标题')),
                ('name', models.CharField(max_length=50, verbose_name='名字')),
                ('text', models.TextField(verbose_name='内容')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.TopicPost', verbose_name='话题')),
            ],
            options={
                'verbose_name': '话题讨论',
                'verbose_name_plural': '话题讨论',
            },
        ),
    ]
