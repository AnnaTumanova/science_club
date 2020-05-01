from django.contrib.auth.models import User
from django.db import models
from wagtail.core.models import Page
from django.core import validators
from forum import constants


class ForumPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['ThreadPage']
    slug = 'forum'


class ThreadPage(Page):
    parent_page_types = ['ForumPage']
    subpage_types = []


class Thread(models.Model):
    subject = models.CharField(
        max_length=constants.POST_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(constants.THREAD_MIN_LENGTH),
            validators.MaxLengthValidator(constants.THREAD_MAX_LENGTH)
        ]
    )
    date_opened = models.DateField(auto_now=False, auto_now_add=True)
    date_closed = models.DateField(auto_now=False, auto_now_add=False, null=True, default=None)


class Post(models.Model):
    content = models.CharField(
        max_length=constants.POST_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(constants.POST_MIN_LENGTH),
            validators.MaxLengthValidator(constants.POST_MAX_LENGTH)
        ]
    )
    is_first = models.BooleanField(default=False)
    date_added = models.DateField(auto_now=False, auto_now_add=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class PostUpvotes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_on = models.BooleanField()
