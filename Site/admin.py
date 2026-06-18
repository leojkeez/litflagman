from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . import views
from django.urls import path
from .models import Region, Project, BookTerritory, Club, Photo, Slider, HtmlSnippet, SliderPhoto, News, StaticPage, Contest, File
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe
import os
import re
from django import forms
from django.conf import settings


def get_svg_ids_from_map():
    """
    Динамически парсит файл шаблона карты Site/templates/includes/map.html
    и возвращает список всех существующих на карте идентификаторов регионов (SVG ID)
    для отображения в выпадающем списке админки.
    """
    defaults = [
        ('PETERSBURG', 'Санкт-Петербург'),
        ('ARHANGELSKAYA_OBLAST', 'Архангельская область'),
        ('BELGOROD', 'Белгородская область'),
        ('VORONEZH', 'Воронежская область'),
        ('ULYANOVSK', 'Ульяновская область'),
        ('NOVOSIBIRSKAYA_OBLAST', 'Новосибирская область'),
        ('IRKUTSK', 'Иркутская область'),
        ('TATARSTAN', 'Республика Татарстан'),
        ('YAKUTIYA', 'Республика Саха (Якутия)'),
        ('RESPUBLIKA_BASHKORTOSTAN', 'Республика Башкортостан'),
        ('KURSKAYA_OBLAST', 'Курская область'),
    ]
    
    map_path = os.path.join(settings.BASE_DIR, 'Site', 'templates', 'includes', 'map.html')
    if not os.path.exists(map_path):
        map_path = os.path.join(settings.BASE_DIR, 'templates', 'includes', 'map.html')
        
    if not os.path.exists(map_path):
        return defaults

    try:
        with open(map_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ищем id всех элементов с классом js-history-competition-region
        pattern = r'class="[^"]*js-history-competition-region[^"]*"\s+id="([^"]+)"'
        matches = re.findall(pattern, content)
        
        pattern_reverse = r'id="([^"]+)"\s+class="[^"]*js-history-competition-region[^"]*"'
        matches += re.findall(pattern_reverse, content)
        
        if not matches:
            return defaults
            
        region_names_mapping = {
            'PETERSBURG': 'Санкт-Петербург',
            'ARHANGELSKAYA_OBLAST': 'Архангельская область',
            'BELGOROD': 'Белгородская область',
            'VORONEZH': 'Воронежская область',
            'ULYANOVSK': 'Ульяновская область',
            'NOVOSIBIRSKAYA_OBLAST': 'Новосибирская область',
            'IRKUTSK': 'Иркутская область',
            'TATARSTAN': 'Республика Татарстан',
            'YAKUTIYA': 'Республика Саха (Якутия)',
            'RESPUBLIKA_BASHKORTOSTAN': 'Республика Башкортостан',
            'KURSKAYA_OBLAST': 'Курская область'
        }
        
        choices = [('', '--- Выберите регион на карте ---')]
        for svg_id in sorted(list(set(matches))):
            display_name = region_names_mapping.get(svg_id)
            if not display_name:
                # Автоматически форматируем красивое имя по умолчанию, если оно не найдено в маппинге
                display_name = svg_id.replace('_', ' ').title()
            choices.append((svg_id, display_name))
            
        return choices
    except Exception:
        return defaults


# Register your models here.
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"region_url": ("title",)}
    list_display = ("title", "svg_id", "is_active",)
    search_fields = ("title", "svg_id",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        Переопределяем форму редактирования в админке:
        Делаем текстовое поле svg_id выпадающим списком с динамически
        вычисляемыми вариантами из файла карты templates/includes/map.html
        """
        if db_field.name == 'svg_id':
            choices = get_svg_ids_from_map()
            return forms.ChoiceField(
                choices=choices,
                required=False,
                label=db_field.verbose_name,
                help_text=db_field.help_text
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("region", "year", "is_active")
    search_fields = ("region__title", "year",)

@admin.register(BookTerritory)
class BookTerritoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('regions',)
    list_display = ('seo_title', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('regions', 'text', 'is_active')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'seo_description'),
        }),
    )

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    filter_horizontal = ('regions',)
    list_display = ('seo_title', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('regions', 'text', 'is_active')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'seo_description'),
        }),
    )

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    filter_horizontal = ('top', 'short_list')
    fieldsets = (
        (None, {
            'fields': ('main_project', 'year', 'top', 'short_list', 'full_text')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'seo_descriptor'),
        }),
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "image")
    list_per_page = 20
    change_list_template = "admin/photo_change_list.html"

    # Добавляем строку поиска. Поиск будет идти по названию фотографии.
    search_fields = ("title",) 

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("multi_upload/", self.admin_site.admin_view(views.multi_upload_photos), name="multi_upload_photos"),
        ]
        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["multi_upload_url"] = reverse("admin:multi_upload_photos")
        return super().changelist_view(request, extra_context)



@admin.register(HtmlSnippet)
class HtmlSnippetAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "category", "get_shortcode", "internal_tag", "is_active")
    list_filter = ("category", "is_active")
    readonly_fields = ("get_shortcode",)


# СЛАЙДЕР
class SliderPhotoInline(admin.TabularInline):
    model = SliderPhoto
    extra = 1

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    # Поля, которые отображаются в списке всех слайдеров
    list_display = ('name', 'project', 'photo_count', 'get_tag_for_insertion', 'is_active')
    
    # Делаем наши кастомные поля доступными для просмотра на странице редактирования
    readonly_fields = ('get_tag_for_insertion', 'get_generated_html')
    
    inlines = [SliderPhotoInline]

    # Красиво группируем поля на странице редактирования слайдера
    fieldsets = (
        ("Основная информация", {
            'fields': ('name', 'project', 'internal_tag', 'is_active')
        }),
        ("Код и интеграция", {
            # Выводим шорткод и сгенерированный HTML рядом
            'fields': ('get_tag_for_insertion', 'get_generated_html'),
        }),
    )

    def get_generated_html(self, obj):
        """
        Генерирует итоговый HTML-код карусели на основе шаблона
        и выводит его в админке как отформатированный текст.
        """
        if not obj.pk:
            return "Сохраните слайдер, чтобы сгенерировать HTML-код."

        # 1. Получаем связанные фотографии слайдера в правильном порядке
        ordered_photos = obj.sliderphoto_set.select_related('photo').order_by('order')

        # 2. Рендерим шаблон слайдера в строку (используем тот же шаблон, что и на сайте)
        html_content = render_to_string('sliders/carousel.html', {
            'slider': obj,
            'ordered_photos': ordered_photos
        })

        # 3. Экранируем спецсимволы (<, >, &), чтобы код отображался именно текстом,
        # а не рендерился браузером как рабочая карусель внутри админки.
        escaped_html = escape(html_content.strip())

        # 4. Возвращаем стилизованный блок кода с темной темой (как в редакторах кода)
        return mark_safe(
            f'<pre style="'
            f'background: #272822; '         # Темный фон (Monokai)
            f'color: #f8f8f2; '              # Светлый текст
            f'padding: 15px; '
            f'border-radius: 6px; '
            f'max-height: 350px; '           # Ограничиваем по высоте
            f'overflow-y: auto; '            # Добавляем прокрутку, если кода много
            f'font-family: Consolas, Monaco, monospace; '
            f'font-size: 13px; '
            f'line-height: 1.5; '
            f'margin: 0;'
            f'"><code>{escaped_html}</code></pre>'
        )
    
    # Название колонки/поля в админке
    get_generated_html.short_description = "Итоговый сгенерированный HTML-код"


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'icon', 'uploaded_at', 'show_on_page')
    list_filter = ('icon', 'show_on_page', 'uploaded_at')
    search_fields = ('title', 'file')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('title', 'short_description', 'full_text')
    readonly_fields = ('updated_at',)
    filter_horizontal = ('documents',)
    fieldsets = (
        (None, {
            'fields': ('title', 'short_description', 'full_text', 'category', 'is_active', 'created_at', 'updated_at'),
        }),
        ('Документы', {
            'fields': ('documents',),
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_descriptor'),
        }),
        ('Изображения', {
            'fields': ('image_16x10', 'image_1x1'),
        }),
    )

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('title', 'short_description', 'full_text', 'is_active'),
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'seo_descriptor'),
        }),
        ('Изображения', {
            'classes': ('collapse',),
            'fields': ('image_16x10', 'image_1x1'),
        }),
    )
