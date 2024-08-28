from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.show_entry_page, name="show_entry_page"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
]
