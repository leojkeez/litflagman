from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Prefetch
import datetime
from .models import Photo, News, Region, Project, Contest, Slider, SliderPhoto, HtmlSnippet, Club, BookTerritory

def festival(request):
    snippets = HtmlSnippet.objects.filter(category='festival', is_active=True)[:3]
    news_items = News.objects.filter(category='forum-fest', is_active=True).order_by('-created_at')[:3]
    
    speakers = [
        {
            "name": "Ирина Хуснутдинова",
            "position": "Директор Благотворительного фонда «Счастливые истории»",
            "photo": "photo-ff/khusnutdinova.jpg"
        },
        {
            "name": "Мария Веденяпина",
            "position": "Директор Российской государственной детской библиотеки",
            "photo": "photo-ff/vedenyapina.jpg"
        },
        {
            "name": "Ольга Коле",
            "position": "Писатель, телеведущая",
            "photo": "photo-ff/kole.jpg"
        },
        {
            "name": "Илья Таранов",
            "position": "Член Союза писателей России, заместитель председателя Ульяновского регионального отделения Союза писателей России, исполнительный директор Ульяновского Фонда поддержки детского чтения",
            "photo": "photo-ff/taranov.jpg"
        },
        {
            "name": "Наталья Чупрова",
            "position": "Поэтесса и прозаик, автор Народного литературного объединения «Заполярье»",
            "photo": "photo-ff/chuprova.jpg"
        },
        {
            "name": "Ирина Селиверстова",
            "position": "прозаик, член Народного литературного объединения «Заполярье», художник-иллюстратор",
            "photo": "photo-ff/seliverstova.jpg"
        },
        {
            "name": "Евгений Шестов",
            "position": "член Союза детских и юношеских писателей РФ",
            "photo": "photo-ff/shestov.jpg"
        },
        {
            "name": "Ленар Шаех",
            "position": "главный редактор Татарского книжного издательства",
            "photo": "photo-ff/shayekh.jpg"
        },
        {
            "name": "Зиннур Мансуров",
            "position": "татарский поэт, журналист, публицист",
            "photo": "photo-ff/mansurov.jpg"
        },
        {
            "name": "Хабир Ибрагимов",
            "position": "татарский литератор, сценарист, драматург, публицист, переводчик",
            "photo": "photo-ff/ibragimov.jpg"
        },
        {
            "name": "Марсель Галиев",
            "position": "татарский прозаик, поэт, член Союза писателей Республики Татарстан",
            "photo": "photo-ff/galiev.jpg"
        },
        {
            "name": "Оксана Сусорова",
            "position": "финалист драматургических конкурсов «Крупица истории», «Время драмы» (г. Москва), шорт-листер конкурса издательства «Настя и Никита» (г. Москва)",
            "photo": "photo-ff/susorova.jpg"
        },
        {
            "name": "Александр Черников",
            "position": "Директор АНО «Сибирский институт развития креативных индустрий»",
            "photo": "photo-ff/chernikov.jpg"
        },
        {
            "name": "Денис Кравченко",
            "position": "Первый заместитель председателя комитета Государственной Думы Российской Федерации по экономической политике",
            "photo": "photo-ff/kravchenko.jpg"
        },
        {
            "name": "Владимир Григорьев",
            "position": "директор Департамента государственной поддержки периодической печати и книжной индустрии",
            "photo": "photo-ff/grigoriev.jpg"
        },
        {
            "name": "Сергей Степашин",
            "position": "Президент Российского книжного союза",
            "photo": "photo-ff/stepashin.jpg"
        },
        {
            "name": "Минтимер Шаймиев",
            "position": "Государственный советник Республики Татарстан, Посол Доброй воли ЮНЕСКО, Председатель Попечительского совета Республиканского Фонда «Возрождение»",
            "photo": "photo-ff/shaimiev.jpg"
        },
        {
            "name": "Ульяна Гаврицкая",
            "position": "бренд-директор книжной сети «Буквоед»",
            "photo": "photo-ff/gavritskaya.jpg"
        },
        {
            "name": "Алсу Абульханова",
            "position": "Заслуженная артистка республики Татарстан, телеведущая",
            "photo": "photo-ff/abulkhanova.jpg"
        },
        {
            "name": "Инна Касенова",
            "position": "Категорийный директор книжных департаментов сетей «Республика» (Россия, Москва) и «Меломан» (Республика Казахстан)",
            "photo": "photo-ff/kasenova.jpg"
        }
    ]

    venues = [
        {
            "name": "Казанское художественное училище имени Н.И. Фешина",
            "address": "ул. К. Маркса, 70, Казань",
            "photo": "photo-ff/place/feshina.jpg"
        },
        {
            "name": "Казанский приволжский федеральный университет",
            "address": "ул. Кремлёвская, 18, корп. 1, Казань",
            "photo": "photo-ff/place/kpfu.jpg"
        },
        {
            "name": "Филиал №27 МБУК «Централизованная библиотечная система г. Казани»",
            "address": "ул. Г. Баруди, 25, Казань",
            "photo": "photo-ff/place/filial_27.jpg"
        },
        {
            "name": "Книжный магазин «Читай-город», ТЦ Кольцо",
            "address": "ул. Петербургская, 1, Казань",
            "photo": "photo-ff/place/chitay_gorod_koltso.jpg"
        },
        {
            "name": "Филиал №26 МБУК «Централизованная библиотечная система г. Казани»",
            "address": "ул. Клары Цеткин, 11, Казань",
            "photo": "photo-ff/place/filial_26.jpg"
        },
        {
            "name": "ГБУК РТ «Республиканская юношеская библиотека»",
            "address": "пр. Ибрагимова, 53Б, Казань",
            "photo": "photo-ff/place/ryb.jpg"
        },
        {
            "name": "Литературное кафе в здании ТАТМЕДИА",
            "address": "ул. Декабристов, 2, Казань",
            "photo": "photo-ff/place/lit_cafe_tatmedia.jpg"
        },
        {
            "name": "Книжный магазин «Книга+», ТЦ Южный",
            "address": "пр. Победы, 91, Казань",
            "photo": "photo-ff/place/kniga_plus_yuzhny.jpg"
        },
        {
            "name": "Магазин «Татарского книжного издательства», ТЦ ГУМ",
            "address": "ул. Баумана, 51, Казань",
            "photo": "photo-ff/place/tat_kniga_gum.jpg"
        },
        {
            "name": "Дом татарской книги",
            "address": "ул. Островского, 15, Казань",
            "photo": "photo-ff/place/dom_tat_knigi.jpg"
        },
        {
            "name": "«Китап-club»",
            "address": "ул. Баумана, 19, Казань",
            "photo": "photo-ff/place/kitap_club.jpg"
        },
        {
            "name": "Детский оздоровительный лагерь «Молодежный»",
            "address": "Высокогорский район, Красносельское сельское поселение",
            "photo": "photo-ff/place/dol_molodezhny.jpg"
        },
        {
            "name": "«Республиканская детская библиотека им. Р. Миннуллина»",
            "address": "пр. Ямашева, 81, Казань",
            "photo": "photo-ff/place/rdb_minnullina.jpg"
        },
        {
            "name": "Филиал №13 МБУК «Централизованная библиотечная система г. Казани»",
            "address": "ул. Х. Мавлютова, 17Б, Казань",
            "photo": "photo-ff/place/filial_13.jpg"
        },
        {
            "name": "ГБУК РТ «Национальная библиотека Республики Татарстан»",
            "address": "ул. Пушкина, 86, Казань",
            "photo": "photo-ff/place/nl_rt.jpg"
        },
        {
            "name": "Культурный центр «Смена»",
            "address": "ул. Бурхана Шахиди, 7, Казань",
            "photo": "photo-ff/place/smena.jpg"
        },
        {
            "name": "Детский оздоровительный лагерь «Мирас-Наследие»",
            "address": "Зеленодольский район, Айшинское сельское поселение",
            "photo": "photo-ff/place/dol_miras.jpg"
        },
        {
            "name": "Книжный магазин «Читай-город», ТРЦ «Горки-Парк»",
            "address": "ул. Рихарда Зорге, 11Б, Казань",
            "photo": "photo-ff/place/chitay_gorod_gorki.jpg"
        },
        {
            "name": "Институт филологии и межкультурной коммуникации",
            "address": "ул. Татарстан, 2, Казань",
            "photo": "photo-ff/place/ifmk.jpg"
        },
        {
            "name": "Студия центрального эфира",
            "address": "Студия центрального эфира",
            "photo": "photo-ff/place/studio_central.jpg"
        }
    ]
    
    return render(request, 'festival.html', {
        'snippets': snippets,
        'news_items': news_items,
        'speakers': speakers,
        'venues': venues
    })

