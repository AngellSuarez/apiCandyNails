# Generated by Django 5.1.7 on 2025-04-02 03:07

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_insumoabastecimiento_estado_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='IVA',
            field=models.DecimalField(decimal_places=2, default=0.19, max_digits=10),
        ),
        migrations.AddField(
            model_name='compra',
            name='fechaCompra',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='compra',
            name='fechaIngreso',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='comprainsumo',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='comprainsumo',
            name='precioUnitario',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AddField(
            model_name='comprainsumo',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='permiso',
            name='accion',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AddField(
            model_name='permiso',
            name='modulo',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AddField(
            model_name='permiso_rol',
            name='permiso_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.permiso'),
        ),
        migrations.AddField(
            model_name='permiso_rol',
            name='rol_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.rol'),
        ),
        migrations.AddField(
            model_name='rol',
            name='descripcion',
            field=models.CharField(max_length=80, null=True, verbose_name='No hay descripcion'),
        ),
        migrations.AddField(
            model_name='rol',
            name='nombre',
            field=models.CharField(default='no ingresado', max_length=60),
        ),
    ]
