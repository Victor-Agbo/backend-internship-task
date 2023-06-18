from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_entry", views.add_entry.as_view(), name="add_entry"),
    path("load_entries", views.load_entries.as_view(), name="load_entries"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("set_calories", views.set_calories.as_view(), name="set_calories"),
]
