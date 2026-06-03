from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("jet/", include("jet.urls", "jet")),  # Django JET URLS
    path("admin/", admin.site.urls),
    path("ckeditor/upload/", include("ckeditor_uploader.urls")),
    path("", include("Site.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
