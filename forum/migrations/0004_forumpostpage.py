# Generated by Django 3.0.5 on 2020-05-03 19:19

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.routable_page.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('forum', '0003_delete_threadpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumPostPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
    ]
