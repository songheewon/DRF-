from django.contrib import admin
from .models import User, UserProfile, Hobby
from django.contrib.auth.admin import UserAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'hobby':
            kwargs['queryset'] = Hobby.objects.filter(id__lte=7)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'fullname', 'email',)  # 보여주는 리스트
    list_display_links = ('username',)  # 상세로 들어가는 링크
    list_filter = ('username',)
    search_fields = ('username', 'email',)

    fieldsets = (
        ("info", {'fields': ('username', 'password', 'email', 'fullname', 'join_date',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)}),)

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date',)
        else:
            return ('join_date',)

    inlines = (
        UserProfileInline,
    )


admin.site.register(User, UserAdmin)
admin.site.register(Hobby)