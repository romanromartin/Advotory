# Generated by Django 4.1.5 on 2023-01-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('argo', '0002_alter_width_width'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prod_float',
            field=models.BooleanField(default=True, verbose_name='Целое число?'),
        ),
    ]
