from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'pub_date', 'score', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category',
                    'description', 'get_genres',)
    list_editable = ('name', 'year', 'category', 'description',)
    list_filter = ('category', 'year',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name',)
    list_editable = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name',)
    list_editable = ('slug', 'name',)
    list_display_links = None
    empty_value_display = '-пусто-'
