# Generated by Django 4.2.7 on 2023-11-16 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_alter_productos_make'),
        ('productos_seleccionados', '0002_alter_productos_seleccionados_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos_seleccionados',
            name='productId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_user', to='productos.productos'),
        ),
    ]
