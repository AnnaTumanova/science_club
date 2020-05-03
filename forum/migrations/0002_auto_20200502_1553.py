# Generated by Django 3.0.5 on 2020-05-02 13:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_first',
        ),
        migrations.RemoveField(
            model_name='threadpage',
            name='body',
        ),
        migrations.RemoveField(
            model_name='threadpage',
            name='date_closed',
        ),
        migrations.RemoveField(
            model_name='threadpage',
            name='date_opened',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(500)]),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(100)])),
                ('content', models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(1000)])),
                ('date_opened', models.DateField(auto_now_add=True)),
                ('date_closed', models.DateField(blank=True, default=None, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Thread'),
        ),
        migrations.AlterField(
            model_name='threadupvotes',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Thread'),
        ),
    ]
