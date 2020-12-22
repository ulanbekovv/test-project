from django.db import models

class Stock(models.Model):
    product_count = models.PositiveIntegerField('Количество продуктов', default=0)

class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-id']

    phone_number = models.CharField(verbose_name='Номер телефона', blank=True, null=True, max_length=10, unique=True)
    name = models.CharField(verbose_name='ФИО', max_length=512)
    total_bonus = models.IntegerField(verbose_name='Общий бонус', blank=True, null=True, default=0)
    card_number = models.CharField(verbose_name='Номер карты', blank=True, null=True, max_length=16)
    count = models.PositiveSmallIntegerField('Количество', blank=True, null=True, default=0)
    date = models.DateTimeField('Дата завоза', auto_now_add=True, blank=True, null=True)
