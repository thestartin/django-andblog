from django.core.paginator import Page, Paginator
from django.conf import settings


class BlogPage(Page):

    def get_previous_numbers(self):
        """
        Method to get previous numbers based on number defined in the settings file PAGE_PREVIOUS_ITEMS
        Like say current page is 3, and if PAGE_PREVIOUS_ITEMS is 3 then 1,2 will be returned.
        :return:
        """
        endrange = self.number - settings.PAGE_PREVIOUS_ITEMS
        if endrange < 1:
            endrange = 1

        self.pre_ellips = endrange - 1 > 1

        if endrange == self.number:
            endrange += 1

        return range(endrange, self.number)

    def get_next_numbers(self):
        """
        Method to get next page numbers based on number defined in the settings file PAGE_PREVIOUS_ITEMS
        Like say current page is 3, and if PAGE_NEXT_ITEMS is 3 then 1,2 will be returned.
        :return:
        """
        endrange = self.number + settings.PAGE_NEXT_ITEMS
        if endrange > self.paginator.num_pages:
            endrange = self.paginator.num_pages

        self.next_ellips = self.paginator.num_pages - endrange > 1

        return range(self.number+1, endrange+1)


class BlogPaginator(Paginator):
    def _get_page(self, *args, **kwargs):
        """
        Returns an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return BlogPage(*args, **kwargs)


def get_custom_fields(fields, request):
    """
    Method to get Custom Fields that was added from the Client
    Custom fields will be added with an <field_name>_<section_id>
    :return:
    """
    custom_fields = []
    for key, value in request.POST.iteritems():
        keys = key.split('_')
        if keys[0] in fields:
            section_id = int(keys[-1]) if len(keys) > 1 else 1
            if section_id > 1:
                custom_fields.append((key, fields[keys[0]]))

    return custom_fields


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip