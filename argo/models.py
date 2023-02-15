from django.db import models


class Category(models.Model):
    id_category = models.CharField(primary_key=True, max_length=30, auto_created=False)
    category = models.CharField(max_length=50)
    prw_category = models.ImageField(upload_to='static/category', default='static/category/default.webp')
    cat_description = models.TextField(null=True)

    def __str__(self):
        return self.category


class Subcategory(models.Model):
    id_sub = models.CharField(primary_key=True, max_length=30, auto_created=False)
    sub = models.CharField(max_length=50)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    prw_sub = models.ImageField(upload_to='static/sub', default='static/sub/default.webp')
    sub_description = models.TextField(null=True)


    def __str__(self):
        return self.sub


class Product(models.Model):
    id_product = models.CharField(primary_key=True, max_length=40, auto_created=False)
    product = models.CharField(max_length=60, verbose_name='продукт')
    prw_product = models.ImageField(upload_to='static/product', default='static/product/default.webp')
    cat = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    sub_cat = models.ForeignKey(Subcategory, null=True, on_delete=models.CASCADE)
    producer = models.ForeignKey('Producer', on_delete=models.CASCADE, null=True, verbose_name='производитель')
    prod_float = models.BooleanField(default=True, verbose_name='Целое число?')
    unit = models.CharField(max_length=20, default='шт')
    currancy = models.ForeignKey('Currancy', on_delete=models.CASCADE, null=True)
    matt = models.CharField(max_length=20, default='-')

    def __str__(self):
        return self.product


class Variation(models.Model):
    id = models.CharField(primary_key=True, max_length=40, auto_created=False)
    prod = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    width = models.CharField(max_length=30, default='-', null=True, verbose_name='ширина')
    sheet = models.CharField(max_length=30, default='-', null=True, verbose_name='размер листа')
    thicknes = models.CharField(max_length=30, default='-', null=True, verbose_name='толщина')
    price = models.IntegerField(verbose_name='цена')
    default = models.BooleanField(default=False, verbose_name='по умолчанию')
    color = models.CharField(max_length=20, verbose_name='цвет', default='#000')


class Currancy(models.Model):
    cur_name = models.CharField(max_length=10, default='rub', verbose_name='валюта')
    cur_value = models.FloatField(verbose_name='значение', default=1)



class Producer(models.Model):
    id_producer = models.CharField(primary_key=True, max_length=40, auto_created=False)
    producer = models.CharField(max_length=60, verbose_name='производитель')

    def __str__(self):
        return self.producer


class Order(models.Model):
    article = models.CharField(default='00000', primary_key=True, max_length=7)
    user_order = models.CharField(max_length=100, null=True, default='аноним')


class Item(models.Model):
    var_product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=5, default='1')
    matt = models.CharField(max_length=10, default='мат')



