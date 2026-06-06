from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/multi_upload_photos/", views.multi_upload_photos, name="multi_upload_photos"),
]
