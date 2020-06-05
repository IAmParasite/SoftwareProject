# Generated by Django 2.2.3 on 2020-06-04 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'verbose_name': '小组',
                'verbose_name_plural': '小组',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='TopicPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='话题')),
                ('body', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(verbose_name='修改时间')),
                ('excerpt', models.CharField(blank=True, max_length=200)),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'verbose_name': '话题',
                'verbose_name_plural': '话题',
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='书名')),
                ('body', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(verbose_name='修改时间')),
                ('excerpt', models.CharField(blank=True, max_length=200)),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Category', verbose_name='分类')),
                ('tags', models.ManyToManyField(blank=True, to='forum.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '书籍',
                'verbose_name_plural': '书籍',
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='MoviePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='影片')),
                ('body', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(verbose_name='修改时间')),
                ('excerpt', models.CharField(blank=True, max_length=200)),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Category', verbose_name='分类')),
                ('tags', models.ManyToManyField(blank=True, to='forum.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '影视',
                'verbose_name_plural': '影视',
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_join', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Group')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '小组关系',
            },
        ),
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='标题')),
                ('body', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(verbose_name='修改时间')),
                ('excerpt', models.CharField(blank=True, max_length=200)),
                ('views', models.PositiveIntegerField(default=0, editable=False)),
                ('top', models.BooleanField(default=False)),
                ('top_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='置顶时间')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grouptalk', to='forum.Group', verbose_name='小组名')),
            ],
            options={
                'verbose_name': '小组讨论',
                'verbose_name_plural': '小组讨论',
                'ordering': ['-created_time'],
                'permissions': (('grouppost_delete', '讨论删除权限'),),
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='forum.MemberShip', to=settings.AUTH_USER_MODEL),
        ),
    ]
