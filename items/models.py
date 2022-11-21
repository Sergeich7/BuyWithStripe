from django.urls import reverse
from django.db import models


class СurrencyUSDRate(models.Model):
    name = models.CharField(max_length=3)
    rate = models.FloatField(verbose_name='Курс к USD')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'
        ordering = ('name',)


class Item(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=250, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    currency = models.ForeignKey(
        СurrencyUSDRate, on_delete=models.CASCADE,
        related_name="currency", verbose_name='Валюта')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('items:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
