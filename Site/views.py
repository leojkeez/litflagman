from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Photo

@staff_member_required
def multi_upload_photos(request):
    if request.method == "POST":
        for file in request.FILES.getlist("photos"):
            Photo.objects.create(title=file.name, image=file)
        return redirect("admin:Site_photo_changelist")
    return render(request, "admin/multi_upload_photos.html")
