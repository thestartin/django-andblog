from collections import defaultdict

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.http import Http404
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager
from autoslug.fields import AutoSlugField
from django_bitly.models import Bittle

from .managers import PublishedArticleSectionManager, UnPublishedArticleSectionManager, AllArticleSectionManager, \
    ArticleManager, ArticlePublishedManager


class Article(models.Model):
    """
    Article model
    """
    slug = AutoSlugField(max_length=150, unique=True)
    title = models.CharField(max_length=150)
    image = ImageField(upload_to=settings.UPLOAD_TO, blank=True, null=True, max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    published = models.BooleanField(default=False)
    tags = TaggableManager()
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_by')
    updated_date_time = models.DateTimeField(auto_now=True)

    objects = ArticleManager()
    pub = ArticlePublishedManager()

    class Meta:
        ordering = ['-updated_date_time']

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return ''.join(['http://', get_current_site(None).domain, reverse('blog:blog_detail', args=[self.slug])])

    def get_social_url(self, social_name):
        data = dict()
        data['url'] = settings.USE_BITLY and Bittle.objects.bitlify(self).shortUrl or self.get_absolute_url()
        data['title'] = self.title[:100]
        return settings.SOCIAL_LINKS[social_name].format(**data)

    def get_facebook_url(self):
        return self.get_social_url('facebook')

    def get_twitter_url(self):
        return self.get_social_url('twitter')

    def get_googleplus_url(self):
        return self.get_social_url('googleplus')

    def add_article(self, data, user):
        self.title = data['title']
        self.image = data['image']
        self.slug = slugify(self.title)
        self.author = user
        self.updated_by = user
        self.save()
        if isinstance(data['tags'], list):
            map(self.tags.add, data['tags'])
        else:
            self.tags.add(data['tags'])

        self.add_article_sections(data, user)

    def add_article_sections(self, data, user):
        article_section = ArticleSection()
        article_section.article = self
        article_section.section_order = 1
        article_section.title = self.title
        article_section.content = data['content']
        article_section.score = data.get('score', 0)
        article_section.updated_by = user
        article_section.save()
        ArticleSection.objects.all()

        sections = defaultdict(ArticleSection)
        for key, value in data.iteritems():
            if '_' in key:
                keys = key.split('_')
                sort_order = int(keys[-1])
                sections[sort_order].section_order = sort_order
                if hasattr(sections[sort_order], keys[0]):
                    setattr(sections[sort_order], keys[0], value)

        for sort_order_num, section in sections.iteritems():
            section.article = self
            section.updated_by = user
            section.save()

    def update_article(self, data, changed, user):
        if 'image' in changed:
            self.image = data['image']

        if 'tags' in changed:
            if isinstance(data['tags'], list):
                map(self.tags.add, data['tags'])
            else:
                self.tags.add(data['tags'])

        self.updated_by = user
        self.save()

        sections = {}
        for key, value in data.iteritems():
            if key.startswith('id'):
                # If the key is id that is section id which would have already been used
                continue

            if '_' in key:
                keys = key.split('_')
                sort_order = int(keys[-1])
                section_id = data['id_' + str(sort_order)]
            else:
                # Dont Allow title of main section to be updated, it is read only but still a check to keep hackers away.
                if key == 'title' or key == 'tags':
                    continue
                sort_order = 1
                section_id = data['id']

            try:
                if sort_order not in sections:
                    sections[sort_order] = ArticleSection.objects.get(pk=section_id)
                col = key if sort_order == 1 else keys[0]
                if hasattr(sections[sort_order], col) and key in changed:
                    setattr(sections[sort_order], col, value)

            except ObjectDoesNotExist:
                raise Http404

        for sort_order_num, section in sections.iteritems():
            section.updated_by = user
            section.save()


class ArticleSection(models.Model):
    article = models.ForeignKey(Article)
    section_order = models.IntegerField(max_length=2) # This must have been a composite key, but Django ORM does not support it
    title = models.CharField(max_length=150)
    content = models.TextField()
    likes = models.IntegerField(max_length=4, default=0)
    unlikes = models.IntegerField(max_length=4, default=0)
    abusive = models.IntegerField(max_length=3, default=0)
    score = models.DecimalField(decimal_places=1, max_digits=settings.RATING_MAX_DIGITS, default=0)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    updated_date_time = models.DateTimeField(auto_now=True)

    objects = AllArticleSectionManager()
    pub = PublishedArticleSectionManager()
    unpub = UnPublishedArticleSectionManager()

    class Meta:
        ordering = ["article_id", "section_order"]


class ArticleSectionLikeUnlike(models.Model):
    section = models.ForeignKey(ArticleSection)
    who = models.CharField(max_length=255)  # This is an hashed IP field for preventing spams
    vote_type = models.CharField(max_length=1)  # 0 - Unlike, 1- Like, 9 - Abusive
    voted_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    voted_date_time = models.DateTimeField(auto_now_add=True)


class ArticleSectionComment(models.Model):
    section = models.ForeignKey(ArticleSection)
    title = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)  # Only approved comments are visible
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    commented_date_time = models.DateTimeField(auto_now_add=True)
