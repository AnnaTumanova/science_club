from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.search import index


class ArticleIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['ArticlePage']
    slug = 'article'


class ArticlePage(Page):
    parent_page_types = ['ArticleIndexPage']
    subpage_types = []

    date = models.DateField("Date added")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]
