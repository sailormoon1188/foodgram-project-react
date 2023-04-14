from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomAdmin(UserAdmin):

    model = User
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', )}),
        ('Role', {'fields': ('role',)}),
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        ('Role', {'fields': ('role',)}),
    )

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'id',
        'role',
    ]

    list_filter = [
        'username',
        'email',
    ]

    search_fields = [
        'username',
        'email',
    ]

    empty_value_display = '-пусто-'
