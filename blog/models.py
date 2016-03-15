from django.db import models
from django.utils import timezone


# Create your models here.
# This holds the list of information about the user, so people who publish to the
# website can be tracked.
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default = timezone.now)
    published_date= models.DateTimeField(
        blank = True, null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
