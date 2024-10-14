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


class Version(models.Model):
    version_name = models.CharField(max_length=200)
    version_number = models.CharField(max_length=100, default='1.0.0')
    current_version = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, **NULLABLE, related_name='versions')

    def __str__(self):
        return f"{self.product.name} {self.version_number}"

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
