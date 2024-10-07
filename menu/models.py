from django.db import models
from django.urls import (reverse,
                         resolve,
                         NoReverseMatch)


class Menu(models.Model):
    """
    Menu - таблица со списком меню
    Атрибуты:
      title (str) - название меню
      url (str) - url меню
      named_url (str) - name url
    """
    title = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    named_url = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Убираем слэш по краям
        """
        if self.url:
            self.url = self.url.strip('/')
        if self.named_url:
            self.named_url = self.named_url.strip('/')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    """
    MenuItem - таблица со списком пунктов меню
    Атрибуты:
      title (str) - название пункта меню
      url (str) - url пункта меню
      named_url (str) - name url
      parent (int) - родительский пункт меню
      menu (int) - ссылка на связанное меню
    """
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True, null=True)
    named_url = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Убираем слэш по краям
        """
        if self.url:
            self.url = self.url.strip('/')
        if self.named_url:
            self.named_url = self.named_url.strip('/')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        """
        Получение актуального url
        """
        if not self.named_url or self.named_url and self.url:
            return self.url

        try:
            resolve(reverse(self.named_url))
            return reverse(self.named_url).lstrip('/')
        except NoReverseMatch:
            return reverse('tree_menu', kwargs={'item_url': self.named_url}).lstrip('/')
        except Exception:
            return self.named_url
