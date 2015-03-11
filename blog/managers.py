from collections import defaultdict

from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .constants import LIKES_UNLIKES
from .services import get_client_ip


class ArticleSectionMixin(object):

    def vote(self, form_data, who, user):
        from .models import ArticleSectionLikeUnlike
        article_section_id = form_data['section']
        vote_type = form_data['vote_type']

        if vote_type == 0:
            attr = 'unlikes'
        elif vote_type == 1:
            attr = 'likes'
        elif vote_type == 9:
            attr = 'abusive'
        else:
            attr = 'likes'

        article_section = self.get(pk=article_section_id)
        article_section_likes_unlikes = ArticleSectionLikeUnlike._default_manager.filter(
            who=who,
            section=article_section
        )

        if not article_section_likes_unlikes:
            article_section_likes_unlikes = ArticleSectionLikeUnlike()
            article_section_likes_unlikes.who = who
            article_section_likes_unlikes.section = article_section
            setattr(article_section, attr, getattr(article_section, attr) + 1)
            article_section.save()
            article_section_likes_unlikes.vote_type = int(vote_type)
            article_section_likes_unlikes.voted_by = user
            article_section_likes_unlikes.save()
            return True
        else:
            return False


class PublishedArticleSectionManager(models.Manager, ArticleSectionMixin):
    def get_queryset(self):
        return super(PublishedArticleSectionManager, self).get_queryset().filter(article__published=True)


class UnPublishedArticleSectionManager(models.Manager, ArticleSectionMixin):
    def get_queryset(self):
        return super(UnPublishedArticleSectionManager, self).get_queryset().filter(article__published=False)


class AllArticleSectionManager(models.Manager, ArticleSectionMixin):
    def get_queryset(self):
        return super(AllArticleSectionManager, self).get_queryset()


class ArticleManager(models.Manager):
    pass