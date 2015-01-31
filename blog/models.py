from django.db import models
from social.apps.django_app.default.models import UserSocialAuth
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager
from django.conf import settings


class BaseArticle(models.Model):
    """
    Base model for all articles
    """
    slug = models.SlugField(max_length=150)
    title = models.CharField(max_length=150)
    image = ImageField(upload_to=settings.UPLOAD_TO, blank=True, null=True)
    author = models.ForeignKey(UserSocialAuth)
    published = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(UserSocialAuth)
    updated_date_time = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        abstract = True


class Article(BaseArticle):
    """
    Simple article which covers news/informational articles, with an image and one section
    """
    pass


class ArticleSection(models.Model):
    article = models.ForeignKey(Article)
    section_order = models.IntegerField(max_length=2)
    title = models.CharField(max_length=150)
    content = models.TextField()
    likes = models.IntegerField(max_length=4)
    unlikes = models.IntegerField(max_length=4)
    abusive = models.IntegerField(max_length=3)
    updated_by = models.ForeignKey(UserSocialAuth)
    updated_date_time = models.DateTimeField(auto_now=True)


class ArticleSectionReference(models.Model):
    pass


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


