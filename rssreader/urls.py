from django.urls import path

from .views import (
    FeedlistTemplateView,
    HomeView,
    RssModelCreateView,
    SignUp,
    SiteListView,
    deletefunc,
    guest_login_func,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("guest/", guest_login_func, name="guest"),
    path("form/", RssModelCreateView.as_view(), name="form"),
    path("delete/", deletefunc, name="delete"),
    path("sitelist/", SiteListView.as_view(), name="sitelist"),
    path("feedlist/<int:pk>", FeedlistTemplateView.as_view(), name="feedlist"),
]
