# Generated by Django 4.1.5 on 2023-01-31 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('argo', '0005_subcategory_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='unit',
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(default='шт', max_length=20),
        ),
    ]