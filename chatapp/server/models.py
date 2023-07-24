from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .validators import validate_icon_image_size, validate_image_file_extension


def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icon/{filename}"


def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_icon/{filename}"


def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"


# Create your models here.
class Category(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon_upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        # veritabanina kayitlimi?
        if self.id:
            # kayitli ornegi getir
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                # objeyi update ettigimiz icon ile eski icon farkliysa eski iconu sil
                # (bu islem yalnizca filefieldveimagefieldlardacalisir)
                existing.icon.delete(save=False)
        # models.Model ust sinifinin save metodunu kullanarak yeni dosyayi veritabanina kaydet.
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

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
    banner = models.ImageField(
        upload_to=server_banner_upload_path,
        null=True,
        blank=True,
        validators=[validate_image_file_extension],
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

    def save(self, *args, **kwargs):
        # veritabanina kayitlimi?
        if self.id:
            # kayitli ornegi getir
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                # objeyi update ettigimiz icon ile eski icon farkliysa eski iconu sil
                # (bu islem yalnizca filefieldveimagefieldlardacalisir)
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        # models.Model ust sinifinin save metodunu kullanarak yeni dosyayi veritabanina kaydet.
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Server")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self) -> str:
        return self.name
