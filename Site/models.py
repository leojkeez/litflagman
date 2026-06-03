from django.db import models
import datetime
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from pytils.translit import slugify as pytils_slugify # Импортируем слаггер для кириллицы
from ckeditor.fields import RichTextField # или откуда у вас RichTextField

# Create your models here.

class Region(models.Model):
    title = models.CharField("Название региона", max_length=255, blank=True, null=True)
    region_description = RichTextField("Описание региона")
    most_reading_region = models.TextField("Самый читающий регион")
    region_url = models.CharField(
        "Урл региона", 
        max_length=255, 
        blank=True, 
        help_text="Если оставить пустым, будет сформирован из тайтла"
    )
    seo_title = models.CharField("Тайтл СЕО", max_length=255)
    seo_description = models.TextField("Дескришен СЕО")
    right_column_text = models.TextField("Текстовое поле для вставки в любое место", blank=True, null=True)
    is_active = models.BooleanField("Активна", default=True)
    coat_of_arms = models.ImageField("Герб", upload_to='regions/coats_of_arms/', blank=True, null=True)

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.title or ""

    def save(self, *args, **kwargs):
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
    main_project = models.TextField("Главный проект")
    regions = models.ManyToManyField(Region, verbose_name="Регион", through='RegionBookTerritoryMembership')
    contest_description = RichTextField("Описание конкурса")
    seo_title = models.CharField("Тайтл СЕО", max_length=255)
    seo_descriptor = models.TextField("Дескриптор СЕО")
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.seo_title

    class Meta:
        verbose_name = "Территория книги"
        verbose_name_plural = "Территория книги"

class Club(models.Model):
    main_project = models.TextField("Главный проект")
    regions = models.ManyToManyField(Region, verbose_name="Регион", through='RegionClubMembership')
    contest_description = RichTextField("Описание конкурса")
    seo_title = models.CharField("Тайтл СЕО", max_length=255)
    seo_descriptor = models.TextField("Дескриптор СЕО")
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.seo_title

    class Meta:
        verbose_name = "Клуб первых"
        verbose_name_plural = "Клубы первых"

class RegionClubMembership(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    club = models.ForeignKey("Club", on_delete=models.CASCADE)
    year = models.IntegerField("Год", default=datetime.datetime.now().year)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        unique_together = (
            'region',
            'club',
            'year',
        )
        verbose_name = "Членство в клубе первых"
        verbose_name_plural = "Членства в клубах первых"

class RegionBookTerritoryMembership(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    book_territory = models.ForeignKey("BookTerritory", on_delete=models.CASCADE)
    year = models.IntegerField("Год", default=datetime.datetime.now().year)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Членство в территории книги"
        verbose_name_plural = "Членство в территориях книги"

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
    name = models.CharField("Название", max_length=255, default="")
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


class News(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'Новость'),
        ('most_reading_region', 'СЧР (самый читающий регион)'),
    ]

    title = models.CharField("Заголовок", max_length=255)
    short_description = models.TextField("Краткое описание")
    seo_title = models.CharField("Тайтл СЕО", max_length=255)
    seo_descriptor = models.TextField("Дескриптор СЕО")
    full_text = RichTextField("Полный текст")
    category = models.CharField(
        "Тип",
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='news',
    )
    image_16x10 = models.ImageField("Картинка 16:10", upload_to='news/16x10/%Y/%m/%d/')
    image_1x1 = models.ImageField("Картинка 1:1", upload_to='news/1x1/%Y/%m/%d/')
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.title

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

    class Meta:
        verbose_name = "Конкурс (итоги)"
        verbose_name_plural = "Конкурсы (итоги)"
        unique_together = ('main_project', 'year')
