# Generated by Django 4.2 on 2023-04-08 21:04

import recipes.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredient_measurement_unit_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterField(
            model_name='amount',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[recipes.validators.validate_amount], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[recipes.validators.validate_cooking_time], verbose_name='Время приготовления в минутах'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, upload_to='images/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, validators=[recipes.validators.validate_color_code], verbose_name='Цвет'),
        ),
    ]
