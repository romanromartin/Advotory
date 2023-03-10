# Generated by Django 4.1.6 on 2023-02-15 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id_category', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=50)),
                ('prw_category', models.ImageField(default='static/category/default.webp', upload_to='static/category')),
                ('cat_description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Currancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_name', models.CharField(default='rub', max_length=10, verbose_name='валюта')),
                ('cur_value', models.FloatField(default=1, verbose_name='значение')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('article', models.CharField(default='00000', max_length=7, primary_key=True, serialize=False)),
                ('user_order', models.CharField(default='аноним', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id_producer', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('producer', models.CharField(max_length=60, verbose_name='производитель')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id_product', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('product', models.CharField(max_length=60, verbose_name='продукт')),
                ('prw_product', models.ImageField(default='static/product/default.webp', upload_to='static/product')),
                ('prod_float', models.BooleanField(default=True, verbose_name='Целое число?')),
                ('unit', models.CharField(default='шт', max_length=20)),
                ('matt', models.CharField(default='-', max_length=20)),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='argo.category')),
                ('currancy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='argo.currancy')),
                ('producer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='argo.producer', verbose_name='производитель')),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('width', models.CharField(default='-', max_length=30, null=True, verbose_name='ширина')),
                ('sheet', models.CharField(default='-', max_length=30, null=True, verbose_name='размер листа')),
                ('thicknes', models.CharField(default='-', max_length=30, null=True, verbose_name='толщина')),
                ('price', models.IntegerField(verbose_name='цена')),
                ('default', models.BooleanField(default=False, verbose_name='по умолчанию')),
                ('color', models.CharField(default='#000', max_length=20, verbose_name='цвет')),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='argo.product', verbose_name='продукт')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id_sub', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('sub', models.CharField(max_length=50)),
                ('prw_sub', models.ImageField(default='static/sub/default.webp', upload_to='static/sub')),
                ('sub_description', models.TextField(null=True)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='argo.category')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sub_cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='argo.subcategory'),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(default='1', max_length=5)),
                ('matt', models.CharField(default='мат', max_length=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='argo.order')),
                ('var_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='argo.variation')),
            ],
        ),
    ]
