# Generated by Django 4.1.7 on 2023-04-12 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_order_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_detail',
            name='size',
            field=models.CharField(default='', max_length=20),
        ),
    ]