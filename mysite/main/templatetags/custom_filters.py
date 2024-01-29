from django import template

register = template.Library()


@register.filter
def user_has_liked(likes_queryset, user):
    return likes_queryset.filter(user=user).exists()
