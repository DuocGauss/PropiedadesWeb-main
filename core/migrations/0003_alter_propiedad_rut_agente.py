# Generated by Django 4.2.13 on 2024-06-07 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_propiedad_rut_agente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propiedad',
            name='rut_agente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.agente'),
        ),
    ]
