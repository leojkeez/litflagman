from django import template
from django.apps import apps
from django.utils.safestring import mark_safe
from django.utils.text import slugify
import re

register = template.Library()

@register.filter
def render_shortcodes(text):
    def replace_shortcode(match):
        shortcode_type = match.group(1).lower()
        identifier = match.group(2)

        if shortcode_type == 'slider':
            try:
                Slider = apps.get_model("Site", "Slider")
                instance = Slider.objects.get(id=identifier)
                from .slider_tags import render_slider
                return render_slider(instance)
            except (Slider.DoesNotExist, ValueError):
                return f"[Invalid slider ID: {identifier}]"
        elif shortcode_type in ['customtag', 'htmlsnippet']:
            try:
                HtmlSnippet = apps.get_model("Site", "HtmlSnippet")
                for snippet in HtmlSnippet.objects.all():
                    if slugify(snippet.name) == identifier:
                        return mark_safe(snippet.html_code)
                return f"[Invalid customtag name: {identifier}]"
            except LookupError:
                return f"[Invalid customtag name: {identifier}]"
        
        return f"[Unsupported shortcode type: {shortcode_type}]"

    return mark_safe(re.sub(r'\[\[(\w+):([\w-]+)\]\]', replace_shortcode, text))
