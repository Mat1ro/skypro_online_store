from django.db import models

from skypro_online_store.settings import NULLABLE


class Product(models.Model):
    name = models.CharField(max_length=100, )
    description = models.TextField()
    image = models.ImageField(upload_to='images/', **NULLABLE)
    category = models.CharField(max_length=100)
    price_per_unit = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
