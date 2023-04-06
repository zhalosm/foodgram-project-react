from django.contrib import admin

from recipes.models import (Amount,
                            Favorite,
                            Ingredient,
                            Recipe,
                            ShoppingCart,
                            Tag)
from users.models import Follow, User


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class AmountInLine(admin.StackedInline):
    model = Amount


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    inlines = [AmountInLine, ]


admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
