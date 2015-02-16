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