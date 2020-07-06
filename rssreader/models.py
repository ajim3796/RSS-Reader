from django.db import models


class RssModel(models.Model):
    feed_title = models.TextField()
    feed_url = models.URLField(unique=True)
    feed_user = models.CharField(max_length=50)
    feed_update = models.DateTimeField(null=True)

    def __str__(self):
        return self.feed_title
