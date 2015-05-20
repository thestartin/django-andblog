from django.http import JsonResponse
from django.db.models import Q

__all__ = ['JSONResponseMixin', 'ArticleFilterMixin', 'ArticleSectionMixin']


class JSONResponseMixin(object):
    failure_message = {'status': 'N', 'message': 'Unable to process request', 'data': ''}
    success_message = {'status': 'Y', 'message': 'Successfully processed request', 'data': ''}

    def render_to_json_response(self, context, **response_kwargs):

        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        return context


class ArticleFilterMixin(object):
    def get_posts(self, route='all', prefetch=True, **kwargs):
        if route == 'tag':
            queryset = self.get_posts_by_tag(kwargs['tag'])
        elif route in ('year', 'year_month', 'ymd'):
            queryset = self.get_posts_by_date(route, **kwargs)
        else:
            queryset = self.get_queryset()

        if prefetch:
            return queryset.prefetch_related('articlesection_set').select_related('author')
        else:
            return queryset

    def get_unpublished_posts_by_user(self, route, user, **kwargs):
        """
        This method is used to get posts for a specified user who has create permissions & even if
        the article is not published
        :return:
        """
        queryset = self.get_posts(route, prefetch=False, **kwargs)
        queryset = queryset.filter(Q(author=user) | Q(published=True))

        return queryset.prefetch_related('articlesection_set').select_related('author')

    def get_posts_by_tag(self, tag_name):
        return self.get_queryset().filter(tags__name=tag_name)

    def get_posts_by_date(self, route, **kwargs):
        queryset = self.get_queryset()
        if route == 'year' or route == 'year_month' or route == 'ymd':
            queryset = queryset.filter(created_date_time__year=kwargs['year'])

        if route == 'year_month':
            queryset = queryset.filter(created_date_time__month=kwargs['month'])

        if route == 'ymd':
            queryset = queryset.filter(created_date_time__day=kwargs['day'])

        return queryset


class ArticleSectionMixin(object):

    def vote(self, form_data, who, user):
        # Import here to avoid circular dependency issues
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
            return True, getattr(article_section, attr, 0)
        else:
            return False, 0
