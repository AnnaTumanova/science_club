from django.contrib import messages
from django.contrib.auth.models import User
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from forum.entities import Thread, Post
from forum.forms import ThreadForm, PostForm


class ForumPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['ForumThreadPage']
    slug = 'forum'

    form = None
    threads = None

    def serve(self, request, *args, **kwargs):
        self.form = ThreadForm(request.POST or None)

        if request.method == 'POST' and self.form.is_valid():
            try:
                data = self.form.cleaned_data
                thread = Thread(
                    subject=data['subject'],
                    content=data['content'],
                    author=request.user
                )
                thread.save()
                messages.success(request, 'Your thread has been created')
                self.form = ThreadForm(None)
            except:
                messages.error(request, 'An error occurred during thread creation. Please try again later')

        self.threads = Thread.objects.all()

        return super().serve(request)


class ForumThreadPage(RoutablePageMixin, Page):
    parent_page_types = ['ForumPage']
    subpage_types = []
    slug = 'threads'

    form = PostForm()
    thread = None

    @route(r'^$')
    def thread_list_view(self, request):
        return ForumPage().serve(request)

    @route(r'^(\d+)/$')
    def thread_view(self, request, thread_pk=None):
        try:
            self.thread = Thread.objects.get(pk=thread_pk)
        except Thread.DoesNotExist:
            messages.error(request, 'Thread deleted or never existed')
            return ForumPage().serve(request)

        self.form = PostForm(request.POST or None)

        if request.method == 'POST' and self.form.is_valid():
            try:
                data = self.form.cleaned_data
                post = Post(
                    content=data['content'],
                    author=request.user,
                    thread=self.thread
                )
                post.save()
                messages.success(request, 'Your post has been created')
                self.form = PostForm(None)
            except:
                messages.error(request, 'An error occurred during post creation. Please try again later')

        return super().serve(request)
