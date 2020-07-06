import feedparser
from django import forms
from django.forms import ModelForm

from .models import RssModel


class RssModelForm(ModelForm):
    class Meta:
        model = RssModel
        fields = ("feed_url",)

    def clean_feed_url(self):
        feed_url = self.cleaned_data["feed_url"]
        feeder = feedparser.parse(feed_url).bozo
        if feeder != 0:
            raise forms.ValidationError("無効なURLです。")
        return feed_url

    def __init__(self, *args, **kwargs):
        super(RssModelForm, self).__init__(*args, **kwargs)
        self.instance.unique_error_message = lambda m, u: u"このURLはすでに追加されています。"
