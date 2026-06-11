from django import template
from django.apps import apps
from django.utils.safestring import mark_safe
from django.utils.text import slugify
import re

register = template.Library()

@register.filter(name='render_custom_tags')
def render_custom_tags(text):
    if not text:
        return ""
        
    def replace_shortcode(match):
        shortcode_type = match.group(1).lower()
        identifier = match.group(2)

        if shortcode_type in ['customtag', 'htmlsnippet']:
            try:
                HtmlSnippet = apps.get_model("Site", "HtmlSnippet")
                for snippet in HtmlSnippet.objects.filter(is_active=True):
                    if slugify(snippet.name) == identifier:
                        return mark_safe(snippet.html_code)
                return ""  # Если не найден, убираем шорткод из публичной части
            except LookupError:
                return ""
        
        # Если это не кастомный тег (например, слайдер), оставляем его как есть
        return match.group(0)

    return mark_safe(re.sub(r'\[\[(\w+):([\w-]+)\]\]', replace_shortcode, text))
