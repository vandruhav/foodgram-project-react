from django.contrib import admin

from .models import MyUser, Follow


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_staff', 'is_superuser',
                    'first_name', 'last_name',)
    list_filter = ('email', 'username',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    list_editable = ('user', 'author',)
    empty_value_display = '-пусто-'


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Follow, FollowAdmin)
