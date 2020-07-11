from rest_framework import serializers
from .models import RssModel


class RssModelSeriializer(serializers.ModelSerializer):
    class Meta:
        model = RssModel
        fields = ("feed_title", "feed_url", "feed_user", "feed_update")
