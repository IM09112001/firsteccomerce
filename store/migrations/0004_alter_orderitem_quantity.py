# Generated by Django 5.0 on 2024-01-01 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_rename_comlete_order_complete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
