# posts/templatetags/post_tags.py
from django import template
from ..models import Like

register = template.Library()

@register.simple_tag
def user_has_liked(post, user):
    if not user.is_authenticated:
        return False
    return post.likes.filter(user=user).exists()