def fest_media(request):
    from django.core.paginator import Paginator
    
    # Исключаем 'custom_tag' (Кастомный тег) из выпадающего списка категорий
    categories = [cat for cat in HtmlSnippet.CATEGORY_CHOICES if cat[0] != 'custom_tag']
    selected_category = request.GET.get('category', '')
    
    # Исключаем 'custom_tag' из выборки сниппетов для этой страницы
    snippets_list = HtmlSnippet.objects.filter(is_active=True).exclude(category='custom_tag')
    if selected_category:
        snippets_list = snippets_list.filter(category=selected_category)
        
    snippets_list = snippets_list.order_by('-id')
    paginator = Paginator(snippets_list, 12)  # 12 сниппетов на страницу (4 строки по 3 сниппета)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'fest-media.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category
    })

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
    # Пытаемся найти регион по URL из БД с предзагрузкой дефолтного слайдера и его фото
    region_url = f"/region/{slug}/"
    region = get_object_or_404(
        Region.objects.select_related('default_slider').prefetch_related(
            Prefetch(
                'default_slider__sliderphoto_set',
                queryset=SliderPhoto.objects.select_related('photo').order_by('order'),
                to_attr='ordered_photos_list'
            )
        ),
        Q(region_url=region_url) | Q(region_url=f"/region/{slug}") | Q(region_url=slug)
    )
    
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
        
    # Логика навигации (предыдущий/следующий регион по алфавиту)
    all_regions = list(Region.objects.filter(is_active=True).only('id', 'title', 'region_url'))

    def get_sort_name(name):
        if not name: return ""
        if name.startswith("Республика "):
            return name[len("Республика "):]
        return name

    all_regions.sort(key=lambda x: get_sort_name(x.title))

    prev_region = None
    next_region = None

    for i, r in enumerate(all_regions):
        if r.pk == region.pk:
            if i > 0:
                prev_region = all_regions[i - 1]
                # Формируем корректный URL для навигации (абсолютный путь)
                p_url = (prev_region.region_url or "").strip('/')
                if p_url.startswith('region/'):
                    p_url = p_url[7:].strip('/')
                prev_region.nav_url = f"/region/{p_url}/"
            if i < len(all_regions) - 1:
                next_region = all_regions[i + 1]
                # Формируем корректный URL для навигации (абсолютный путь)
                n_url = (next_region.region_url or "").strip('/')
                if n_url.startswith('region/'):
                    n_url = n_url[7:].strip('/')
                next_region.nav_url = f"/region/{n_url}/"
            break

    return render(request, "region_detail.html", {
        'region': region,
        'years_data': years_data,
        'active_year': active_year,
        'prev_region': prev_region,
        'next_region': next_region,
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
        
        # Если слайдер для проекта текущего года отсутствует, пробуем использовать дефолтный слайдер региона
        if not winner_slider and winner_region.default_slider and winner_region.default_slider.is_active:
            winner_slider = winner_region.default_slider

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
    
    valid_categories = [code for code, name in News.CATEGORY_CHOICES]
    if category in valid_categories:
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


def club(request):
    club_instance = Club.objects.filter(is_active=True).prefetch_related(
        Prefetch('regions', queryset=Region.objects.filter(is_active=True).prefetch_related('contest_main_project'))
    ).first()
    
    # Получаем регионы для интерактивной карты (те, у которых заполнен svg_id)
    map_regions = Region.objects.filter(is_active=True, svg_id__isnull=False).exclude(svg_id="").prefetch_related('contest_main_project')
    
    return render(request, "club.html", {
        "club": club_instance,
        "map_regions": map_regions
    })


def book_territory(request):
    book_territory_instance = BookTerritory.objects.filter(is_active=True).prefetch_related(
        Prefetch('regions', queryset=Region.objects.filter(is_active=True).prefetch_related('contest_main_project'))
    ).first()
    
    return render(request, "book-territory.html", {
        "book_territory": book_territory_instance
    })
