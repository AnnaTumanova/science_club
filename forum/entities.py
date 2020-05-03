from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from forum import constants


class Thread(models.Model):
    subject = models.CharField(
        max_length=constants.THREAD_SUBJECT_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(constants.THREAD_SUBJECT_MIN_LENGTH),
            validators.MaxLengthValidator(constants.THREAD_SUBJECT_MAX_LENGTH)
        ]
    )
    content = models.CharField(
        max_length=constants.POST_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(constants.THREAD_CONTENT_MIN_LENGTH),
            validators.MaxLengthValidator(constants.THREAD_CONTENT_MAX_LENGTH)
        ]
    )
    date_opened = models.DateField(auto_now=False, auto_now_add=True)
    date_closed = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    content = models.CharField(
        max_length=constants.POST_MAX_LENGTH,
        validators=[
            validators.MinLengthValidator(constants.POST_MIN_LENGTH),
            validators.MaxLengthValidator(constants.POST_MAX_LENGTH)
        ]
    )
    date_added = models.DateField(auto_now=False, auto_now_add=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class ThreadUpvotes(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PostUpvotes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
