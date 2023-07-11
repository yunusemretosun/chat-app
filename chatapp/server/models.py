from django.conf import settings
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Server(models.Model):
    name = models.TextField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")
    # categories have multple server and servers have one category
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="server_category")
    description = models.CharField(max_length=500, blank=True, null=True)
    # members have multiple server and servers have multiple member
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self) -> str:
        return f"{self.name} - {self.id}"


class Channel(models.Model):
    name = models.TextField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    server = models.ForeignKey(Server, on_delete=models.PROTECT, related_name="channel_server")
    topic = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
