# Generated by Django 5.1.7 on 2025-04-07 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base_app', '0009_techgadget'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='techgadget',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Base_app.techgadget'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product_type',
            field=models.CharField(choices=[('new_arrival', 'New Arrival'), ('featured_product', 'Featured Product'), ('earphone', 'Earphone'), ('headphone', 'Headphone'), ('techgadget', 'Tech Gadget')], max_length=20),
        ),
    ]
