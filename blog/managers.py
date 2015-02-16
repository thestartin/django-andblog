from collections import defaultdict

from django.db import models

from .constants import LIKES_UNLIKES
from .services import get_client_ip
from .models import ArticleSectionLikeUnlike


class ArticleSectionMixin(object):
    def get_article_with_sections(self):
        data = self.values(
            'article_id', 'article__slug', 'article__title', 'article__image', 'article__author',
            'article__tags', 'article__created_date_time', 'article__updated_by', 'article__updated_date_time', 'id',
            'section_order', 'title', 'content', 'likes', 'unlikes', 'abusive', 'score', 'updated_by',
            'updated_date_time'
        ).order_by(
            'article_id', 'article__slug', 'article__title', 'article__image', 'article__author',
            'article__tags', 'article__created_date_time', 'article__updated_by', 'article__updated_date_time', 'id',
            'section_order', 'title', 'content', 'likes', 'unlikes', 'abusive', 'score', 'updated_by',
            'updated_date_time'
        )

        result = defaultdict(list)
        for row in data:
            result[row['article_id']].append(row)

        return result

    def vote(self, article_section_id, attr, request):
        attr = attr.lower()
        article_section = self.get(pk=article_section_id)
        article_section_likes_unlikes, created = ArticleSectionLikeUnlike.objects.get_or_create(
            who=get_client_ip(request)
        )

        if not created:
            setattr(article_section, attr, getattr(article_section, attr) + 1)
            article_section.save()
            article_section_likes_unlikes.vote_type = LIKES_UNLIKES[attr]
            article_section_likes_unlikes.voted_by(request.user)
            article_section_likes_unlikes.save()
            return True
        else:
            return False

class PublishedArticleSectionManager(ArticleSectionMixin, models.Manager):
    def get_queryset(self):
        return super(PublishedArticleSectionManager, self).get_queryset().filter(article__published=True)


class UnPublishedArticleSectionManager(ArticleSectionMixin, models.Manager):
    def get_queryset(self):
        return super(UnPublishedArticleSectionManager, self).get_queryset().filter(article__published=False)


class AllArticleSectionManager(ArticleSectionMixin, models.Manager):
    def get_queryset(self):
        return super(AllArticleSectionManager, self).get_queryset()
