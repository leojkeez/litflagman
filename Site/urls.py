from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/multi_upload_photos/", views.multi_upload_photos, name="multi_upload_photos"),
    path("region/<slug:slug>/", views.region_detail, name="region_detail"),
    path("<int:year>-contest/", views.contest_detail, name="contest_detail"),
    path("contest/", views.contest_detail_default, name="contest_detail_default"),
    path("news/", views.news_list, name="news_list"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("festival/", views.festival, name="festival"),
    path("festival/media/", views.fest_media, name="fest_media"),
    path("club/", views.club, name="club"),
    path("book-territory/", views.book_territory, name="book_territory"),
]
