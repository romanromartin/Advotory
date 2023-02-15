# Generated by Django 4.1.5 on 2023-02-02 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('argo', '0006_remove_subcategory_unit_product_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur', models.CharField(default='rub', max_length=10, verbose_name='валюта')),
            ],
        ),
        migrations.AlterField(
            model_name='variation',
            name='sheet',
            field=models.CharField(default='-', max_length=30, null=True, verbose_name='размер листа'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='thicknes',
            field=models.CharField(default='-', max_length=30, null=True, verbose_name='толщина'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='width',
            field=models.CharField(default='-', max_length=30, null=True, verbose_name='ширина'),
        ),
        migrations.AddField(
            model_name='product',
            name='currancy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='argo.currancy'),
        ),
    ]