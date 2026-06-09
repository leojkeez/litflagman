from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Prefetch
import datetime
from .models import Photo, News, Region, Project, Contest, Slider, SliderPhoto

def partition_regions_by_letters(groups, k=6):
    n = len(groups)
    if n <= k:
        cols = [[g] for g in groups]
        while len(cols) < k:
            cols.append([])
        return cols
        
    weights = [len(g[1]) + 2 for g in groups]
    
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    parent = [[0] * (k + 1) for _ in range(n + 1)]
    
    dp[0][0] = 0
    
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i+1] = pref[i] + weights[i]
        
    for j in range(1, k + 1):
        for i in range(1, n + 1):
            for p in range(i):
                cost = max(dp[p][j-1], pref[i] - pref[p])
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    parent[i][j] = p
                    
    cols = []
    curr_i = n
    for curr_j in range(k, 0, -1):
        p = parent[curr_i][curr_j]
        cols.append(groups[p:curr_i])
        curr_i = p
    cols.reverse()
    return cols

def index(request):
    latest_news = News.objects.filter(is_active=True, category='most_reading_region').order_by('-created_at')[:3]
    
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
        if name.startswith("Республика "):
            sort_name = name[len("Республика "):]
        else:
            sort_name = name
            
        letter = sort_name[0].upper() if sort_name else ""
        
        regions_data.append({
            'name': name,
            'url': db_regions.get(name), # Если регион есть в БД, тут будет ссылка, иначе None
            'sort_name': sort_name,
            'letter': letter
        })

    # Сортируем по значению sort_name
    regions_data.sort(key=lambda x: x['sort_name'])

    # Группируем по буквам
    from collections import defaultdict
    grouped = defaultdict(list)
    for r in regions_data:
        grouped[r['letter']].append(r)

    grouped_list = sorted(grouped.items())

    # Разбиваем список на 6 колонок
    region_columns = partition_regions_by_letters(grouped_list, k=6)

    # Получаем все активные регионы с заполненным svg_id для интерактивной карты
    map_regions = Region.objects.filter(is_active=True, svg_id__isnull=False).exclude(svg_id="").prefetch_related('contest_main_project')

    return render(request, "index.html", {
        'latest_news': latest_news,
        'region_columns': region_columns,
        'map_regions': map_regions
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
    contests_winner = set(Contest.objects.filter(main_project=region, year__gte=start_year, year__lte=end_year).values_list('year', flat=True))
    
    # 2. Получаем года, когда регион был в топе (лауреаты)
    contests_top = set(Contest.objects.filter(top=region, year__gte=start_year, year__lte=end_year).values_list('year', flat=True))
    
    # 3. Получаем года, когда регион был в шорт-листе
    contests_short_list = set(Contest.objects.filter(short_list=region, year__gte=start_year, year__lte=end_year).values_list('year', flat=True))
    
    # Объединенный сет для лауреатов (топ + шорт-лист) для обратной совместимости статуса
    contests_laureate_years = contests_top | contests_short_list
    
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
        is_winner = year in contests_winner
        is_top = year in contests_top
        is_short_list = year in contests_short_list
        
        status = 'none'
        if is_winner:
            status = 'winner'
        elif is_top or is_short_list:
            status = 'laureate'
            
        project = projects_by_year.get(year, None)
        
        years_data.append({
            'year': year,
            'status': status,
            'is_winner': is_winner,
            'is_top': is_top,
            'project': project,
            'has_project': project is not None
        })
        
    return render(request, "region_detail.html", {
        'region': region,
        'years_data': years_data,
        'active_year': active_year,
    })


def contest_detail(request, year=None):
    if year is None:
        last_contest = Contest.objects.order_by('-year').first()
        if last_contest:
            year = last_contest.year
        else:
            year = datetime.datetime.now().year
    
    # Ограничим диапазон согласно требованиям от 2015 до 2028
    if year < 2015 or year > 2028:
        year = 2025 # Дефолт, если передан некорректный год
        
    contest = get_object_or_404(Contest, year=year)
    years = list(range(2015, 2029))

    winner_region = contest.main_project
    winner_project = None
    winner_slider = None
    winner_photos = []
    
    if winner_region:
        winner_project = Project.objects.filter(region=winner_region, year=year, is_active=True).first()
        if winner_project:
            winner_slider = Slider.objects.filter(project=winner_project, is_active=True).first()
            if winner_slider:
                winner_photos = SliderPhoto.objects.filter(slider=winner_slider).select_related('photo').order_by('order')

    # Лауреаты конкурса - это contest.top
    laureates = contest.top.filter(is_active=True)
    laureates_data = []
    for r in laureates:
        proj = Project.objects.filter(region=r, year=year, is_active=True).first()
        laureates_data.append({
            'region': r,
            'project': proj
        })

    # Короткий список - это contest.short_list
    short_list_regions = contest.short_list.filter(is_active=True).order_by('title')
    short_list_data = []
    for r in short_list_regions:
        proj = Project.objects.filter(region=r, year=year, is_active=True).first()
        short_list_data.append({
            'region': r,
            'project': proj
        })

    context = {
        'contest': contest,
        'year': year,
        'years': years,
        'winner_region': winner_region,
        'winner_project': winner_project,
        'winner_slider': winner_slider,
        'winner_photos': winner_photos,
        'laureates_data': laureates_data,
        'short_list_data': short_list_data,
    }
    return render(request, "contest_detail.html", context)


from django.core.paginator import Paginator

def contest_detail_default(request):
    last_contest = Contest.objects.order_by('-year').first()
    if last_contest:
        year = last_contest.year
    else:
        year = datetime.datetime.now().year
        
    if year < 2015 or year > 2028:
        year = 2025
        
    return redirect('contest_detail', year=year)


def news_list(request):
    category = request.GET.get('category')
    news_qs = News.objects.filter(is_active=True)
    
    if category in ['news', 'most_reading_region']:
        news_qs = news_qs.filter(category=category)
        
    news_qs = news_qs.order_by('-created_at')
    
    paginator = Paginator(news_qs, 12)  # 12 новостей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "news_list.html", {
        "page_obj": page_obj,
        "selected_category": category or "",
        "categories": News.CATEGORY_CHOICES
    })


def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug, is_active=True)
    return render(request, "news_detail.html", {"news": news_item})
