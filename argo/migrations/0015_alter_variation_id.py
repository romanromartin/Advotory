# Generated by Django 4.1.6 on 2023-02-14 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('argo', '0014_product_matt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='id',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
    ]
