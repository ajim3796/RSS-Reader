from datetime import datetime

import feedparser
import pytz
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import RssModelForm
from .models import RssModel


class HomeView(TemplateView):
    template_name = "rssreader/home.html"


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "rssreader/signup.html"


class RssModelCreateView(LoginRequiredMixin, CreateView):
    model = RssModel
    template_name = "rssreader/form.html"
    form_class = RssModelForm
    success_url = reverse_lazy("sitelist")

    def form_valid(self, form):
        feeder = feedparser.parse(form.instance.feed_url)
        form.instance.feed_title = feeder.feed.title
        form.instance.feed_user = self.request.user
        return super().form_valid(form)


class SiteListView(LoginRequiredMixin, ListView):
    model = RssModel
    template_name = "rssreader/sitelist.html"

    def get_context_data(self, **kwargs):
        context = super(SiteListView, self).get_context_data(**kwargs)

        feeds = RssModel.objects.all()
        UTC = pytz.timezone("UTC")
        JST = pytz.timezone("Asia/Tokyo")
        for feed in feeds:
            feeder = feedparser.parse(feed.feed_url)
            date = {
                entry.updated_parsed or entry.published_parsed
                for entry in feeder.entries
            }
            latest = max(date)
            feed.feed_update = datetime(*latest[:6], tzinfo=UTC).astimezone(JST)
            feed.save()
        sorted_rssmodel = feeds.order_by("feed_update").reverse()

        context = {
            "sorted_rssmodel": sorted_rssmodel,
        }

        return context


class FeedlistTemplateView(TemplateView):
    model = RssModel
    template_name = "rssreader/feedlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        feed = RssModel.objects.get(pk=self.kwargs["pk"])
        url = feed.feed_url
        feeder = feedparser.parse(url)
        UTC = pytz.timezone("UTC")
        JST = pytz.timezone("Asia/Tokyo")
        feed_list = []
        for entry in feeder.entries:
            update = datetime(
                *(entry.updated_parsed or entry.published_parsed)[:6], tzinfo=UTC
            ).astimezone(JST)
            feed_list.append((entry, update))

        context = {"feed_title": feeder.feed.title, "feed_list": feed_list}

        return context


def deletefunc(request):
    delete_ids = request.POST.getlist("delete_ids")
    if delete_ids:
        for delete_id in delete_ids:
            RssModel.objects.filter(id__in=delete_ids).delete()
        return redirect("sitelist")


def guest_login_func(request):
    guest_user = User.objects.get(username="guest")
    login(request, guest_user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect("sitelist")
