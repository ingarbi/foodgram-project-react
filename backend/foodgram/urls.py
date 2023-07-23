from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("recipes.urls", namespace='recipes')),
    path("api/", include("users.urls", namespace='users')),
]
