import re
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.db.models import Prefetch
from Site.models import Slider, SliderPhoto

register = template.Library()

# Регулярное выражение для поиска шорткодов [[slider:12]]
SLIDER_REGEX = re.compile(r'\[\[slider:(\d+)\]\]')


@register.filter(name='render_sliders')
def render_sliders(text):
    if not text:
        return ""

    # 1. Находим все ID слайдеров из текста (и убираем дубликаты через set)
    slider_ids = list(set(int(match) for match in SLIDER_REGEX.findall(text)))
    
    if not slider_ids:
        return mark_safe(text)  # Если слайдеров нет, просто возвращаем текст безопасным

    # 2. Оптимизированный запрос к БД: достаем только нужные активные слайдеры 
    # и сразу подгружаем их фотографии в правильном порядке за ОДИН проход.
    photo_prefetch = Prefetch(
        'sliderphoto_set',
        queryset=SliderPhoto.objects.select_related('photo').order_by('order'),
        to_attr='ordered_photos_list'  # Результат запишется в этот атрибут
    )
    
    sliders = Slider.objects.filter(
        id__in=slider_ids, 
        is_active=True
    ).prefetch_related(photo_prefetch)

    # 3. Рендерим HTML для каждого найденного слайдера через обычный Django-шаблон
    rendered_sliders = {}
    for slider in sliders:
        html = render_to_string('sliders/carousel.html', {
            'slider': slider,
            'ordered_photos': slider.ordered_photos_list
        })
        rendered_sliders[str(slider.id)] = html

    # 4. Функция автозамены шорткода на готовый HTML
    def replace_match(match):
        slider_id = match.group(1)
        # Если слайдер нашелся в БД, заменяем шорткод на его HTML. 
        # Если слайдера нет (например, удалили), шорткод просто исчезнет из текста.
        return rendered_sliders.get(slider_id, "")

    # Производим замену по всему тексту
    final_text = SLIDER_REGEX.sub(replace_match, text)
    
    return mark_safe(final_text)