from django.contrib import admin

from .models import Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Конфигурация модели Post."""
    list_display = ('pk',
                    'text',
                    'pub_date',
                    'author',
                    'group'
                    )
    list_editable: tuple = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Конфигурация модели Group."""
    list_display: tuple = ('title', 'description')
