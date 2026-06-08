from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Prefetch
import datetime
from .models import Photo, News, Region, Project, Contest, Slider, SliderPhoto

def index(request):
    latest_news = News.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    # Получаем все активные регионы из базы данных
    db_regions = {r.title: r.region_url for r in Region.objects.filter(is_active=True)}
    
    # Полный эталонный список 89 регионов РФ
    master_regions_list = [
        "Республика Адыгея", "Республика Алтай", "Республика Башкортостан", "Республика Бурятия",
        "Республика Дагестан", "Республика Ингушетия", "Кабардино-Балкарская Республика",
        "Республика Калмыкия", "Карачаево-Черкесская Республика", "Республика Карелия",
        "Республика Коми", "Республика Крым", "Республика Марий Эл", "Республика Мордовия",
        "Республика Саха (Якутия)", "Республика Северная Осетия — Алания", "Республика Татарстан",
        "Республика Тыва", "Удмуртская Республика", "Республика Хакасия", "Чеченская Республика",
        "Чувашская Республика", "Алтайский край", "Забайкальский край", "Камчатский край",
        "Краснодарский край", "Красноярский край", "Пермский край", "Приморский край",
        "Ставропольский край", "Хабаровский край", "Амурская область", "Архангельская область",
        "Астраханская область", "Белгородская область", "Брянская область", "Владимирская область",
        "Волгоградская область", "Вологодская область", "Воронежская область", "Ивановская область",
        "Иркутская область", "Калининградская область", "Калужская область", "Кемеровская область",
        "Кировская область", "Костромская область", "Курганская область", "Курская область",
        "Ленинградская область", "Липецкая область", "Магаданская область", "Московская область",
        "Мурманская область", "Нижегородская область", "Новгородская область", "Новосибирская область",
        "Омская область", "Оренбургская область", "Орловская область", "Пензенская область",
        "Псковская область", "Ростовская область", "Рязанская область", "Самарская область",
        "Саратовская область", "Сахалинская область", "Свердловская область", "Смоленская область",
        "Тамбовская область", "Тверская область", "Томская область", "Тульская область",
        "Тюменская область", "Ульяновская область", "Челябинская область", "Ярославская область",
        "Москва", "Санкт-Петербург", "Севастополь", "Еврейская автономная область",
        "Ненецкий автономный округ", "Ханты-Мансийский автономный округ — Югра",
        "Чукотский автономный округ", "Ямало-Ненецкий автономный округ",
        "Донецкая Народная Республика", "Луганская Народная Республика",
        "Запорожская область", "Херсонская область"
    ]
    
    # Формируем финальный список объектов для шаблона
    regions_data = []
    for name in master_regions_list:
        regions_data.append({
            'name': name,
            'url': db_regions.get(name) # Если регион есть в БД, тут будет ссылка, иначе None
        })

    # Разбиваем список на 6 колонок
    import math
    cols_count = 6
    rows_per_col = math.ceil(len(regions_data) / cols_count)
    region_columns = [regions_data[i:i + rows_per_col] for i in range(0, len(regions_data), rows_per_col)]

    return render(request, "index.html", {
        'latest_news': latest_news,
        'region_columns': region_columns
    })

@staff_member_required
def multi_upload_photos(request):
    if request.method == "POST":
        for file in request.FILES.getlist("photos"):
            Photo.objects.create(title=file.name, image=file)
        return redirect("admin:Site_photo_changelist")
    return render(request, "admin/multi_upload_photos.html")


def region_detail(request, slug):
    # Пытаемся найти регион по URL из БД
    region_url = f"/region/{slug}/"
    region = get_object_or_404(Region, Q(region_url=region_url) | Q(region_url=f"/region/{slug}") | Q(region_url=slug))
    
    # Года от 2015 до 2028 включительно
    start_year = 2015
    end_year = 2028
    
    # 1. Получаем года, когда регион был победителем
    contests_winner = {c.year: True for c in Contest.objects.filter(main_project=region, year__gte=start_year, year__lte=end_year)}
    
    # 2. Получаем года, когда регион был лауреатом (в шорт-листе или в топе)
    contests_other = Contest.objects.filter(
        Q(short_list=region) | Q(top=region),
        year__gte=start_year,
        year__lte=end_year
    ).values_list('year', flat=True)
    contests_laureate = {y: True for y in contests_other}
    
    # 3. Загружаем проекты региона за эти годы со связанными слайдерами и фото
    photo_prefetch = Prefetch(
        'sliderphoto_set',
        queryset=SliderPhoto.objects.select_related('photo').order_by('order'),
        to_attr='ordered_photos_list'
    )
    
    slider_prefetch = Prefetch(
        'slider',
        queryset=Slider.objects.filter(is_active=True).prefetch_related(photo_prefetch)
    )
    
    projects_qs = Project.objects.filter(
        region=region,
        is_active=True,
        year__gte=start_year,
        year__lte=end_year
    ).prefetch_related(slider_prefetch)
    
    projects_by_year = {p.year: p for p in projects_qs}
    
    # Ищем дефолтный (активный) год: последний проект или последний год (2028)
    active_year = datetime.datetime.now().year
    if active_year < start_year or active_year > end_year:
        active_year = end_year
        
    # Если за текущий год проекта нет, возьмем последний доступный год с проектом
    if active_year not in projects_by_year and projects_by_year:
        active_year = max(projects_by_year.keys())
    
    years_data = []
    for year in range(start_year, end_year + 1):
        is_winner = contests_winner.get(year, False)
        is_laureate = contests_laureate.get(year, False)
        
        status = 'none'
        if is_winner:
            status = 'winner'
        elif is_laureate:
            status = 'laureate'
            
        project = projects_by_year.get(year, None)
        
        years_data.append({
            'year': year,
            'status': status,
            'project': project,
            'has_project': project is not None
        })
        
    return render(request, "region_detail.html", {
        'region': region,
        'years_data': years_data,
        'active_year': active_year,
    })

