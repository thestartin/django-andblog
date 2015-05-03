from collections import defaultdict

from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .constants import LIKES_UNLIKES
from .services import get_client_ip
from .mixins import ArticleFilterMixin, ArticleSectionMixin


class PublishedArticleSectionManager(models.Manager, ArticleSectionMixin):
    def get_queryset(self):
        return super(PublishedArticleSectionManager, self).get_queryset().filter(article__published=True)


class UnPublishedArticleSectionManager(models.Manager, ArticleSectionMixin):
    def get_queryset(self):
        return super(UnPublishedArticleSectionManager, self).get_queryset().filter(article__published=False)


class AllArticleSectionManager(models.Manager, ArticleSectionMixin):
    def get_queryset(self):
        return super(AllArticleSectionManager, self).get_queryset()


class ArticleManager(models.Manager, ArticleFilterMixin):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset()


class ArticlePublishedManager(models.Manager, ArticleFilterMixin):
    def get_queryset(self):
        return super(ArticlePublishedManager, self).get_queryset().filter(published=True)
