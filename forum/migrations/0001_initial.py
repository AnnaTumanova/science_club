# Generated by Django 3.0.5 on 2020-05-01 13:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(1000)])),
                ('is_first', models.BooleanField(default=False)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(100)])),
                ('date_opened', models.DateField(auto_now_add=True)),
                ('date_closed', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThreadPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PostUpvotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_on', models.BooleanField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Thread'),
        ),
    ]
