# Generated by Django 5.0 on 2024-01-08 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_alter_orderitem_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
