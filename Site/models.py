from django.db import models
import datetime
import os
from django.utils import timezone
from django.conf import settings
from urllib.parse import urljoin
from unidecode import unidecode
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from pytils.translit import slugify as pytils_slugify
from ckeditor.fields import RichTextField

# Create your models here.

class Region(models.Model):
    title = models.CharField("Название региона", max_length=255, blank=True, null=True)
    region_description = RichTextField("Описание региона")
    most_reading_region = models.TextField("Самый читающий регион")
    laureates = models.TextField("Лауреаты", blank=True, null=True)  # Новое поле
    region_url = models.CharField(
        "Урл региона", 
        max_length=255, 
        blank=True, 
        help_text="Если оставить пустым, будет сформирован из тайтла"
    )
    seo_title = models.CharField("Тайтл СЕО", max_length=255)
    seo_description = models.TextField("Дескришен СЕО")
    right_column_text = models.TextField("Текстовое поле для вставки в любое место", blank=True, null=True)
    svg_id = models.CharField(
        "ID на карте (SVG ID)", 
        max_length=100, 
        blank=True, 
        null=True, 
        unique=True, 
        help_text="Идентификатор региона в SVG-карте (например, PETERSBURG, VORONEZH)"
    )
    is_active = models.BooleanField("Активна", default=True)
    coat_of_arms = models.ImageField("Герб", upload_to='regions/coats_of_arms/', blank=True, null=True)
    default_slider = models.ForeignKey(
        'Slider',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Дефолтный слайдер",
        related_name="default_for_regions"
    )
    main_photo = models.ImageField(
        "Главное фото региона",
        upload_to='regions/main_photos/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.title or ""

    def save(self, *args, **kwargs):
        # Если svg_id пустая строка, сохраняем как None для корректной работы unique=True
        if self.svg_id == '':
            self.svg_id = None

        # Если region_url пустой (был стерт или не заполнен)
        if not self.region_url:
            if self.title:
                # Используем pytils_slugify для поддержки русского языка
                slug = pytils_slugify(self.title)
                self.region_url = f"/region/{slug}/"
            else:
                self.region_url = "/region/untitled-region/"
                
        super().save(*args, **kwargs)


class Project(models.Model):
    YEAR_CHOICES = []
    for r in range(2000, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    project_description = RichTextField("Описание проекта")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион", related_name="projects")
    year = models.IntegerField("Год", choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    seo_title = models.CharField("Тайтл СЕО", max_length=255)
    seo_descriptor = models.TextField("Дескриптор СЕО")
    internal_tag = models.CharField("Тег для внутренней фильтрации в админке", max_length=255)
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.seo_title

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

class BookTerritory(models.Model):
    regions = models.ManyToManyField(Region, verbose_name="Регионы", blank=True, through='BookTerritoryRegion')
    text = RichTextField("Текстовое поле", blank=True, default="")
    seo_title = models.CharField("Тайтл СЕО", max_length=255, blank=True, default="")
    seo_description = models.TextField("Дескриптор СЕО", blank=True, default="")
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.seo_title or "Территория книги и чтения"

    class Meta:
        verbose_name = "Территория книги и чтения"
        verbose_name_plural = "Территория книги и чтения"

class BookTerritoryRegion(models.Model):
    book_territory = models.ForeignKey(BookTerritory, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Регион в территории книги"
        verbose_name_plural = "Регионы в территории книги"

class Club(models.Model):
    regions = models.ManyToManyField(Region, verbose_name="Регионы", blank=True, through='ClubRegion')
    text = RichTextField("Текстовое поле", blank=True, default="")
    seo_title = models.CharField("Тайтл СЕО", max_length=255, blank=True, default="")
    seo_description = models.TextField("Дескриптор СЕО", blank=True, default="")
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.seo_title or "Клуб первых"

    class Meta:
        verbose_name = "Клуб первых"
        verbose_name_plural = "Клубы первых"

class ClubRegion(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Регион в клубе"
        verbose_name_plural = "Регионы в клубе"

class Photo(models.Model):
    image = models.ImageField("Изображение", upload_to='photos/%Y/%m/%d/')
    title = models.CharField("Название", max_length=255)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return self.title


class Slider(models.Model):
    name = models.CharField("Название слайдера", max_length=255)
    # Используем строку 'Project' вместо прямого класса, чтобы избежать круговых импортов
    project = models.OneToOneField(
        'Project', 
        on_delete=models.CASCADE, 
        verbose_name="Проект", 
        null=True, 
        blank=True
    )
    photos = models.ManyToManyField(
        Photo, 
        through="SliderPhoto", 
        verbose_name="Фотографии"
    )
    internal_tag = models.CharField("Тег для внутренней фильтрации", max_length=255, blank=True)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдеры"

    def __str__(self):
        return self.name

    def get_tag_for_insertion(self):
        return f"[[slider:{self.pk}]]"
    get_tag_for_insertion.short_description = "Тег для вставки"

    def photo_count(self):
        return self.photos.count()
    photo_count.short_description = "Количество фото"


class SliderPhoto(models.Model):
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    order = models.PositiveIntegerField("Порядок")

    class Meta:
        ordering = ["order"]
        verbose_name = "Фото в слайдере"
        verbose_name_plural = "Фото в слайдерах"

class HtmlSnippet(models.Model):
    CATEGORY_CHOICES = [
        ('custom_tag', 'Кастомный тег'),
        ('festival', 'Фестиваль'),
        ('interview', 'Интервью'),
        ('intensive', 'Образовательный интенсив'),
    ]
    name = models.CharField("Название (для тега)", max_length=255, default="")
    title = models.CharField("Заголовок", max_length=255, blank=True, null=True)
    category = models.CharField("Категория", max_length=50, choices=CATEGORY_CHOICES, default='custom_tag')
    html_code = models.TextField("HTML код")
    internal_tag = models.CharField("Тег для внутренней фильтрации", max_length=255)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "HTML сниппет"
        verbose_name_plural = "HTML сниппеты"

    def __str__(self):
        return self.name

    def get_shortcode(self):
        return f"[[customtag:{slugify(self.name)}]]"
    get_shortcode.short_description = "Shortcode"


# Модель файла
class File(models.Model):
    ICON_CHOICES = [
        ("pdf.png", "PDF"),
        ("doc.png", "DOC"),
        ("xls.png", "Excel"),
        ("zip.png", "Архив"),
        ("img.png", "Изображение"),
        ("default.png", "По умолчанию"),
    ]
    title = models.CharField(max_length=300, verbose_name="Название файла", blank=True, null=True)
    file = models.FileField(upload_to='files/')
    icon = models.CharField(
        max_length=100,
        choices=ICON_CHOICES,
        default="default.png",
        verbose_name="Иконка"
    )
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="Дата загрузки")
    show_on_page = models.BooleanField(default=False, verbose_name="Выводить на странице файлов")

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.file.name

    def direct_url(self):
        return self.file.url  # автоматически отдаёт URL файла

    def icon_url(self):
        return urljoin(settings.STATIC_URL, f"file_icons/{self.icon}")

    def save(self, *args, **kwargs):
        # Сохраняем файл с транслитерацией имени
        if self.title:
            base_name = slugify(unidecode(self.title))
            extension = os.path.splitext(self.file.name)[1]
            new_filename = f"{base_name}{extension}"
            file_path = os.path.join("files", new_filename)

            # Проверка на уникальность
            counter = 1
            while File.objects.filter(file=file_path).exclude(pk=self.pk).exists():
                new_filename = f"{base_name}-{counter}{extension}"
                file_path = os.path.join("files", new_filename)
                counter += 1

            # Если файл уже сохранен и имя изменилось
            if self.pk and self.file.name != file_path:
                try:
                    old_path = self.file.path
                    new_path = os.path.join(settings.MEDIA_ROOT, file_path)

                    # Создаем папку, если она не существует
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)

                    # Проверяем, существует ли файл по новому пути
                    if not os.path.exists(new_path) and os.path.exists(old_path):
                        # Перемещаем файл
                        os.rename(old_path, new_path)
                        # Обновляем путь к файлу в модели
                        self.file.name = file_path
                except (ValueError, OSError):
                    # Если файл еще не существует на диске или возникла ошибка доступа
                    pass

        # Сохраняем объект
        super().save(*args, **kwargs)


class News(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'Новость'),
        ('most_reading_region', 'СЧР (самый читающий регион)'),
        ('forum-fest', 'Фестиваль форум'),
    ]

    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("ЧПУ (Slug)", max_length=255, blank=True, null=True, unique=True)
    short_description = models.TextField("Краткое описание", blank=True, null=True)
    seo_title = models.CharField("Тайтл СЕО", max_length=255)
    seo_descriptor = models.TextField("Дескриптор СЕО")
    full_text = RichTextField("Полный текст")
    category = models.CharField(
        "Тип",
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='news',
    )
    image_16x10 = models.ImageField("Картинка 16:10", upload_to='news/16x10/%Y/%m/%d/', blank=True, null=True)
    image_1x1 = models.ImageField("Картинка 1:1", upload_to='news/1x1/%Y/%m/%d/', blank=True, null=True)
    documents = models.ManyToManyField(File, verbose_name="Документы", blank=True)
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.title

    def get_previous(self):
        return News.objects.filter(is_active=True, created_at__lt=self.created_at).order_by('-created_at').first()

    def get_next(self):
        return News.objects.filter(is_active=True, created_at__gt=self.created_at).order_by('created_at').first()

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = pytils_slugify(self.title)[:240]
            if not slug_base:
                slug_base = "news"
            slug = slug_base
            counter = 1
            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{slug_base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]

class StaticPage(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    short_description = models.TextField("Краткое описание")
    full_text = RichTextField("Полный текст", blank=True, null=True)
    seo_title = models.CharField("Тайтл СЕО", max_length=255, blank=True, null=True)
    seo_descriptor = models.TextField("Дескриптор СЕО", blank=True, null=True)
    image_16x10 = models.ImageField("Картинка 16 к 10", upload_to='static_pages/16x10/%Y/%m/%d/', blank=True, null=True)
    image_1x1 = models.ImageField("Картинка 1 к 1", upload_to='static_pages/1x1/%Y/%m/%d/', blank=True, null=True)
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статическая страница"
        verbose_name_plural = "Статические страницы"

class Contest(models.Model):
    main_project = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Главный проект", related_name="contest_main_project")
    top = models.ManyToManyField(Region, verbose_name="Топ", related_name="contest_top")
    short_list = models.ManyToManyField(Region, verbose_name="Шорт лист", related_name="contest_short_list")
    year = models.IntegerField("Год", default=datetime.datetime.now().year)
    full_text = RichTextField("Полный текст", blank=True, null=True)
    seo_title = models.CharField("Тайтл СЕО", max_length=255)
    seo_descriptor = models.TextField("Дескриптор СЕО")

    def __str__(self):
        return f"{self.seo_title} ({self.year})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Если выбран главный проект (победитель), автоматически активируем регион
        if self.main_project:
            self.main_project.is_active = True
            self.main_project.save()

    class Meta:
        verbose_name = "Конкурс (итоги)"
        verbose_name_plural = "Конкурсы (итоги)"
        unique_together = ('main_project', 'year')
