from collections import defaultdict

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from social.apps.django_app.default.models import UserSocialAuth
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager


class Article(models.Model):
    """
    Article model
    """
    slug = models.SlugField(max_length=150)
    title = models.CharField(max_length=150)
    image = ImageField(upload_to=settings.UPLOAD_TO, blank=True, null=True)
    author = models.ForeignKey(UserSocialAuth)
    published = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(UserSocialAuth, related_name='updated_by')
    updated_date_time = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def add_article(self, data, user, fields):
        self.title = data['title']
        self.image = data['image']
        self.tags = data['tags']
        self.slug = slugify(self.title)
        self.author = user
        self.updated_by = user
        self.save()

        article_section = ArticleSection()
        article_section.article = self
        article_section.section_order = 1
        article_section.title = self.title
        article_section.content = self.content
        article_section.save()

        sections = defaultdict(ArticleSection)
        for key, value in data.iteritems():
            if '_' in key:
                keys = key.split('_')
                sort_order = int(keys[-1])
                sections[sort_order].section_order = sort_order
                if hasattr(sections[sort_order], keys[0]):
                    setattr(sections[sort_order], keys[0], value)
        
        for sort_order_num, section in sections.iteritems():
            section.save()

class ArticleSection(models.Model):
    article = models.ForeignKey(Article)
    section_order = models.IntegerField(max_length=2) # This must have been a composite key, but Django ORM does not support it
    title = models.CharField(max_length=150)
    content = models.TextField()
    likes = models.IntegerField(max_length=4, default=0)
    unlikes = models.IntegerField(max_length=4, default=0)
    abusive = models.IntegerField(max_length=3, default=0)
    updated_by = models.ForeignKey(UserSocialAuth)
    updated_date_time = models.DateTimeField(auto_now=True)


class ArticleSectionLikeUnlike(models.Model):
    section = models.ForeignKey(ArticleSection)
    who = models.CharField(max_length=255)  # This is an hashed IP field for preventing spams
    vote_type = models.CharField(max_length=1)  # 0 - Unlike, 1- Like, 9 - Abusive
    voted_by = models.ForeignKey(UserSocialAuth)
    voted_date_time = models.DateTimeField(auto_now_add=True)


class ArticleSectionComment(models.Model):
    section = models.ForeignKey(ArticleSection)
    title = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)  # Only approved comments are visible
    commented_by = models.ForeignKey(UserSocialAuth)
    commented_date_time = models.DateTimeField(auto_now_add=True)

